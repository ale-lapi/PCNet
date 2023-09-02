#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
from PCNet import PCNet_parser as pp
from PCNet import PCNet_network as pcn
from PCNet import PCNet_utils as utils
import pytest
from gzip import GzipFile
import csv

__author__ = "Alessandro Lapi"
__email__ = "alessandro.lapi@studio.unibo.it"

# Path to the data
if not os.path.exists('../data/test/'):
    os.makedirs('../data/test/')
path_test = '../data/test/'

# Random MeSH and term for testing
mesh = 'D004724'
mesh_word = 'endoscopy'

@pytest.fixture
def parse_file():
    """
    Parse the test xml file.
    """
    xml_file = GzipFile(path_test + "test.xml.gz", 'r')
    parse_file = ET.parse(xml_file)
    return parse_file

@pytest.fixture
def csv_file():
    csv_list = pp.xml_parser(path_test, path_test)
    return csv_list

@pytest.fixture
def df_nodes(csv_file):
    df_nodes = pcn.csv_to_dataframe(csv_file, type_of_df='nodes')
    return df_nodes

@pytest.fixture
def df_links(csv_file):
    df_links = pcn.csv_to_dataframe(csv_file, type_of_df='links')
    return df_links

@pytest.fixture
def graph():
    G = nx.read_gexf(path_test + 'test.gexf')
    return G


def test_get_pmid(parse_file):
    """
    Test the get_pmid function.
    It checks if the pmid is an integer and if it has the right length.
    """
    min_pmid, max_pmid = 100000, 100000000

    for node in parse_file.getroot().iter('PubmedArticle'):
        if pp.get_pmid(node) == None:
            continue
        assert type(pp.get_pmid(node)) == int
        assert min_pmid < pp.get_pmid(node) < max_pmid
    assert pp.get_pmid(parse_file.getroot()[0]) == None    
    assert pp.get_pmid(parse_file.getroot()[1]) == 36464820

def test_get_title(parse_file):
    """
    Test the get_title function.
    It checks if the title is a string and if it does not contain '\n' or '\t'.
    """
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_title(node)) == str 
        assert '\n' not in pp.get_title(node)
        assert '\t' not in pp.get_title(node)

    assert pp.get_title(parse_file.getroot()[3]) == '' 
    assert pp.get_title(parse_file.getroot()[2]) == 'Assessing implementation strategy and learning curve for transoral incisionless fundoplication as a new technique.'

def test_get_abstract(parse_file):
    """
    Test the get_abstract function.
    It checks if the abstract is a string and if it does not contain '\n' or '\t'.
    """
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_abstract(node)) == str
        assert '\n' not in pp.get_abstract(node)
        assert '\t' not in pp.get_abstract(node)

    assert pp.get_abstract(parse_file.getroot()[2]) == '      Abstract for testing.     '
    assert pp.get_abstract(parse_file.getroot()[3]) == ''

def test_validate_date():
    """
    Test the validate_date function.
    It checks if the date is in the right format.
    """
    correct_date = str('2020-01-01')
    wrong_date = str('2020-01-32')
    unordered_date = str('01-01-2020')
    wrong_format = str('2020 january 01')
    assert utils.validate_date(correct_date) == True
    assert utils.validate_date(wrong_date) == False
    assert utils.validate_date(unordered_date) == False
    assert utils.validate_date(wrong_format) == False

def test_get_publication_date(parse_file):
    """
    Test the get_publication_date function. 
    It checks if the date is a string, if it does not contain '\n' or '\t' and if it is in the right format.
    """
    for node in parse_file.getroot().iter('PubmedArticle'):
        if pp.get_publication_date(node) != '':
            continue
        assert type(pp.get_publication_date(node)) == str
        assert '\n' not in pp.get_publication_date(node)
        assert '\t' not in pp.get_publication_date(node)
        assert utils.validate_date(pp.get_publication_date(node), "%Y-%m-%d") == True

    assert pp.get_publication_date(parse_file.getroot()[1]) == '2022-10-05'

