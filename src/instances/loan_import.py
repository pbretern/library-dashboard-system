#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This script makes the import of the loan data. It contains one function
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

from configuration import FILEPATH_LOAN_IMP, FILEPATH_LOAN_STOR, FILEPATH_HELPER_RVK


def main():
    """Makes the import happened.
    Following methods will be applied:
        filename_format_corr() from cls FilenameValidation.
        load_excel_to_df() from cls FileImport.
        2 x create_new_column_for_rvk_benennung() from cls CleanPreProcDf.
        create_new_column_for_rvk_benennung() from cls CleanPreProcDf.
        fill_rows_value_by_column() from cls CleanPreProcDf.
        add_df_existing_csv_file() or create_new_csv_file_df() from cls SaveDfToCSV.
    """
    h = FilenameValidation(FILEPATH_LOAN_IMP).filename_format_corr()

    i = FileImport(h).load_excel_to_df(sheet_name=2, ignore_index=True)

    i = CleanPreProcDf(i).create_new_column_for_rvk_benennung(
        'shelfmark', 'Systematikstelle', 'RVK-Bez-SysStelle',
        FILEPATH_HELPER_RVK, r'([A-Z]{1,2}\s\d{2,5})')

    i = CleanPreProcDf(i).create_new_column_for_rvk_benennung(
        'shelfmark', 'Systematikgruppe', 'RVK-Bez-SysGruppe',
        FILEPATH_HELPER_RVK, r'(^[A-Z]{1,2})')

    i = CleanPreProcDf(i).fill_rows_value_by_column(
        'shelfmark', '099', 'Systematikgruppe', 'Buchservice')

    i = CleanPreProcDf(i).precalc_column(
        'cum_loans', 'Systematikgruppe', 'Buchservice')

    if os.path.exists(FILEPATH_LOAN_STOR):
        i = SaveDfToCSV(FILEPATH_LOAN_STOR,
                        i).add_df_existing_csv_file()
    else:
        i = SaveDfToCSV(FILEPATH_LOAN_STOR,
                        i).create_new_csv_file_df()

    print('Der Import wurde erfolgreich durchgeführt.')


if __name__ == '__main__':
    main()
