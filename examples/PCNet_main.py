#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import configparser
from PCNet import PCNet_parser as pp
from PCNet import PCNet_network as pcn
import networkx as nx

__author__ = "Alessandro Lapi"
__email__ = "alessandro.lapi@studio.unibo.it"

# CONFIGURATION
# Define a function to read the configuration data from the file
def read_configuration(file_path):
    # Read the configuration data from the file
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

# Set up the argument parser
parser = argparse.ArgumentParser(description='Read configuration from a .ini file.')

# Add the argument for the configuration.ini file
parser.add_argument('--config_file', type=str, default='../configuration.ini', help='Path to the configuration.ini file') # default='../configuration.ini', 

# Parse the command-line arguments
args = parser.parse_args()

# Access the provided configuration.ini file path
config_file_path = args.config_file

# Read the configuration data from the file
try:
    config = read_configuration(config_file_path)
    print("Configuration loaded successfully.")
except FileNotFoundError:
    print(f"Error: File '{config_file_path}' not found.")
except configparser.Error as e:
    print(f"Error: Failed to read the configuration file - {e}")


pubmed_path = config.get('path settings', 'pubmed_path')
csv_path = config.get('path settings', 'csv_path')
graph_path = config.get('path settings', 'graph_path')

mesh = config.get('mesh settings', 'mesh')
term_mesh = config.get('mesh settings', 'term_mesh')

info = list(config.get('informations settings', 'info').split(', '))

connected = config.getboolean('graph settings', 'connected')
keep_unknown_nodes = config.getboolean('graph settings', 'keep_unknown_nodes')

# PARSE
csv_list = pp.xml_parser(path_xml=pubmed_path, path_csv=csv_path, MeSH=mesh, informations=info)

# DATAFRAMES
df_links = pcn.csv_to_dataframe(csv_list, type_of_df='links')
df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=info)

# GRAPH
graph = pcn.df_to_graph(df_links, df_nodes, connected_graph=connected, unknown_nodes=keep_unknown_nodes)

# SAVE THE GRAPH
if term_mesh == '':
    term_mesh = 'pubmed'
nx.write_gexf(graph, graph_path + term_mesh + '.gexf') 