def test_get_authors(parse_file):
    """
    Test the get_authors function.
    It checks if the authors is a string and if it does not contain '\n' or '\t'.
    """
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_authors(node)) == str
        assert '\n' not in pp.get_authors(node)
        assert '\t' not in pp.get_authors(node)
    
    assert pp.get_authors(parse_file.getroot()[2]) == 'Muhammad Haseeb, Christopher C Thompson'
    assert pp.get_authors(parse_file.getroot()[6]) == ''

def test_get_journal(parse_file):
    """
    Test the get_journal function.
    It checks if the journal is a string and if it does not contain '\n' or '\t'.
    """
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_journal(node)) == str
        assert '\n' not in pp.get_journal(node)
        assert '\t' not in pp.get_journal(node)

    assert pp.get_journal(parse_file.getroot()[2]) == 'Clinical endoscopy'

def test_get_keywords(parse_file):
    """
    Test the get_keywords function.
    It checks if the keywords is a string and if it does not contain '\n' or '\t'.
    """
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_keywords(node)) == str
        assert '\n' not in pp.get_keywords(node)
        assert '\t' not in pp.get_keywords(node)
    
    assert pp.get_keywords(parse_file.getroot()[6]) == 'endoscopic submucosal dissection, endoscopy, stomach neoplasms'
    assert pp.get_keywords(parse_file.getroot()[2]) == ''

def test_get_references(parse_file):
    """
    Test the get_references function.
    It checks if the references is a string and if it does not contain '\n' or '\t'.
    """
    for node in parse_file.getroot().iter('PubmedArticle'):
        assert type(pp.get_references(node)) == str
        assert '\n' not in pp.get_references(node)
        assert '\t' not in pp.get_references(node)

    assert pp.get_references(parse_file.getroot()[2]) == '36464824'
    assert pp.get_references(parse_file.getroot()[3]) == ''


def test_xml_parser(csv_file):
    """
    Test the xml_parser function.
    It checks if the xml_parser function creates the right files.
    """
    assert os.path.exists(path_test + 'links_test.csv')
    assert os.path.exists(path_test + 'nodes_test.csv')

    with open(path_test + 'links_test.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            assert row == ['36464820\t36464821']
            break

    with open(path_test + 'nodes_test.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        next(csv_reader)
        assert next(csv_reader) == ['36464822\t\t\t2022-11-16\tSeung Woo Lee\tClinical endoscopy\t\t']          

def test_csv_to_dataframe(csv_file):
    """
    Test the csv_to_dataframe function.
    It checks if the csv_to_dataframe function creates pandas dataframes of the right shape.
    """
    df_links = pcn.csv_to_dataframe(csv_file, type_of_df='links')
    df_nodes = pcn.csv_to_dataframe(csv_file, type_of_df='nodes')

    assert type(df_links) == pd.core.frame.DataFrame
    assert type(df_nodes) == pd.core.frame.DataFrame
    assert df_links.shape[1] == 2
    assert df_nodes.shape[1] == 8

    assert df_links.iloc[0, 0] == 36464820
    assert df_links.iloc[0, 1] == 36464821
    assert df_nodes.iloc[0, 0] == 36464820
    assert df_nodes.iloc[1, 1] == 'Assessing implementation strategy and learning curve for transoral incisionless fundoplication as a new technique.'
    assert df_nodes.iloc[1, 2] == '      Abstract for testing.     '
    assert df_nodes.iloc[0, 3] == '2022-10-05'
    assert df_nodes.iloc[1, 4] == 'Muhammad Haseeb, Christopher C Thompson'
    assert df_nodes.iloc[1, 5] == 'Clinical endoscopy'
    assert df_nodes.iloc[5, 6] == 'endoscopic submucosal dissection, endoscopy, stomach neoplasms'
    assert df_nodes.iloc[1, 7] == '36464824'

    assert df_nodes.iloc[2, 1] == ''
    assert df_nodes.iloc[2, 2] == ''
    assert df_nodes.iloc[5, 4] == ''
    assert df_nodes.iloc[1, 6] == ''
    assert df_nodes.iloc[2, 7] == ''


def test_mesh_selection():
    """
    Test the mesh selection in the xml_parser function and csv_to_dataframe function.
    It checks if the xml_parser function creates the right files and if the keywords column contains the mesh_word.
    """
    csv_list = pp.xml_parser(path_test, path_test, MeSH=mesh)
    df = pcn.csv_to_dataframe(csv_list, type_of_df='nodes')

    assert os.path.exists(path_test + 'links_test.csv')
    assert os.path.exists(path_test + 'nodes_test.csv') 
    assert df['keywords'].str.contains(mesh_word).all() == True
  

def test_title_selecion():
    """
    Test the title selection. It checks the shape of the dataframe and if the title column is in the dataframe.
    """
    title = ['title']
    csv_list = pp.xml_parser(path_test, path_test, informations=title)
    title_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=title)

    assert 'title' in title_df_nodes.columns
    assert title_df_nodes.shape[1] == 3

def test_no_title_selecion():
    """
    Test the title not selection. It checks the shape of the dataframe and if the title column is not in the dataframe.
    """
    no_title = ['abstract', 'date', 'authors', 'journal', 'keywords']
    csv_list = pp.xml_parser(path_test, path_test, informations=no_title)
    no_title_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=no_title)

    assert 'title' not in no_title_df_nodes.columns
    assert no_title_df_nodes.shape[1] == 7

