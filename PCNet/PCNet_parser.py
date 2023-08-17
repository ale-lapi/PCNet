#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm
from gzip import GzipFile
import xml.etree.ElementTree as ET

__author__ = "Alessandro Lapi"
__email__ = "alessandro.lapi@studio.unibo.it"



def sanitize_text(text):
    """
    Sanitize the text from the xml file to avoid problems with the csv file

    Parameters
    ----------
    text : str
        Text to sanitize

    Returns
    -------
    text : str
        Sanitized text
    """
    # clean the text from the brackets and the newlines and tabs to avoid problems with the csv file
    text = text.replace('[','')
    text = text.replace(']','')
    text = text.replace('\n',' ')
    text = text.replace('\t',' ')
    text = text.replace('  ',' ')
    text = text.replace('&lt;b&gt;',' ')
    text = text.replace('&lt;/b&gt;',' ')
    text = text.replace('&lt;br&gt;',' ')
    text = text.replace('&lt;sup&gt;',' ')
    text = text.replace('&quot;',' ')
    text = text.replace('&lt;/sup&gt;',' ')
    text = text.replace('&lt;/br&gt;&lt;/br&gt;',' ')


    return text


def get_pmid(node):
    """
    While parsing the xml file, return the pmid of the article corresponding to the node
    
    Parameters
    ----------
    node : int
        Node of the parsed xml file
        
    Returns
    -------
    pmid : int
        pmid of the article corresponding to the node
    """
    # pmid_min and pmid_max to check if the pmid is in the correct format
    pmid_min, pmid_max = 100000, 100000000

    pmid = node.find("./PubmedData/ArticleIdList/ArticleId[@IdType='pubmed']").text

    if pmid is not None:
        pmid = int(pmid)
    
        # Set pmid to 0 if it is not in the correct format to exclude the article from the parse
        if pmid < pmid_min or pmid > pmid_max:
            pmid = None     

    return pmid

def get_title(node):
    """
    While parsing the xml file, return the title of the article corresponding to the node
    
    Parameters
    ----------
    node : int
        Node of the parsed xml file
        
    Returns
    -------
    title : str
        Title of the article corresponding to the node
    """
    for child in node.iter('ArticleTitle'):
        title = "".join(child.itertext())

        title = sanitize_text(title)

    return title
    
def get_abstract(node):
    """
    While parsing the xml file, return the abstract of the article corresponding to the node

    Parameters
    ----------
    node : int
        Node of the parsed xml file
        
    Returns
    -------
    abstract : str
        Abstract of the article corresponding to the node
    """
    abstract = ""

    for child in node.iter('Abstract'):
        if child.text is not None:
            abstract = "".join(child.itertext())

            abstract = sanitize_text(abstract)
    return abstract

def get_publication_date(node):
    """
    While parsing the xml file, return the publication date of the article corresponding to the node
    
    Parameters
    ----------
    node : int
        Node of the parsed xml file
        
    Returns
    -------
    date : str
        Publication date of the article corresponding to the node
    """
    def get_date(child):
        """
        Get the date from the child node
        """
        year = child.find('Year').text
        month = child.find('Month').text
        day = child.find('Day').text
        date = year + '-' + month + '-' + day
        return date

    date = ""

    # Get the date of the publication. It is extracted according to the availability,
    # following this priority: electronic, revised, accepted.
    for child in node.iter('PubMedPubDate'):
        if child.attrib['PubStatus'] == 'accepted':
            date = get_date(child)
    
    for child in node.iter('DateRevised'):
        date = get_date(child)

    for child in node.iter('ArticleDate'):
        if child.attrib['DateType'] == 'Electronic':
            date = get_date(child)

    return date

def get_authors(node):
    """
    While parsing the xml file, return the authors of the article corresponding to the node
    
    Parameters
    ----------
    node : int
        Node of the parsed xml file
        
    Returns
    -------
    authors : str
        Authors of the article corresponding to the node
    """
    authors = []

    for child in node.iter('Author'):

        if child.find('LastName') is not None:   
            lastname = child.find('LastName').text
        else:
            lastname = ''

        if child.find('ForeName') is not None:
            forename = child.find('ForeName').text
        elif child.find('Initials') is not None:
                forename = child.find('Initials').text
        else:
            forename = ''

        if lastname != '' and forename != '':
            authors.append(forename + ' ' + lastname + ', ')

    # clean the authors from newlines and tabs to avoid problems with the csv file
    if len(authors) > 0:
        authors[-1] = authors[-1][:-2]
        authors = ''.join(authors)
        
        authors = sanitize_text(authors)
    else:
        authors = ""

    return authors

def get_journal(node):
    """
    While parsing the xml file, return the journal of the article corresponding to the node
    
    Parameters
    ----------
    node : int
        Node of the parsed xml file
        
    Returns
    -------
    journal : str
        Journal of the article corresponding to the node
    """
    journal = node.find("./MedlineCitation/Article/Journal/Title").text

    journal = sanitize_text(journal)

    return journal

