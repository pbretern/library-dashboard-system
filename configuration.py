#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Set the global pathes in the project.

"""
import os


# absolute path for project folder
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# path for the import folders
DIRPATH_IMP = 'data/import_folders'
# path for the storage folders
STOR_DIRPATH = 'data/storage_folders/'


# path to each file for importing the data
UMSATZ_IMP = 'umsatz'  # umsatz
BUDGET_IMP = 'budget'  # budget

# for further paths (example)
# NEWACQ_IMP = '...' # example


# path to each file for storage and loading the data
UMSATZ_STOR = 'umsatz/umsatz_total.csv'  # umsatz
BUDGET_STOR = 'budget/budget_total.csv'  # budget

# for further files (example)
# NEWACQ_STOR = '...'

# Helper files for preparing the data during import and preparation
# FILE_LIEF = '...'

# Path to the import folders
FILEPATH_UMSATZ_IMP = os.path.join(PROJECT_ROOT, DIRPATH_IMP, UMSATZ_IMP)
FILEPATH_BUDGET_IMP = os.path.join(PROJECT_ROOT, DIRPATH_IMP, BUDGET_IMP)

# for further paths (example)
# FILEPATH_NEWACQ_IMP = os.path.join(...)

# Path to the storage files
FILEPATH_UMSATZ_STOR = os.path.join(PROJECT_ROOT, STOR_DIRPATH, UMSATZ_STOR)
FILEPATH_BUDGET_STOR = os.path.join(PROJECT_ROOT, STOR_DIRPATH, BUDGET_STOR)

# for further paths (example)
# FILEPATH_NEWACQ_STOR = os.path.join(...)

# Path to the helper files if necessary ... (example)
# HELPER_FILE_LIEF = os.path.join(...)