def test_abstract_selecion():
    """
    Test the abstract selection. It checks the shape of the dataframe and if the abstract column is in the dataframe.
    """
    abstract = ['abstract']
    csv_list = pp.xml_parser(path_test, path_test, informations=abstract)
    abstract_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=abstract)

    assert 'abstract' in abstract_df_nodes.columns
    assert abstract_df_nodes.shape[1] == 3

def test_no_abstract_selecion():
    """
    Test the abstract not selection. It checks the shape of the dataframe and if the abstract column is not in the dataframe.
    """
    no_abstract = ['title', 'date', 'authors', 'journal', 'keywords']
    csv_list = pp.xml_parser(path_test, path_test, informations=no_abstract)
    no_abstract_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=no_abstract)

    assert 'abstract' not in no_abstract_df_nodes.columns
    assert no_abstract_df_nodes.shape[1] == 7

def test_date_selecion():
    """
    Test the date selection. It checks the shape of the dataframe and if the date column is in the dataframe.
    """
    date = ['date']
    csv_list = pp.xml_parser(path_test, path_test, informations=date)
    date_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=date)

    assert 'date' in date_df_nodes.columns
    assert date_df_nodes.shape[1] == 3

def test_no_date_selecion():
    """
    Test the date not selection. It checks the shape of the dataframe and if the date column is not in the dataframe.
    """
    no_date = ['title', 'abstract', 'authors', 'journal', 'keywords']
    csv_list = pp.xml_parser(path_test, path_test, informations=no_date)
    no_date_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=no_date)

    assert 'date' not in no_date_df_nodes.columns
    assert no_date_df_nodes.shape[1] == 7

def test_authors_selecion():
    """
    Test the authors selection. It checks the shape of the dataframe and if the authors column is in the dataframe.
    """
    authors = ['authors']
    csv_list = pp.xml_parser(path_test, path_test, informations=authors)
    authors_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=authors)

    assert 'authors' in authors_df_nodes.columns
    assert authors_df_nodes.shape[1] == 3

def test_no_authors_selecion():
    """
    Test the authors not selection. It checks the shape of the dataframe and if the authors column is not in the dataframe.
    """
    no_authors = ['title', 'abstract', 'date', 'journal', 'keywords']
    csv_list = pp.xml_parser(path_test, path_test, informations=no_authors)
    no_authors_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=no_authors)

    assert 'authors' not in no_authors_df_nodes.columns
    assert no_authors_df_nodes.shape[1] == 7

def test_journal_selecion():
    """
    Test the journal selection. It checks the shape of the dataframe and if the journal column is in the dataframe.
    """
    journal = ['journal']
    csv_list = pp.xml_parser(path_test, path_test, informations=journal)
    journal_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=journal)

    assert 'journal' in journal_df_nodes.columns
    assert journal_df_nodes.shape[1] == 3

