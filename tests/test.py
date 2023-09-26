import os
import json
import sys
import snap
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__" :
    # IMPORT DATA
    # Open the JSON file for reading
    json_file_path = os.path.join('twitch\PTBR', 'musae_PTBR_features.json')

    with open(json_file_path, 'r') as json_file:
        # Load the JSON data into a Python dictionary
        adj_list_twitch = json.load(json_file)

    nodes_twitch = os.path.join('twitch\PTBR', 'musae_PTBR_target.csv')
    nodes_df = pd.read_csv(nodes_twitch)

    max_node = nodes_df['new_id'].max()

    edges_twitch = os.path.join('twitch\PTBR', 'musae_PTBR_edges.csv')
    edges_df = pd.read_csv(edges_twitch)

    # SNAP GRAPH
    # G_twitch = snap.TUNGraph.New()
    # for node in range(0, len(nodes_df)):
    #     G_twitch.AddNode(node)
    
    # for _, row in edges_df.iterrows():
    #     source = row['from']
    #     target = row['to']
    #     G_twitch.AddEdge(source, target)

    # print(f"Number of nodes: {G_twitch.GetNodes()}")
    # print(f"Number of edges: {G_twitch.GetEdges()}")