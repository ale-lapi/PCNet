#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
from PCNet import PCNet_parser as pp
from PCNet import PCNet_network as pcn
from datetime import datetime
from gzip import GzipFile

__author__ = "Alessandro Lapi"
__email__ = "alessandro.lapi@studio.unibo.it"

# Path to the data
if not os.path.exists('../data/'):
    os.makedirs('../data/')
path_data = '../data/'
path_test = '../data/test/'

# Random MeSH and term for testing
mesh = 'D000328'
mesh_word = 'adult'


def test_get_pmid():
    """
    Test the get_pmid function.
    It checks if the pmid is an integer and if it has the right length.
    """
    xml_file = GzipFile(path_test + 'test.xml.gz', 'r')
    parse_file = ET.parse(xml_file)

    min_pmid, max_pmid = 100000, 100000000

    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_pmid(node)) == int
        assert min_pmid < pp.get_pmid(node) < max_pmid

def test_get_title():
    """
    Test the get_title function.
    It checks if the title is a string and if it does not contain '\n' or '\t'.
    """
    xml_file = GzipFile(path_test + 'test.xml.gz', 'r')
    parse_file = ET.parse(xml_file)
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_title(node)) == str 
        assert '\n' not in pp.get_title(node)
        assert '\t' not in pp.get_title(node)
     
def test_get_abstract():
    """
    Test the get_abstract function.
    It checks if the abstract is a string and if it does not contain '\n' or '\t'.
    """
    xml_file = GzipFile(path_test + 'test.xml.gz', 'r')
    parse_file = ET.parse(xml_file)
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_abstract(node)) == str
        assert '\n' not in pp.get_abstract(node)
        assert '\t' not in pp.get_abstract(node)

def validate_date(date_string):
    """
    Validate that a date string is in the expected format. 

    Parameters
    ----------
    date_string : str
        The date string to validate.

    Returns
    -------
    bool
        True if the date string is in the expected format, False otherwise.
    """
    try:
        datetime.strptime(date_string, expected_format="%Y-%m-%d")
        return True
    except ValueError:
        return False

def test_get_publication_date():
    """
    Test the get_publication_date function. 
    It checks if the date is a string, if it does not contain '\n' or '\t' and if it is in the right format.
    """
    xml_file = GzipFile(path_test + 'test.xml.gz', 'r')
    parse_file = ET.parse(xml_file)
    for node in parse_file.getroot().iter('PubmedArticle'):
        if pp.get_publication_date(node) != '':
            continue
        assert type(pp.get_publication_date(node)) == str
        assert '\n' not in pp.get_publication_date(node)
        assert '\t' not in pp.get_publication_date(node)
        assert validate_date(pp.get_publication_date(node), "%Y-%m-%d") == True

def test_get_authors():
    """
    Test the get_authors function.
    It checks if the authors is a string and if it does not contain '\n' or '\t'.
    """
    xml_file = GzipFile(path_test + 'test.xml.gz', 'r')
    parse_file = ET.parse(xml_file)
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_authors(node)) == str
        assert '\n' not in pp.get_authors(node)
        assert '\t' not in pp.get_authors(node)

def test_get_journal():
    """
    Test the get_journal function.
    It checks if the journal is a string and if it does not contain '\n' or '\t'.
    """
    xml_file = GzipFile(path_test + 'test.xml.gz', 'r')
    parse_file = ET.parse(xml_file)
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_journal(node)) == str
        assert '\n' not in pp.get_journal(node)
        assert '\t' not in pp.get_journal(node)

def test_get_keywords():
    """
    Test the get_keywords function.
    It checks if the keywords is a string and if it does not contain '\n' or '\t'.
    """
    xml_file = GzipFile(path_test + 'test.xml.gz', 'r')
    parse_file = ET.parse(xml_file)
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_keywords(node)) == str
        assert '\n' not in pp.get_keywords(node)
        assert '\t' not in pp.get_keywords(node)

