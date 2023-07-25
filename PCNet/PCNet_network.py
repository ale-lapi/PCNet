#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm
import pandas as pd
import networkx as nx
import csv
import configparser
from PCNet import PCNet_parser as pp

__author__ = "Alessandro Lapi"
__email__ = "alessandro.lapi@studio.unibo.it"


def csv_to_dataframe(path_csv, type_of_df, columns=['title', 
                                                    'abstract', 
                                                    'date', 
                                                    'authors', 
                                                    'journal',
                                                    'keywords',
                                                    ]):
    """
    Create a dataframe from the csv files. 
    Specify if you want the links or the nodes, with the type_of_df parameter.
    Specify the columns of the dataframe with the columns parameter: if you want the links,
    the columns are ['source', 'target'], if you want the nodes, the columns are by default
    ['pmid', 'title', 'abstract', 'date', 'authors', 'journal', 'keywords', 'references'].
    If you created the csv files with less informations, you can specify the columns you want
    in the columns parameter. For example, if you created the csv files with only the title 
    and the abstract, you can write: columns=['title', 'abstract'].


    Parameters
    ----------
    path : str
        Path of the csv files
    type_of_df : str
        'links' or 'nodes' according to the type of dataframe the user wants
    columns : list
        List of the columns of the dataframe. 

    Returns
    -------
    df : pandas dataframe
        Dataframe with the links or the nodes
    """
    csv_files = [file for file in os.listdir(path_csv) if file.startswith(type_of_df)]
    l = []

    for file in tqdm(csv_files, desc='- Processing csv files ...'):

        # Skip the file if it is empty
        if is_empty_csv(path_csv + file) == True:
            print(f"{file}  is empty")
            continue

        df = pd.read_csv(path_csv + file, sep='\t', header=None, quoting=csv.QUOTE_NONE)
        l.append(df)

    if len(l) != 0:
        df = pd.concat(l, axis=0, ignore_index=True)

        # Rename the columns of the dataframe according to the type of dataframe
        if type_of_df == 'links':
            df.columns = ['source', 'target']
        else:
            df.columns = ['pmid'] + columns + ['references']
            df = df.fillna('') # Replace NaN values by empty strings
        return df
    
    else:
        return None

def df_to_graph(df_links, df_nodes, connected_graph=True, unknown_nodes=False):
    """
    Create a graph from the links and the nodes dataframes.
    Each nodes of the graph has its attributes, if known. 
    The attributes are the informations extracted with the parse_xml function.
    Self loops are removed from the graph.
    
    Parameters
    ----------
    df_links : pandas dataframe
        Dataframe with the links
    df_nodes : pandas dataframe
        Dataframe with the nodes
    connected : boolean
        If True, the graph will be connected (default: True)
    keep_unkown_nodes : boolean
        If True, the graph will keep the nodes whose informations are not known (default: False)
        
    Returns
    -------
    G : networkx graph
        Graph created from the links and the nodes dataframes
    """
    if unknown_nodes == False:
        df_links = df_links[df_links['target'].isin(df_nodes['pmid'])]
        
    G = nx.from_pandas_edgelist(df_links, source='source', target='target', create_using=nx.DiGraph())
    G.remove_edges_from(nx.selfloop_edges(G))

    if connected_graph == True:
        G = G.subgraph(max(nx.weakly_connected_components(G), key=len))

    nodes = list(G.nodes())
    df_nodes = df_nodes[df_nodes['pmid'].isin(nodes)]

    # Add the attributes to the nodes
    for index, row in df_nodes.iterrows():
        if row['pmid'] in G.nodes:
            for col in df_nodes.columns:
                if col != 'pmid':
                    G.nodes[row['pmid']].update({col: row[col]})

    return G

def is_empty_csv(csv_file):
    """
    Check if a csv file is empty
    
    Parameters
    ----------
    csv_file : str
        Path to the csv file
        
    Returns
    -------
    boolean
        True if the csv is empty, False otherwise
    """
 
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:  
                return False
    return True


def nodes_to_df(path):
    """
    Return a dataframe of nodes from the attributes of the input .gexf graph  

    Parameters
    ----------
    path : str
        Path of the .gexf graph

    Returns
    -------
    df : pandas dataframe
        Dataframe of nodes 
    """
    nodes = []

    G = nx.read_gexf(path)

    for node in G.nodes(data=True):
        nodes.append(node[1])

    df = pd.DataFrame(nodes)

    # Reorder the columns and rename the label column to have the same format of the csv files
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]
    df = df.rename(columns={'label': 'pmid'})

    return df

def links_to_df(path):
    """
    Return a dataframe of links from the edges of the input .gexf graph.

    Parameters
    ----------
    path : str
        Path of the .gexf graph 

    Returns
    -------
    df : pandas dataframe  
        Dataframe of links
    """
    edges = []
    
    G = nx.read_gexf(path)

    for edge in G.edges(data=True):
        edges.append(edge)

    df = pd.DataFrame(edges)

     # Rename the columns and remove the label column to have the same format of the csv files
    df = df.drop([2], axis=1)
    df = df.rename(columns={0: 'source', 1: 'target'})
    
    return df

