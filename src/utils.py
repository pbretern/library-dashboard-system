#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" These module contains functions which do not affect objects (self). Nevertheless
they will be needed for doing some basic jobs, e.g. making a dict from file, making a
list of from file. Find below a list of functions within this module. They will be
used in data_import and data_prep.

    read_csv_file_in_dict(file, col_headers=None):
    read_txt_file_in_list(file):
    transform_actual_month():
    get_dates_list(start_date='2014-12-31'):
"""
# datetime func
from datetime import datetime
# pandas func
import pandas as pd


def read_csv_file_in_dict(file, col_headers=None):
    """converts a two column csv file in dictionary using pandas library,
    especially .to_dict()

    Parameters
    ----------
    file : str
        the name of the file.
    col_headers : list, optional
        the two columns, by default None

    Returns
    -------
    dic:
        with key value from the two columns.
    """
    df = pd.read_csv(file)
    df_dict = {}
    if col_headers:
        df_dict = df.set_index(col_headers[0])[col_headers[1]].to_dict()

    df_dict = df.set_index(df.columns[0])[df.columns[1]].to_dict()

    return df_dict


def read_txt_file_in_list(file):
    """Returns a list from a txt file

    Returns
    -------
    list:
        contains elements from a txt file
    """
    lines = []
    with open(file, 'r') as f:
        lines = f.read().splitlines()

    return lines

def transform_actual_month():
    """Transforms the actual date into a format '%Y-%m-%d'.

    Returns
    -------
    str:
        which contains the date format
    """
    # calculates the actual month in format '%Y-%m-%d'
    # get actual date
    actual_date = datetime.today()

    if not actual_date.month == 12:
        actual_date = actual_date.replace(day=1)
    else:
        actual_date = actual_date.replace(day=31)

    # strftime() method returns a string representing date and time
    actual_date = actual_date.strftime('%Y-%m-%d')

    return actual_date


# function
def get_dates_list(start_date='2014-12-01'):
    """Returns a list of specific dates backwards to the start date.
    Those dates shows the last day of a year in '%Y-%m-%d' in str format, e.g.
    '2014-12-31'.


    Parameters
    ----------
    start_date : str, optional
        [description], by default '2014-12-01'

    Returns
    -------
    list:
        with strings containing YYYY-m-dd format
    """
    temp_list_dates = []
    list_dates = []
    end_date = transform_actual_month()
    # temp_list_dates = pd.date_range(start_date, end_date, freq='y')
    temp_list_dates = pd.date_range(start_date, end_date, freq='AS-DEC')
    list_dates = temp_list_dates.to_native_types().tolist()
    # set func verwenden
    if end_date not in list_dates:
        list_dates.append(end_date)

    return list_dates


def date_from_filename(filename):
    """Change string from filename into date string for latter column in dataframe.

    Parameters
    ----------
    filename : str
        file with the date in special format ('%Y_%m_%d')

    Returns
    -------
    str:
        the date in a special format
    """
    # extract date from filename and added as a new column to dataframe
    date_from_file = filename.split('/')[-1].split('.')[0]
    date_from_file = datetime.strptime(
        str(date_from_file), '%Y_%m_%d').date()  # format colname als parameter

    return date_from_file


if __name__ == '__main__':
    print(transform_actual_month())
    print(get_dates_list('2014-12-01'))
