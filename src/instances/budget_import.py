#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This script makes the import of the budget data. It contains one function
which makes the import and will be executed. It's based on the module data_import
and it's classes:
    FilenameValidation,
    FileImport,
    CleanPreProcDf,
    SaveDfToCSV
Necessary file/path/directory are defined in the configuration.py.
"""

import os
from src.data_import import FilenameValidation, FileImport, CleanPreProcDf, SaveDfToCSV

from configuration import FILEPATH_BUDGET_IMP, FILEPATH_BUDGET_STOR, HELPER_FILE_KOST


def main():
    """Makes the import happened.
    Following methods will be applied:
        filename_format_corr() from cls FilenameValidation.
        load_txt_to_df(skiprows=6, skipfooter=3) from cls FileImport.
        remove_rows_with_special_char() from cls CleanPreProcDf
        remove_whitespaces_col_headers() from cls CleanPreProcDf
        create_new_column_by_dict_value() from cls CleanPreProcDf
        add_df_existing_csv_file() or create_new_csv_file_df() from cls SaveDfToCSV
    """
    d = FilenameValidation(FILEPATH_BUDGET_IMP).filename_format_corr()

    e = FileImport(d).load_txt_to_df(skiprows=6, skipfooter=3)

    g = CleanPreProcDf(e).remove_rows_with_special_char()

    h = CleanPreProcDf(g).remove_whitespaces_col_headers()

    h = CleanPreProcDf(h).create_new_column_by_dict_value(
        col_name_map_new='Bezeichnung', col_name_map='S Bezeichnung',
        filename=HELPER_FILE_KOST)

    if os.path.exists(FILEPATH_BUDGET_STOR):
        f = SaveDfToCSV(FILEPATH_BUDGET_STOR, h).add_df_existing_csv_file()
    else:
        f = SaveDfToCSV(FILEPATH_BUDGET_STOR, h).create_new_csv_file_df()

    print('Der Import wurde erfolgreich durchgeführt.')
    
if __name__ == '__main__':
    main()
