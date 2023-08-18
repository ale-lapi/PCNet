#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import csv

__author__ = "Alessandro Lapi"
__email__ = "alessandro.lapi@studio.unibo.it"


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
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
    
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

