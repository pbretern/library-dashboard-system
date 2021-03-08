#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This script makes the import of the readingrooms data. It contains one function
which makes the import and will be executed. It's based on the module data_import
and it's classes:
    FilenameValidation,
    FileImport,
    SaveDfToCSV
Necessary file/path/directory are defined in the configuration.py.
"""

import os
from src.data_import import FilenameValidation, FileImport, SaveDfToCSV

from configuration import FILEPATH_READING_IMP, FILEPATH_READING_STOR


def main():
    """Makes the import happened.
    Following methods will be applied:
        filename_format_corr() from cls FilenameValidation.
        load_excel_to_df() from cls FileImport.
        add_df_existing_csv_file() or create_new_csv_file_df() from cls SaveDfToCSV
    """
    h = FilenameValidation(FILEPATH_READING_IMP).filename_format_corr()

    i = FileImport(h).load_excel_to_df()

    if os.path.exists(FILEPATH_READING_STOR):
        i = SaveDfToCSV(FILEPATH_READING_STOR, i).add_df_existing_csv_file()
    else:
        i = SaveDfToCSV(FILEPATH_READING_STOR, i).create_new_csv_file_df()

    print('Der Import wurde erfolgreich durchgeführt.')
    
if __name__ == '__main__':
    main()