def get_keywords(node):
    """
    While parsing the xml file, return the keywords of the article corresponding to the node
    
    Parameters
    ----------
    node : int
        Node of the parsed xml file
        
    Returns
    -------
    keywords : str
        Keywords of the article corresponding to the node
    """
    keywords = []

    # get the keywords from keywords tag
    for child in node.iter('Keyword'):
        if child.text is not None:
            key = child.text

            # clean the keywords from newlines and tabs to avoid problems with the csv file
            key = sanitize_text(key)
            keywords.append(key + ', ')

    # get the keywords from the MeSH tag
    for child in node.iter('DescriptorName'):
        key = child.text

        # clean the keywords from newlines and tabs to avoid problems with the csv file
        key = sanitize_text(key)
        keywords.append(key + ', ')

    if len(keywords) > 0:
        keywords[-1] = keywords[-1][:-2]
        keywords = ''.join(keywords)
    else:
        keywords = ""

    # make all the letters lowercase to have less duplicates
    keywords = keywords.lower()

    # remove repeated words
    keywords = keywords.split()
    keywords = list(dict.fromkeys(keywords))
    keywords = ' '.join(keywords)

    return keywords

def get_references(node):
    """
    While parsing the xml file, return the references of the article corresponding to the node
    
    Parameters
    ----------
    node : int
        Node of the parsed xml file
        
    Returns
    -------
    references : str
        References of the article corresponding to the node
    """
    references = []
    ref = ""
    for child in node.iter('Reference'):
        for item in child.iter("ArticleId"):
            if item.attrib.get("IdType") == "pubmed":
                ref = item.text

                # check if the reference is in the correct format
                if ref is not None and 5 < len(ref) < 9:
                    references.append(ref + ', ')


    if len(references) > 0:
       
        references[-1] = references[-1][:-2]
        references = ''.join(references)
        
    else:
        references = ""

    return references


def xml_parser(path_xml, path_csv, MeSH="", informations = ['title', 
                                                   'abstract',
                                                   'date', 
                                                   'authors', 
                                                   'journal',
                                                   'keywords'] 
                                                   ):
    """
    Parse the xml files and store information of the links and the nodes in csv files. 
    Each xml file will have its own csv files.
    The structure of the csv files is the following:
    - links: PMID of the article, PMID of the reference
    - nodes: PMID of the article, informations, references; where informations are the informations chosen by the user.

    Parameters
    ----------
    path_xml : str
        Path of the xml.gz files
    path_csv : str
        Path where we want to save the .csv files
    MeSH : str
        Mesh corresponding to the area of interest.
        Default is "", which means that the parse is performed over all the articles.
    informations : list
        List of the informations we want to get from the xml files. 
        Default is ['title', 'abstract', 'date', 'authors', 'journal', 'keywords'].
        If you need less information you can specify it in the list, keeping the same name.
        For example, if you want only the title and the abstract, you can write:
        informations = ['title', 'abstract'].
        Note: the order of the informations in the list is important.
        
    Returns
    -------
    None
    """
    
    def get_info(node, net_nodes, net_links, informations):
        """
        Get the information from the xml file.
        """
        # Extract the pmid
        pmid = get_pmid(node)
        net_nodes.write(f"{pmid}\t")

        # If the pmid is not in the correct format, we skip the article
        if pmid is not None:
            
            # Extract the informations selected
            if 'title' in informations:
                title = get_title(node)
                net_nodes.write(f"{title} \t")
            
            if 'abstract' in informations:
                abstract = get_abstract(node)
                net_nodes.write(f"{abstract} \t")
            
            if 'date' in informations:
                date = get_publication_date(node)
                net_nodes.write(f"{date}\t")
            
            if 'authors' in informations:
                authors = get_authors(node)
                net_nodes.write(f"{authors} \t")
            
            if 'journal' in informations:
                journal = get_journal(node)
                net_nodes.write(f"{journal} \t")
            
            if 'keywords' in informations:
                keywords = get_keywords(node)
                net_nodes.write(f"{keywords}\t")

            # Extract the references
            references = get_references(node)
            net_nodes.write(f"{references}")

            net_nodes.write("\n")

            # Write the links in the links csv file 
            if references != "":
            
                for ref in references.split(', '): 
                    net_links.write(f"{pmid}\t{ref}\n")



    for file in tqdm([file for file in os.listdir(path_xml) if file.endswith('.gz')], desc='- Processing xml files ...'):
        
        # Unzip the xml.gz file and parse it
        xml_file = GzipFile(path_xml + file, 'r')
        parse_file = ET.parse(xml_file)

        # Create 2 csv files for the links and the nodes
        with open(path_csv + "links_" + file + ".csv", "w", encoding='utf-8') as net_links:
            with open(path_csv + "nodes_" + file + ".csv", "w", encoding='utf-8') as net_nodes:
                
                # Loop over the nodes of the xml file, i.e. the articles
                for node in parse_file.getroot().iter('PubmedArticle'):

                    if MeSH != "":

                        # Apply the MeSH filter selected
                        for child in node.iter('DescriptorName'):
                            if child.attrib['UI'] == MeSH:
                                get_info(node, net_nodes, net_links, informations)

                    else:
                        get_info(node, net_nodes, net_links, informations)

                    