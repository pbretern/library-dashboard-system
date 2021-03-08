#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This script makes the import of the umsatz data. It contains one function
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

from configuration import FILEPATH_UMSATZ_IMP, FILEPATH_UMSATZ_STOR, HELPER_FILE_LIEF



def main():
    """Makes the import happened.
    Following methods will be applied:
        filename_format_corr() from cls FilenameValidation.
        load_txt_to_df(skiprows=5, skipfooter=3) from cls FileImport.
        remove_rows_with_special_char() from cls CleanPreProcDf.
        remove_whitespaces_col_headers() from cls CleanPreProcDf.
        create_new_column_by_dict_value(col_name_map_new='Lieferant Abk.',
            col_name_map='Lieferant',filename=HELPER_FILE_LIEF) from cls CleanPreProcDf.
        add_df_existing_csv_file() or create_new_csv_file_df() from cls SaveDfToCSV.
    """
    h = FilenameValidation(FILEPATH_UMSATZ_IMP).filename_format_corr()


    i = FileImport(h).load_txt_to_df(skiprows=5, skipfooter=3)

    j = CleanPreProcDf(i).remove_rows_with_special_char()

    k = CleanPreProcDf(j).remove_whitespaces_col_headers()
    
    k = CleanPreProcDf(k).create_new_column_by_dict_value(
        col_name_map_new='Lieferant Abk.', col_name_map='Lieferant',
        filename=HELPER_FILE_LIEF)

    if os.path.exists(FILEPATH_UMSATZ_STOR):
        l = SaveDfToCSV(FILEPATH_UMSATZ_STOR, k).add_df_existing_csv_file()
    else:
        m = SaveDfToCSV(FILEPATH_UMSATZ_STOR, k).create_new_csv_file_df()

    print('Der Import wurde erfolgreich durchgeführt.')


if __name__ == '__main__':
    main()
