import numpy as np
import pandas as pd
# import subprocess

df = pd.read_json('./../dataset/wikiconv-it/article_index_it.json', orient='records', lines = True)

num_files = 100
total_actions = df['numActions'].sum()
print(f'There are {total_actions} element to extract in {num_files} files')

threshold = total_actions / num_files

base = 0
length = 0
file_index = 0

with open('export-it.sh', 'w') as filehandle:
  for index, record in df.iterrows():
    num_actions = record['numActions']
    length += num_actions

    if (length > threshold):
      print(f'From {base} with {length} records')

      bashCommand = "mongoexport --host localhost:27017 --db=wiki-conv-it --collection=full --out=test" + str(file_index) + ".json --sort='{pageId: 1, timestamp: 1}' --limit=" + str(length) + " --skip=" + str(base)
      filehandle.write(bashCommand + "\n")

      base += length
      length = 0
      file_index += 1
    
  bashCommand = "mongoexport --host localhost:27017 --db=wiki-conv-it --collection=full --out=test" + str(file_index) + ".json --sort='{pageId: 1, timestamp: 1}' --limit=" + str(length) + " --skip=" + str(base)
  filehandle.write(bashCommand + "\n")

    # if index > 200:
    #   break