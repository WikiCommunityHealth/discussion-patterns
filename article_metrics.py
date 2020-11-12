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

import numpy as np
import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt


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


def get_article_data(file_path, should_clean_data=True):
    df = pd.read_json(file_path, lines=True, orient='records')
    return clean_article_data(df) if should_clean_data else df

# input file: all the records for a discussion page from the wiki conv dataset
# https://github.com/conversationai/wikidetox/tree/master/wikiconv
df = get_article_data("out_bruni.json")
# -

# # Analyzing article data

# +
# graph for deletion and modification (dm actions):
# - each node v is a user involved in the article
# - each edge (u,v) implies that user u has done a dm action on user v

G = nx.DiGraph()
G.add_nodes_from(df['user'].unique())

for index, record in enumerate(df.iloc()):
    if record.parentId and record.type in ['MODIFICATION', 'DELETION']:
        try:
            parent_record = df[df['id'] == record.parentId].iloc[0]
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
G.add_nodes_from(df['user'].unique())

for index, record in enumerate(df.iloc()):
    if record.replytoId and record.type in ['ADDITION', 'CREATION']:
        try:
            parent_record = df[df['id'] == record.replytoId].iloc[0]
            if parent_record.user != record.user:
                G.add_edge(record.user, parent_record.user)
        except:
            pass
        
nx.draw_shell(G, with_labels=True)
print(G.in_degree)
