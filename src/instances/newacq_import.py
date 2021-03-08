#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This script makes the import of the new acquisition data. It contains one function
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

from configuration import FILEPATH_NEWACQ_IMP, FILEPATH_NEWACQ_STOR, FILEPATH_HELPER_RVK


def main():
    """Makes the import happened.
    Following methods will be applied:
        filename_format_corr() from cls FilenameValidation.
        load_tsv_to_df() from cls FileImport.
        remove_rows_with_special_char() from cls CleanPreProcDf
        remove_whitespaces_col_headers() from cls CleanPreProcDf
        2 x create_new_column_for_rvk_benennung() from cls CleanPreProcDf
        add_df_existing_csv_file() or create_new_csv_file_df() from cls SaveDfToCSV
    """
    h = FilenameValidation(FILEPATH_NEWACQ_IMP).filename_format_corr()

    i = FileImport(h).load_tsv_to_df()

    i = CleanPreProcDf(i).remove_rows_with_special_char()

    i = CleanPreProcDf(i).remove_whitespaces_col_headers()
    
    i = CleanPreProcDf(i).setting_value_column(col_name_set='Ex', value_set=1)

    i = CleanPreProcDf(i).create_new_column_for_rvk_benennung(
        'Signatur', 'Systematikstelle', 'RVK-Bez-SysStelle',
        FILEPATH_HELPER_RVK, r'([A-Z]{1,2}\s\d{2,5})')

    i = CleanPreProcDf(i).create_new_column_for_rvk_benennung(
        'Signatur', 'Systematikgruppe', 'RVK-Bez-SysGruppe',
        FILEPATH_HELPER_RVK, r'(^[A-Z]{1,2})')

    if os.path.exists(FILEPATH_NEWACQ_STOR):
        i = SaveDfToCSV(FILEPATH_NEWACQ_STOR, i).add_df_existing_csv_file()
    else:
        i = SaveDfToCSV(FILEPATH_NEWACQ_STOR, i).create_new_csv_file_df()

    print('Der Import wurde erfolgreich durchgeführt.')

if __name__ == '__main__':
    main()