def test_get_references():
    """
    Test the get_references function.
    It checks if the references is a string and if it does not contain '\n' or '\t'.
    """
    xml_file = GzipFile(path_test + 'test.xml.gz', 'r')
    parse_file = ET.parse(xml_file)
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_references(node)) == str
        assert '\n' not in pp.get_references(node)
        assert '\t' not in pp.get_references(node)


def test_xml_parser():
    """
    Test the xml_parser function.
    It checks if the xml_parser function creates the right files.
    """
    pp.xml_parser(path_test, path_test)
    assert os.path.exists(path_test + 'links_test.xml.gz.csv')
    assert os.path.exists(path_test + 'nodes_test.xml.gz.csv')

def test_csv_to_dataframe():
    """
    Test the csv_to_dataframe function.
    It checks if the csv_to_dataframe function creates pandas dataframes of the right shape.
    """

    info = ['title', 'abstract', 'date', 'authors', 'journal', 'keywords']
    pp.xml_parser(path_test, path_test, informations=info)
    df_links = pcn.csv_to_dataframe(path_test, type_of_df='links')
    df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes')

    assert type(df_links) == pd.core.frame.DataFrame
    assert type(df_nodes) == pd.core.frame.DataFrame
    assert df_links.shape[1] == 2
    assert df_nodes.shape[1] == 2 + len(info)


def test_mesh_selection():
    """
    Test the mesh selection in the xml_parser function and csv_to_dataframe function.
    It checks if the xml_parser function creates the right files and if the keywords column contains the mesh_word.
    """
    pp.xml_parser(path_test, path_test, MeSH=mesh)

    assert os.path.exists(path_test + 'links_test.xml.gz.csv')
    assert os.path.exists(path_test + 'nodes_test.xml.gz.csv') 
    
    df = pcn.csv_to_dataframe(path_test, type_of_df='nodes')

    assert df['keywords'].str.contains(mesh_word).any() == True

def test_no_mesh_selection():
    """
    Test the no mesh selection in the xml_parser function and csv_to_dataframe function.
    It checks if if all the articles in the xml file are parsed. 
    """
    pp.xml_parser(path_test, path_test) 
    df = pcn.csv_to_dataframe(path_test, type_of_df='nodes')
    xml_file = GzipFile(path_test + 'test.xml.gz', 'r')
    test_xml = ET.parse(xml_file)

    assert len(test_xml.getroot()) == len(df)
    

def test_title_selecion():
    """
    Test the title selection. It checks the shape of the dataframe and if the title column is in the dataframe.
    """
    title = ['title']
    pp.xml_parser(path_test, path_test, informations='title')
    title_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=title)

    assert 'title' in title_df_nodes.columns
    assert title_df_nodes.shape[1] == 3

def test_no_title_selecion():
    """
    Test the title not selection. It checks the shape of the dataframe and if the title column is not in the dataframe.
    """
    no_title = ['abstract', 'date', 'authors', 'journal', 'keywords']
    pp.xml_parser(path_test, path_test, informations=no_title)
    no_title_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=no_title)

    assert 'title' not in no_title_df_nodes.columns
    assert no_title_df_nodes.shape[1] == 7

def test_abstract_selecion():
    """
    Test the abstract selection. It checks the shape of the dataframe and if the abstract column is in the dataframe.
    """
    abstract = ['abstract']
    pp.xml_parser(path_test, path_test, informations=abstract)
    abstract_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=abstract)

    assert 'abstract' in abstract_df_nodes.columns
    assert abstract_df_nodes.shape[1] == 3

def test_no_abstract_selecion():
    """
    Test the abstract not selection. It checks the shape of the dataframe and if the abstract column is not in the dataframe.
    """
    no_abstract = ['title', 'date', 'authors', 'journal', 'keywords']
    pp.xml_parser(path_test, path_test, informations=no_abstract)
    no_abstract_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=no_abstract)

    assert 'abstract' not in no_abstract_df_nodes.columns
    assert no_abstract_df_nodes.shape[1] == 7

