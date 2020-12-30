import json
import datetime
from pymongo import MongoClient
from multiprocessing import Pool
import os

from articlemetrics import NewUsersByMonth, ActionsType, MutualChain

def date_hook(json_dict):
  try:
    json_dict['timestamp'] = datetime.datetime.strptime(json_dict['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
  except:
    pass
  return json_dict

def send_data(data):
  if data != []:
    client = MongoClient('localhost', 27017)
    infos = client.articles.test
    result = infos.insert_one(data)

def analyze_wiki_conv_file(file_path):
  with open(file_path) as file:

    last_line_page_id = '-1'
    is_new_discussion_page = True
    num_lines_current_discussion_page = 0

    # Metric initialization
    m_new_users_by_month = NewUsersByMonth()
    m_actions_type = ActionsType()
    m_mutual_chains = MutualChain()

    for line in file:
      record = json.loads(line, object_hook=date_hook) 
      is_new_discussion_page = last_line_page_id != record['pageId']

      if is_new_discussion_page and last_line_page_id != '-1':
        # STEP #1: save result from previous discussione page to db
        print(last_line_page_id, num_lines_current_discussion_page)
        # print(m_new_users_by_month.calculate())
        # print(m_actions_type.calculate())
        # send_data(m_mutual_chains.calculate())
        send_data({
          'pageId': int(last_line_page_id),
          'numActions': num_lines_current_discussion_page,
          'actionsType': m_actions_type.calculate(),
          'newUsersByMonth': m_new_users_by_month.calculate(),
          'mutualChains': m_mutual_chains.calculate(),
          'numMutualChains': m_mutual_chains.num_chains
        })

        # STEP #2: recreate structures for metrics calculation
        num_lines_current_discussion_page = 0
        m_new_users_by_month.reset()
        m_actions_type.reset()
        m_mutual_chains.reset()

      # get metadata about current line
      username = ''
      if 'user' in record and 'text' in record['user']:
        username = record['user']['text']
      elif 'user' in record and 'ip' in record['user']:
        username = record['user']['ip']
      else:
        username = 'unknown'
        
      current_month_year = f"{record['timestamp'].month}/{record['timestamp'].year}"

      # add info to metrics calculators
      m_new_users_by_month.add_info(username, current_month_year)
      m_actions_type.add_info(record['type'])
      m_mutual_chains.add_info(record, username)

      num_lines_current_discussion_page += 1
      last_line_page_id = record['pageId']

    # last discussion page
    print(last_line_page_id, num_lines_current_discussion_page)
    # print(m_new_users_by_month.calculate())
    # print(m_actions_type.calculate())
    # print(m_mutual_chains.calculate())
    # send_data(m_mutual_chains.calculate())
    send_data({
      'pageId': int(last_line_page_id),
      'numActions': num_lines_current_discussion_page,
      'actionsType': m_actions_type.calculate(),
      'newUsersByMonth': m_new_users_by_month.calculate(),
      'mutualChains': m_mutual_chains.calculate(),
      'numMutualChains': m_mutual_chains.num_chains
    })


if __name__ == "__main__":
  # file_paths = ['data/filosofia.json', 'data/0-502.json', 'data/503-999.json']
  # file_paths = ['../../it-splitted/it-part0.json']
  # analyze_wiki_conv_file(file_paths[0])

  output = []
  for root, dirs, files in os.walk("../../it-splitted"):
    for filename in files:
      if filename[0:2] == 'it':
        output.append(f"../../it-splitted/{filename}")

  with Pool(processes=4) as pool:        
    pool.map(analyze_wiki_conv_file, output)