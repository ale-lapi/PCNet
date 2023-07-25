#!/usr/bin/env python
# -*- coding: utf-8 -*-


import networkx as nx
import configparser
from PCNet import PCNet_parser as pp
from PCNet import PCNet_network as pcn

__author__ = "Alessandro Lapi"
__email__ = "alessandro.lapi@studio.unibo.it"


# CONFIGURATION   
config = configparser.ConfigParser()
config.read('../configuration.ini')

pubmed_path = config.get('path settings', 'pubmed_path')
csv_path = config.get('path settings', 'csv_path')
graph_path = config.get('path settings', 'graph_path')


mesh = config.get('mesh settings', 'mesh')
term_mesh = config.get('mesh settings', 'term_mesh')

info = list(config.get('informations settings', 'info').split(', '))
# print(info)

connected = config.getboolean('graph settings', 'connected')
keep_unknown_nodes = config.getboolean('graph settings', 'keep_unknown_nodes')

# PARSE
pp.xml_parser(path_xml=pubmed_path, path_csv=csv_path, MeSH=mesh, informations=info)

# DATAFRAMES
df_links = pcn.csv_to_dataframe(path_csv=csv_path, type_of_df='links')
df_nodes = pcn.csv_to_dataframe(path_csv=csv_path, type_of_df='nodes', columns=info)

# GRAPH
graph = pcn.df_to_graph(df_links, df_nodes, connected_graph=connected, unknown_nodes=keep_unknown_nodes)

# SAVE THE GRAPH
if term_mesh == '':
    term_mesh = 'pubmed'
nx.write_gexf(graph, graph_path + term_mesh + '.gexf') 