def test_date_selecion():
    """
    Test the date selection. It checks the shape of the dataframe and if the date column is in the dataframe.
    """
    date = ['date']
    pp.xml_parser(path_test, path_test, informations=date)
    date_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=date)

    assert 'date' in date_df_nodes.columns
    assert date_df_nodes.shape[1] == 3

def test_no_date_selecion():
    """
    Test the date not selection. It checks the shape of the dataframe and if the date column is not in the dataframe.
    """
    no_date = ['title', 'abstract', 'authors', 'journal', 'keywords']
    pp.xml_parser(path_test, path_test, informations=no_date)
    no_date_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=no_date)

    assert 'date' not in no_date_df_nodes.columns
    assert no_date_df_nodes.shape[1] == 7

def test_authors_selecion():
    """
    Test the authors selection. It checks the shape of the dataframe and if the authors column is in the dataframe.
    """
    authors = ['authors']
    pp.xml_parser(path_test, path_test, informations=authors)
    authors_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=authors)

    assert 'authors' in authors_df_nodes.columns
    assert authors_df_nodes.shape[1] == 3

def test_no_authors_selecion():
    """
    Test the authors not selection. It checks the shape of the dataframe and if the authors column is not in the dataframe.
    """
    no_authors = ['title', 'abstract', 'date', 'journal', 'keywords']
    pp.xml_parser(path_test, path_test, informations=no_authors)
    no_authors_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=no_authors)

    assert 'authors' not in no_authors_df_nodes.columns
    assert no_authors_df_nodes.shape[1] == 7

def test_journal_selecion():
    """
    Test the journal selection. It checks the shape of the dataframe and if the journal column is in the dataframe.
    """
    journal = ['journal']
    pp.xml_parser(path_test, path_test, informations=journal)
    journal_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=journal)

    assert 'journal' in journal_df_nodes.columns
    assert journal_df_nodes.shape[1] == 3

def test_no_journal_selecion():
    """
    Test the journal not selection. It checks the shape of the dataframe and if the journal column is not in the dataframe.
    """
    no_journal = ['title', 'abstract', 'date', 'authors', 'keywords']
    pp.xml_parser(path_test, path_test, informations=no_journal)
    no_journal_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=no_journal)

    assert 'journal' not in no_journal_df_nodes.columns
    assert no_journal_df_nodes.shape[1] == 7

def test_keywords_selecion():
    """
    Test the keywords selection. It checks the shape of the dataframe and if the keywords column is in the dataframe.
    """
    keywords = ['keywords']
    pp.xml_parser(path_test, path_test, informations=keywords)
    keywords_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=keywords)

    assert 'keywords' in keywords_df_nodes.columns
    assert keywords_df_nodes.shape[1] == 3

def test_no_keywords_selecion():
    """
    Test the keywords not selection. It checks the shape of the dataframe and if the keywords column is not in the dataframe.
    """
    no_keywords = ['title', 'abstract', 'date', 'authors', 'journal']
    pp.xml_parser(path_test, path_test, informations=no_keywords)
    no_keywords_df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=no_keywords)

    assert 'keywords' not in no_keywords_df_nodes.columns
    assert no_keywords_df_nodes.shape[1] == 7

def test_all_selecion():
    """
    Test the all selection. It checks the shape of the dataframe and if all the columns are in the dataframe.
    """
    info = ['title', 'abstract', 'date', 'authors', 'journal', 'keywords']
    pp.xml_parser(path_test, path_test, informations=info)
    df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=info)

    for column in info:
        assert column in df_nodes.columns
    
    assert df_nodes.shape[1] == 2 + len(info)
    assert df_nodes.shape[1] == 8

def test_no_selecion():
    """
    Test the no selection. It checks the shape of the dataframe.
    """
    no_info = []
    pp.xml_parser(path_test, path_test, informations=no_info)
    df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=no_info)

    assert df_nodes.shape[1] == 2  


