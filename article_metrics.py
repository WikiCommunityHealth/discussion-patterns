# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Imports and setup

# +
import numpy as np
import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt

# mongoDB
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017, maxPoolSize=200)
records = client.discussions['wiki-conv']


# -

# # Getting article data

# +
# sort the records by timestamp in descending order to build the tree

def clean_article_data(df):
    def collapse_user_name(x):
        res = ''
        if 'ip' in x:
            res = x['ip']
        else:
            res = x['text']
        return res
    
    df.sort_values("timestamp", inplace=True, ascending=False)
    df.reset_index()
    df["user"] = df["user"].apply(collapse_user_name)
    return df


def get_article_data(page_id: str, should_clean_data=True):
    # df = pd.read_json(file_path, lines=True, orient='records')
    df = pd.DataFrame(records.find({"pageId": page_id}).sort("timestamp", pymongo.ASCENDING))
    return clean_article_data(df) if should_clean_data else df
    

# input data: all the actions for a discussion page from the wiki conv dataset
# https://github.com/conversationai/wikidetox/tree/master/wikiconv
df_article = get_article_data("687")
# -

# # Analyzing article data

# +
# graph for deletion and modification (dm actions):
# - each node v is a user involved in the article
# - each edge (u,v) implies that user u has done a dm action on user v

G = nx.DiGraph()
G.add_nodes_from(df_article['user'].unique())

for index, record in enumerate(df_article.iloc()):
    if record.parentId and record.type in ['MODIFICATION', 'DELETION']:
        try:
            parent_record = df_article[df_article['id'] == record.parentId].iloc[0]
            if parent_record.user != record.user:
                G.add_edge(record.user, parent_record.user)
        except:
            pass
        
nx.draw_shell(G, with_labels=True)
print(G.in_degree)
# +
# graph for addition and creation (ac actions):
# - each node v is a user involved in the article
# - each edge (u,v) implies that user u has done a ac action on user v

G = nx.DiGraph()
G.add_nodes_from(df_article['user'].unique())

for index, record in enumerate(df_article.iloc()):
    if record.replytoId and record.type in ['ADDITION', 'CREATION']:
        try:
            parent_record = df_article[df_article['id'] == record.replytoId].iloc[0]
            if parent_record.user != record.user:
                G.add_edge(record.user, parent_record.user)
        except:
            pass
        
nx.draw_shell(G, with_labels=True)
print(G.in_degree)
# -
# # Getting number of article with minimum number of actions

df_index = pd.read_json('dataset/wikiconv-it/article_index_it.json', orient='records', lines = True)

# +
min_actions = np.array([0, 1, 2, 3, 4, 5, 10, 15, 20, 50, 100, 500, 1000, 5000, 10000, 30000])

df_num_actions = pd.DataFrame(data={'min_actions': min_actions})
df_num_actions['num_articles'] = df_num_actions['min_actions'].apply(
    lambda x: len(df_index[df_index['numActions'] > x].index))

plt.figure()
df_num_actions.plot.bar(x='min_actions', y='num_articles')
# -

# # Getting stats about type of actions inside each article

"""
import multiprocessing as mp
pool = mp.Pool(mp.cpu_count())

from tqdm import tqdm

actions = {
    'CREATION': np.zeros(num_rows),
    'ADDITION': np.zeros(num_rows),
    'MODIFICATION': np.zeros(num_rows),
    'DELETION': np.zeros(num_rows),
    'RESTORATION': np.zeros(num_rows)
}
client.close()
def process(page_id, index):
    print(ciao)
    clientt = MongoClient('localhost', 27017)
    recordss = clientt.discussions['wiki-conv']
    df = pd.DataFrame(recordss.find({"pageId": str(page_id)}).sort("timestamp", pymongo.ASCENDING))
    print(len(pd.index))
    for action_type in actions.keys():
        print(len(df[df['type'] == action_type].index))
        actions[action_type][index] = len(df[df['type'] == action_type].index)

for index, record in tqdm(df_test.iterrows(), total=num_rows):
    pool.apply_async(process, args=(record['_id'], index))
    
pool.close()
pool.join()
    
print(actions)
"""

df_test = df_index[(df_index['numActions'] > 20)].sample(n = 50)
df_test.reset_index(inplace=True, drop=True)
num_rows = len(df_test.index)
df_test.tail()

# +
from tqdm import tqdm

actions = {
    'CREATION': np.zeros(num_rows),
    'ADDITION': np.zeros(num_rows),
    'MODIFICATION': np.zeros(num_rows),
    'DELETION': np.zeros(num_rows),
    'DM_OTHER_USER': np.zeros(num_rows),
    'DM_OTHER_TOXIC': np.zeros(num_rows),
    'RESTORATION': np.zeros(num_rows)
}

def process(page_id, index):
    df = pd.DataFrame(records.find({"pageId": str(page_id)}).sort("timestamp", pymongo.ASCENDING))
    for action_type in actions.keys():
        if action_type not in ['DELETION_OTHER_USER', 'DELETION_OTHER_TOXIC']:
            actions[action_type][index] = len(df[df['type'] == action_type].index)
        
    df_deletion = df[(df['type'] == 'DELETION') | (df['type'] == 'MODIFICATION')]
    for index2, record2 in df_deletion.iterrows():
        try:
            parent_record = df[df['id'] == record2.parentId].iloc[0]
            if parent_record.user != record2.user:
                actions['DM_OTHER_USER'][index] += 1
                if record2.score['toxicity'] > 0.3:
                    actions['DM_OTHER_TOXIC'][index] += 1
        except:
            pass
    

for index, record in tqdm(df_test.iterrows(), total=num_rows):
    process(record['_id'], index)
# -

actions['DM_OTHER_USER'][0] = 0
actions['DM_OTHER_TOXIC'][0] = 0
process(6055134, 0)

# +
for action_type in actions.keys():
    df_test[action_type] = actions[action_type]
    
df_test
# -