def test_no_journal_selecion():
    """
    Test the journal not selection. It checks the shape of the dataframe and if the journal column is not in the dataframe.
    """
    no_journal = ['title', 'abstract', 'date', 'authors', 'keywords']
    csv_list = pp.xml_parser(path_test, path_test, informations=no_journal)
    no_journal_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=no_journal)

    assert 'journal' not in no_journal_df_nodes.columns
    assert no_journal_df_nodes.shape[1] == 7

def test_keywords_selecion():
    """
    Test the keywords selection. It checks the shape of the dataframe and if the keywords column is in the dataframe.
    """
    keywords = ['keywords']
    csv_list = pp.xml_parser(path_test, path_test, informations=keywords)
    keywords_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=keywords)

    assert 'keywords' in keywords_df_nodes.columns
    assert keywords_df_nodes.shape[1] == 3

def test_no_keywords_selecion():
    """
    Test the keywords not selection. It checks the shape of the dataframe and if the keywords column is not in the dataframe.
    """
    no_keywords = ['title', 'abstract', 'date', 'authors', 'journal']
    csv_list = pp.xml_parser(path_test, path_test, informations=no_keywords)
    no_keywords_df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=no_keywords)

    assert 'keywords' not in no_keywords_df_nodes.columns
    assert no_keywords_df_nodes.shape[1] == 7

def test_all_selecion(df_nodes):
    """
    Test the all selection. It checks the shape of the dataframe and if all the columns are in the dataframe.
    """
    info = ['title', 'abstract', 'date', 'authors', 'journal', 'keywords']

    for column in info:
        assert column in df_nodes.columns
    
    assert df_nodes.shape[1] == 8

def test_no_selecion():
    """
    Test the no selection. It checks the shape of the dataframe.
    """
    no_info = []
    csv_list = pp.xml_parser(path_test, path_test, informations=no_info)
    df_nodes = pcn.csv_to_dataframe(csv_list, type_of_df='nodes', columns=no_info)

    assert df_nodes.shape[1] == 2  


def test_is_empty_csv():
    """
    Test the is_empty_csv function.
    """
    assert utils.is_empty_csv(path_test + 'test_empty.csv') == True
    assert utils.is_empty_csv(path_test + 'test_not_empty.csv') == False


def test_df_to_graph(df_links, df_nodes):
    """
    Test the df_to_graph function.
    It checks if the df_to_graph function creates a networkx graph.
    """
    graph = pcn.df_to_graph(df_links, df_nodes)

    assert type(graph) == nx.classes.digraph.DiGraph

def test_connected_graph_selection(df_links, df_nodes):
    """
    Test the connected graph selection of the df_to_graph function.
    """
    graph_connected = pcn.df_to_graph(df_links, df_nodes, connected_graph=True)
    graph_not_connected = pcn.df_to_graph(df_links, df_nodes, connected_graph=False)
    
    assert nx.is_weakly_connected(graph_connected) == True
    assert nx.is_weakly_connected(graph_not_connected) == False
    assert len(graph_connected.nodes()) <= len(graph_not_connected.nodes())

def test_unknown_nodes_selection(df_links, df_nodes):
    """
    Test the unknown nodes selection of the df_to_graph function.
    It checks if the graph with unknown nodes has more nodes than the graph without unknown nodes.
    It also checks if the nodes in the graph without unknown nodes have no empty attributes.   
    """
    graph_unknown_nodes = pcn.df_to_graph(df_links, df_nodes, connected_graph=False, unknown_nodes=True)
    graph_no_unknown_nodes = pcn.df_to_graph(df_links, df_nodes, connected_graph=False, unknown_nodes=False)
    
    assert len(graph_unknown_nodes.nodes()) >= len(graph_no_unknown_nodes.nodes())

    for node in list(graph_no_unknown_nodes.nodes(data=True)):
        assert node[1] != {}