def test_is_empty_csv():
    """
    Test the is_empty_csv function.
    """
    assert pcn.is_empty_csv(path_test + 'test_empty.csv') == True
    assert pcn.is_empty_csv(path_test + 'test_not_empty.csv') == False


def test_df_to_graph():
    """
    Test the df_to_graph function.
    It checks if the df_to_graph function creates a networkx graph.
    """
    info = ['title', 'abstract', 'date', 'authors', 'journal', 'keywords']
    pp.xml_parser(path_test, path_test, informations=info)
    df_links = pcn.csv_to_dataframe(path_test, type_of_df='links')
    df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=info)

    graph = pcn.df_to_graph(df_links, df_nodes, unknown_nodes=True)

    assert type(graph) == nx.classes.digraph.DiGraph

def test_connected_graph():
    """
    Test the connected graph selection of the df_to_graph function.
    """
    info = []
    pp.xml_parser(path_test, path_test, informations=info)
    df_links = pcn.csv_to_dataframe(path_test, type_of_df='links', columns=info)
    df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=info)
    graph_connected = pcn.df_to_graph(df_links, df_nodes, connected_graph=True, unknown_nodes=True)
    graph_not_connected = pcn.df_to_graph(df_links, df_nodes, connected_graph=False, unknown_nodes=True)
    
    assert nx.is_weakly_connected(graph_connected) == True
    assert nx.is_weakly_connected(graph_not_connected) == False
    assert len(graph_connected.nodes()) <= len(graph_not_connected.nodes())

def test_unknown_nodes():
    """
    Test the unknown nodes selection of the df_to_graph function.
    It checks if the graph with unknown nodes has more nodes than the graph without unknown nodes.
    It also checks if the nodes in the graph without unknown nodes have no empty attributes.   
    """
    info = ['title', 'abstract', 'date', 'authors', 'journal', 'keywords']
    pp.xml_parser(path_test, path_test, informations=info)
    df_links = pcn.csv_to_dataframe(path_test, type_of_df='links')
    df_nodes = pcn.csv_to_dataframe(path_test, type_of_df='nodes', columns=info)
    graph_unknown_nodes = pcn.df_to_graph(df_links, df_nodes, connected_graph=False, unknown_nodes=True)
    graph_no_unknown_nodes = pcn.df_to_graph(df_links, df_nodes, connected_graph=False, unknown_nodes=False)
    
    assert len(graph_unknown_nodes.nodes()) >= len(graph_no_unknown_nodes.nodes())

    for node in list(graph_no_unknown_nodes.nodes(data=True)):
        assert node[1] != {}


def test_nodes_to_df():
    """
    Test the nodes_to_df function. 
    It checks if the nodes_to_df function creates a pandas dataframe of the right shape.
    It also checks if the first column is 'pmid'.
    """
    info = ['title', 'abstract', 'date', 'authors', 'journal', 'keywords']
    
    G = nx.read_gexf(path_test + 'test.gexf')
    df_nodes_graph = pcn.nodes_to_df(G)

    assert type(df_nodes_graph) == pd.core.frame.DataFrame
    assert df_nodes_graph.shape[1] == 2 + len(info)
    assert df_nodes_graph.columns[0] == 'pmid'
    
    # for column in info:
    #     assert column in df_nodes_graph.columns

def test_links_to_df():
    """
    Test the links_to_df function.
    It checks if the links_to_df function creates a pandas dataframe of the right shape.
    It also checks if the first column is 'source' and the second column is 'target'.
    """
    G = nx.read_gexf(path_test + 'test.gexf')
    df_links_graph = pcn.links_to_df(G)

    assert type(df_links_graph) == pd.core.frame.DataFrame
    assert df_links_graph.shape[1] == 2
    assert df_links_graph.columns[0] == 'source'
    assert df_links_graph.columns[1] == 'target'


