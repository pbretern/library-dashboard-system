#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module imports (automatically) files in e.g.
txt, csv... formats into the right format to work on.
It includes the following classes:
    FilenameValidation
    FileImport
    SaveDfToCSV
    CleanPreProcDf

"""
# os func
import os
# regex func
import re
# pandas func
import pandas as pd

from src.utils import read_csv_file_in_dict, date_from_filename


class FilenameValidation:
    """This class checks if the files exist and if they are in the correct
    filename format for the import. The class also checks the existence of the directory.

    Attributes
    ----------

    dir_name : str
    _root : str
    _ext = str
    _match = str
    _file_list : list
    _file_list_corr : list

    Class Attributes
    ---------------
    file_ext : list
    filename_format : regex


    Methods
    -------
    check_dir(self)
    check_files_exist(self)
    filename_format_corr(self)



    """
    # a list with file extension
    file_ext = ['.csv', '.tsv', '.txt', '.xls', '.xlsx']
    # regex for the filename format
    filename_format = r'((\d{4})(\_)(\d{2})_(\d{2}))'

    def __init__(self, dir_name):
        """Inits FilenameValidation with some attributes which will be needed by
        other methods in this class.

        Parameters
        ----------
        dir_name : str
            the name of the directory on which will be worked in the other methods.

        Attributes
        ----------
        dir_name : str
        _root : str
        _ext = str
        _match = str
        _file_list : list
        _file_list_corr : list

        """

        self.dir_name = dir_name
        self._root = None
        self._ext = None
        self._match = None
        self._file_list = self.check_files_exist()
        self._file_list_corr = []

    def check_dir(self):
        """checks if dir exists

        Returns
        -------
        str:
            if directory exists.

        Raises
        ------
        FileNotFoundError:
            if directory does not exists.
        """
        # check if directory not exists
        if not os.path.exists(self.dir_name):
            raise FileNotFoundError('The directory does not exist.')
        # returning dir exists
        return 'There is such directory like {}'.format(self.dir_name)

    def check_files_exist(self):
        """Checks if directory is not empty. If not returns a list with
        all the possible files.

        Returns
        -------
        list:
            with all filenames in the directory.

        Raises
        ------
        FileNotFoundError:
           if the directory is empty.
        """
        # checks if folder are empty
        if not os.listdir(self.dir_name):
            raise FileNotFoundError('There are any file(s) to import.')

        # if not returning a list with filenames
        self._file_list = [f for f in os.listdir(
            self.dir_name) if os.path.isfile(os.path.join(self.dir_name, f))]

        print('The directory {0} contains {1} files: {2}'.format(
            self.dir_name, len(self._file_list), self._file_list))

        return self._file_list

    def filename_format_corr(self):
        """Checks if the formats of the files are correct depending on a list
        with extensions and on a regex expression.

        Returns
        -------
        list:
            contains the filenames with correct format
        """
        for f in self._file_list:
            self._root, self._ext = os.path.splitext(f)
            self._match = re.search(self.filename_format, self._root)

            if self._ext in self.file_ext and self._match:
                i = os.path.join(self.dir_name, f)
                self._file_list_corr.append(i)

        print('Following file(s) are ready to import: {}.'.format(
            self._file_list_corr))

        return self._file_list_corr


class FileImport:
    """Imports the file(s) with correct file format to dataframes and
    get the date from the filename (only available in txt and tsv methods).

    Attributes
    ----------

    file_list : list
    _df : dataframe
    _help_df = dataframe

    Methods
    -------
    load_txt_to_df(self, skiprows=0, skipfooter=0, encoding='utf-8')
    load_tsv_to_df(self, skiprows=0, skipfooter=0, encoding='utf-8')
    load_excel_to_df(self,sheet_name=None, ignore_index=True)


    """

    def __init__(self, file_list=None):
        """Inits FileImport with:

        Parameters
        ----------
        file_list : list, optional
            list of filenames, by default None

        Attributes
        ----------
        _df : dataframe, private
        _help_df : dataframe, private

        """
        self.file_list = file_list
        self._df = pd.DataFrame()
        self._help_df = pd.DataFrame()

    def load_txt_to_df(self, skiprows=0, skipfooter=0, encoding='utf-8'):
        """Load the txt.files to dataframe.

        Parameters
        ----------
        skiprows : int, optional
            for skipping rows at the same time as importing files, by default 5
        skipfooter : int, optional
            for skipping foot rows at the same time as importing Files, by default 3
        encoding : str, optional
            character-encoding at the same time as importing Files, by default 'utf-8'

        Returns
        -------
       dataframe:
            the data from the files
        """

        for f in self.file_list:
            self._df = pd.read_fwf(f, skiprows=skiprows,
                                   skipfooter=skipfooter, encoding=encoding)
            self._df['Datum'] = date_from_filename(f)
            self._help_df = pd.concat([self._help_df, self._df])

        self._df = self._help_df
        return self._df

    def load_tsv_to_df(self, skiprows=0, skipfooter=0, encoding='utf-8'):
        """Load the tsv.files to dataframe.

        Parameters
        ----------
        skiprows : int, optional
            for skipping rows at the same time as importing files, by default 0
        skipfooter : int, optional
            for skipping foot rows at the same time as importing Files, by default 0
        encoding : str, optional
            character-encoding at the same time as importing Files, by default 'utf-8'

        Returns
        -------
       dataframe:
            the data from the files.
        """

        for f in self.file_list:
            self._df = pd.read_csv(f, encoding=encoding, skiprows=skiprows, skipfooter=skipfooter,
                                   engine='python', sep=r'\t')

            self._df['Datum'] = date_from_filename(f)
            self._help_df = pd.concat([self._help_df, self._df])

        self._df = self._help_df

        return self._df

    def load_excel_to_df(self, sheet_name=None, ignore_index=True):
        """Loads the excel file to dataframe.

        Parameters
        ----------
        sheet_name : str, int, list, or None, optional
            how many sheets will be imported, by default None = all
        ignore_index : bool, optional
            ignore index, by default True

        dataframe:
            the data from the files.

        """
        for f in self.file_list:
            if sheet_name is None:
                self._df = pd.concat(pd.read_excel(
                    f, sheet_name=sheet_name), ignore_index=ignore_index)
            else:
                self._df = pd.read_excel(f, sheet_name=sheet_name)

        return self._df


class SaveDfToCSV:
    """Save the dataframe to a existing or a new csv file.
    attributes and methods.

    Attributes
    ----------

    storage_file_path : str
    df : dataframe

    Methods
    -------
    add_df_existing_csv_file(self, mode='a', index=False, header=False, encoding='utf-8')
    create_new_csv_file_df(self, mode='a', index=False, encoding='utf-8')

    """

    def __init__(self, storage_file_path, df):
        """Inits the SaveToDf with:

        Parameters
        ----------
        storage_file_path : str
            pathname to directory where the csv file should be stored.
        df : dataframe
            the data which should be stored in the csv file.
        """
        self.storage_file_path = storage_file_path
        self.df = df

    def add_df_existing_csv_file(self, mode='a', index=False, header=False, encoding='utf-8'):
        """Adds the dataframe to an existing file.

        Parameters
        ----------
        mode : str, optional
            append the file with the data from Dataframe, by default 'a'
        index : bool, optional
            if an index column is needed, by default False
        header : bool, optional
            if a header is needed, by default False
        encoding : str, optional
            character-encoding, by default 'utf-8'

        Returns
        -------
        csv file:
            the data from the new dataframe
        """
        print(f'Es werden {len(self.df.index)} Datensätze importiert.')
        # saves to existing csv file
        return self.df.to_csv(self.storage_file_path, mode=mode, index=index,
                              header=header, encoding=encoding)

    def create_new_csv_file_df(self, mode='a', index=False, encoding='utf-8'):
        """Creates a new csv file for the data from the dataframe

        Parameters
        ----------
        mode : str, optional
            append the file with the data from Dataframe, by default 'a'
        index : bool, optional
            if an index column is needed, by default False
        encoding : str, optional
            character-encoding, by default 'utf-8'

        Returns
        -------
        csv file:
            the data from the new dataframe.
        """
        print(f'Es werden {len(self.df.index)} Datensätze importiert.')
        return self.df.to_csv(self.storage_file_path, mode=mode, index=index, encoding=encoding)


class CleanPreProcDf:
    """Basic cleaning and preprocessing the dataframe before importing to csv.
    attributes and methods. Can also extract Information from columns into new
    columns.

    Attributes
    ----------
    char : str

    Methods
    -------
    select_row_numbers(self, start=None, end=None)
    remove_rows_with_special_char(self, char='-')
    remove_whitespaces_col_headers(self)
    create_new_column_for_rvk_benennung(
        self, col_name_extract, col_name_extract_new, col_name_map_new,
        filename, pattern, col_header=None)
    create_new_column_by_dict_value(
        self, col_name_map_new, col_name_map, filename, col_header=None)
    fill_rows_value_by_column(self, col_name_extract, substring, col_name_fill)
    precalc_column(self, col_name_calc, col_name_cond, col_name_val)
    setting_value_column(self, col_name_set, value_set=0)
    """

    def __init__(self, df):
        """Inits CleanPreProcDf with:

        Parameters
        ----------
        df : dataframe
            a dataframe to clean
        """
        self.df = df

    def select_row_numbers(self, start=None, end=None):
        """Select specific subset from dataframe to import to csv

        Parameters
        ----------
        start : int, optional
            from which row, by default None
        end : int, optional
            to which row, by default None

        Returns
        -------
        dataframe:
             the rows which where selected
        """
        # select row numbers for the dataframe
        self.df = self.df.iloc[start:end]
        return self.df

    def remove_rows_with_special_char(self, char='-'):
        """Removes rows with only a specific character.

        Parameters
        ----------
        char : str, optional
            select character, by default '-'

        Returns
        -------
        dataframe:
             dataframe without the rows with special characters
        """

        self.df = self.df[~self.df.apply(lambda row: row.astype(
            str).str.contains(char).all(), axis=1).dropna()]
        return self.df

    def remove_whitespaces_col_headers(self):
        """Removes unnecessary whitespace from header column header values.

        Returns
        -------
        dataframe:
            contains only one whitespace between column header value
        """
        self.df.columns = self.df.columns.str.replace(r'\s+', ' ')
        return self.df

    # wenn Zeit: Umschreiben in zwei Methoden
    # (Erstellen einer leeren col, Füllen einer col mit dictionary val)
    def create_new_column_for_rvk_benennung(self, col_name_extract, col_name_extract_new, col_name_map_new, filename, pattern, col_header=None):
        """Returns a dataframe with a new column extracted from string by a
        regex and then check that new column against a dictionary.

        Parameters
        ----------
        col_name_extract : str
            column from which data will be extracted.
        col_name_new : str
            new column which will be created by the extracted dataset.
        filename : str
            csv file with the data which will be mapped against the new column.
        pattern : str
            regex-pattern to find and copy the data into the new column.
        col_header : list, optional
            values for the read_csv_file_in_dict function, by default None

        Returns
        -------
        dataframe:
            with the new columns added.
        """
        rvk_dict = read_csv_file_in_dict(filename, col_header)

        self.df[col_name_extract_new] = self.df[col_name_extract].str.extract(
            pattern)
        # map the keys from the rvk dic with values of the column
        # Systematikstelle and create a new column with the value from the
        # matching key
        self.df[col_name_map_new] = self.df[col_name_extract_new].map(rvk_dict)

        return self.df

    def create_new_column_by_dict_value(self, col_name_map_new, col_name_map, filename, col_header=None):
        """Returns a pandas dataframe with a new column which contains the values
        from a dictionary which is mapped against another column.
        Parameters
        ----------
        col_name_map_new : str
            the name of the new column.
        col_name_map : str
            the name of the column which is mapped by the dictionary keys.
        filename : str
            the name of the filename which contains the data which will be transformed into a dictionary.
        col_header : list, optional
            name of the column headers for the csv file, by default None

        Returns
        -------
        dataframe :
            wth the new column based on another column.
        """

        dic = read_csv_file_in_dict(filename, col_header)
        # making a copy of a dataframe and working on that to avoid the copyWarning
        # https://stackoverflow.com/a/32682095
        self.df = self.df.copy()
        # copy the column
        self.df.loc[:, col_name_map_new] = self.df[col_name_map]
        # retain the column values if not mapping key found in dictionary
        self.df.loc[:, col_name_map_new] = self.df[col_name_map_new].map(
            dic).fillna(self.df[col_name_map_new])

        return self.df

    def fill_rows_value_by_column(self, col_name_extract, substring, col_name_fill, col_val_fill):
        """Returns a pandas dataframe with replaced nan-values by a substring
        from another column based on the condition that this column contains the
        substring.

        Parameters
        ----------
        col_name_extract : str
            the name of the column which will be extracted.
        substring : str
            the substring itself
        col_name_fill : str
            the name of the column which will be filled.

        Returns
        -------
        dataframe:
            dataframe with replaced nan-values in one column.
        """

        self.df.loc[self.df[col_name_extract].str.contains(
            substring), col_name_fill] = col_val_fill

        return self.df

    def precalc_column(self, col_name_calc, col_name_cond, col_name_val):
        """Returns a pandas dataframe with calculations (substraction) on one
        column based on two conditions (the value is greater than 0, and the
        value of another column is not).

        Parameters
        ----------
        col_name_calc : str
            the name of the column which will be calculated on.
        col_name_cond : str
            the name of the column which is the condition.
        col_name_val : str
            the value of the column.

        Returns
        -------
        dataframe:
            returns a dataframe with clean(er) numbers
        """

        self.df.loc[(self.df[col_name_calc] > 0) & (
            self.df[col_name_cond] != col_name_val), col_name_calc] -= 1

        return self.df

    def setting_value_column(self, col_name_set, value_set=0):
        """Returns a dataframe with a column in which all values are set
        to a specific value.

        Parameters
        ----------
        col_name_set : str
            the name of the column in which the values will set.
        value_set : int, optional
            the value, by default 0

        Returns
        -------
        dataframe:
            with manipulated values of a column.
        """

        self.df[col_name_set] = value_set

        return self.df


if __name__ == '__main__':
    pass