def test_connect_graph(df_links, df_nodes):
    """
    Test the connect_graph function.
    It checks if the connect_graph function creates a connected graph.
    """
    edge_list = [(36464820, 36464821), (36464820, 36464824), (36464821, 36464824), (36464825, 36464821), (36464825, 36464828)]
    G = pcn.df_to_graph(df_links, df_nodes, connected_graph=False, unknown_nodes=True)
    G_connected = pcn.connect_graph(G)

    assert nx.is_weakly_connected(G) == False
    assert nx.is_weakly_connected(G_connected) == True
    assert list(G_connected.edges(data=False)) == edge_list

def test_add_attributes(df_links, df_nodes):
    """
    Test the add_attributes function.
    It checks if the add_attributes function adds the attributes to the nodes.
    """
    G = pcn.df_to_graph(df_links, df_nodes, connected_graph=False, unknown_nodes=True)
    G = pcn.add_attributes(G, df_nodes)

    assert G.nodes[36464821]['title'] == 'Assessing implementation strategy and learning curve for transoral incisionless fundoplication as a new technique.'
    assert G.nodes[36464821]['abstract'] == '      Abstract for testing.     '
    assert G.nodes[36464820]['date'] == '2022-10-05'
    assert G.nodes[36464821]['authors'] == 'Muhammad Haseeb, Christopher C Thompson'
    assert G.nodes[36464821]['journal'] == 'Clinical endoscopy'
    assert G.nodes[36464825]['keywords'] == 'endoscopic submucosal dissection, endoscopy, stomach neoplasms'
    assert G.nodes[36464821]['references'] == '36464824'

    assert G.nodes[36464822]['title'] == ''
    assert G.nodes[36464822]['abstract'] == ''
    assert G.nodes[36464825]['authors'] == ''
    assert G.nodes[36464821]['keywords'] == ''
    assert G.nodes[36464822]['references'] == ''

    # assert all the attributes of the nodes 36464827 and 36464828 are empty
    for node in G.nodes(data=True):
        if node[0] == 36464827 or node[0] == 36464828:
            assert node[1] == {}


def test_nodes_to_df(graph):
    """
    Test the nodes_to_df function. 
    It checks if the nodes_to_df function creates a pandas dataframe of the right shape.
    It also checks if the first column is 'pmid'.
    """
    df_nodes_graph = pcn.nodes_to_df(graph)

    assert type(df_nodes_graph) == pd.core.frame.DataFrame
    assert df_nodes_graph.shape[1] == 8
    assert df_nodes_graph.columns[0] == 'pmid'
    
    # order the rows by the pmid column to check specific values
    df_nodes_graph = df_nodes_graph.sort_values(by=['pmid'])

    assert df_nodes_graph.iloc[0, 0] == '36464820'
    assert df_nodes_graph.iloc[1, 1] == 'Assessing implementation strategy and learning curve for transoral incisionless fundoplication as a new technique.'
    assert df_nodes_graph.iloc[1, 2] == '      Abstract for testing.     '
    assert df_nodes_graph.iloc[0, 3] == '2022-10-05'
    assert df_nodes_graph.iloc[1, 4] == 'Muhammad Haseeb, Christopher C Thompson'
    assert df_nodes_graph.iloc[1, 5] == 'Clinical endoscopy'
    assert df_nodes_graph.iloc[5, 6] == 'endoscopic submucosal dissection, endoscopy, stomach neoplasms'
    assert df_nodes_graph.iloc[1, 7] == '36464824'

    assert df_nodes_graph.iloc[2, 1] == ''
    assert df_nodes_graph.iloc[2, 2] == ''
    assert df_nodes_graph.iloc[5, 4] == ''
    assert df_nodes_graph.iloc[1, 6] == ''
    assert df_nodes_graph.iloc[2, 7] == ''

def test_links_to_df(graph):
    """
    Test the links_to_df function.
    It checks if the links_to_df function creates a pandas dataframe of the right shape.
    It also checks if the first column is 'source' and the second column is 'target'.
    """
    df_links_graph = pcn.links_to_df(graph)

    assert type(df_links_graph) == pd.core.frame.DataFrame
    assert df_links_graph.shape[1] == 2
    assert df_links_graph.columns[0] == 'source'
    assert df_links_graph.columns[1] == 'target'

    assert df_links_graph.iloc[0, 0] == '36464820'
    assert df_links_graph.iloc[0, 1] == '36464821'
