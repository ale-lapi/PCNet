#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

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