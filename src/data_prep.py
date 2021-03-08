#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" This module provides some basic sanity checks on Pandas Dataframes. Also it
includes subclasses of the class DataPreparation, e.g. Expenditures, Collection,
ReadingRoom and LoanColl which are tailored to specific problems in
context of library expenditures (budgets, sales), collection,
readingroom use and loan. They all present the basic layer for the latter data
visualization with Plotly and Dash."""

# os func
import os
# datetime func
import datetime
# pandas func
import pandas as pd
# some utils func
from src.utils import read_csv_file_in_dict, get_dates_list


class DataPreparation:
    """This class contains generic method for the preprocessing and preparation
    of data which will be shown in the dashboard. These methods will be applied
    after the data files are imported in a pandas dataframe from the storage
    folders. This class is a base class which provides methods for classes which
    inherits from this class.

    Attributes
    ----------

    filename : str
    _df : dataframe
    _match : str
    _change_row_val : dictionary
    _years : list
    _date_max : Pandas Timestamp Object
    _not_top_number_val : Pandas Series

    Methods
    -------
    create_dataframe(self, filename)
    change_col_val(self, file, col_name, col_headers=None)
    set_str_to_datetime(self, col_name)
    get_specific_dates_dataframe(self, col_name_date)


   """

    def __init__(self, filename):
        """Inits Datapreparation with some private attributes which will be
        needed in other methods. Calls the method create_dataframe which will
        load dataframe.

        Parameters
        ----------
        filename : str
             the name of the file.

        Attributes
        ----------
        filename : str
        _df : dataframe
        _change_row_val : dictionary
        _years : list
        _date_max : Pandas Timestamp Object
        _not_top_number_val : Pandas Series

        """
        self.filename = filename
        self._df = self.create_dataframe(self.filename)
        self._change_row_val = {}
        self._years = []
        self._date_max = None
        self._not_top_number_val = None

    def create_dataframe(self, filename, encoding='utf-8'):
        """Returns the loaded dataframe.

        Parameters
        ----------
        filename : str
            the name of the file.
        encoding : str, optional
            the encoding format for reading a csv file, by default 'utf-8'.

        Returns
        -------
        dataframe :
            with the data.

        Raises
        ------
        FileNotFoundError
            if file does not exist.
        """
        # loads the dataframe
        if not os.path.exists(filename):
            raise FileNotFoundError('File does not exists.')

        self._df = pd.read_csv(filename, encoding=encoding)

        return self._df

    def top_number_values(self, col_name_sum, col_name_sort, new_value='Sonstige', number=9):
        """Returns a pandas Dataframe with the top number values grouped and sum by
        a column, sorted by a another column. It also replaces the other not top
        ten values with unique value.

        Parameters
        ----------
        col_name_sum : str
            the name of the column on which will be grouped and sum.
        col_name_sort : str
            the name of the sort column.
        new_value : str, optional
            name of the new value for the not top ten values, by default 'Sonstige'
        number : int, optional
            filter the top values by that number, by default 9

        Returns
        -------
        dataframe:
           with top number values
        """
        self._not_top_number_val = self._df.groupby(col_name_sum).sum().sort_values(
            col_name_sort, ascending=False).index[number:]
        self._df = self._df.replace(self._not_top_number_val, new_value)

        return self._df

    def change_col_val(self, file, col_name, col_headers=None):
        """Replaces values in a column with values from a dictionary which will
        be load from a csv file.

        Parameters
        ----------
        file : str
            the name of the csv file which contains two columns.
        col_name : str
             the name of the column.
        col_headers : list, optional
             the names of the columns of the filename, by default None

        Returns
        -------
        dataframe:
          with the changed values from the dictionary.
        """
        # loads the file into a dictionary
        self._change_row_val = read_csv_file_in_dict(file, col_headers)
        # replace the old values against the new ones, also substrings
        self._df[col_name] = self._df.replace(self._change_row_val, regex=True)

        return self._df

    def get_specific_dates_dataframe(self, col_name_date, col_name_year='Jahr'):
        """Returns a dataframe filtered by specific dates.

        Parameters
        ----------
        col_name_date : str
             the name of the date column.

        Returns
        -------
        dataframe:
             rows filtered by date.
        """
        # load the date data in a list
        self._years = get_dates_list()
        # set column to index
        self._df = self._df.set_index(col_name_date)
        # determine the max date in the index column
        self._date_max = self._df.index.max()
        # check if not max_value in years
        if not self._date_max in self._years:
            # replace the value in list on index -1 with the max value in dataframe
            self._years[-1] = self._date_max

        # select rows with the values of the dates list
        self._df = self._df.loc[self._df.index.intersection(
            self._years).sort_values()]
        # split the values in the index by '-' at position 0 and making a new column out of it
        self._df[col_name_date] = self._df.index.astype(
            str).str.split('-').str[0]
        # setting the new column to datetime objects
        self._df[col_name_date] = pd.to_datetime(
            self._df[col_name_date]).dt.year
        return self._df


class Expenditures(DataPreparation):
    """This class is tailored for the expenditure data of the library. It is a
    child class which inherits attributes and methods from its parent class
    DataPreparation. The class has own attributes and own methods, which computes
    some basic mathematical operations using pandas.

    Attributes
    ----------

    filename : str
    __date_max : str

    Methods
    -------
    total_expnd_net(self, col_name_date, col_name_expnd):
    total_expnd_mean_by_body(self, col_name_date, col_name_expnd, col_name_body, body='Antiquariat')
    total_expnd_net_year_by_body(self, col_name_date, col_name_body, body='Antiquariat')
    total_expnd_net_current_year(self, col_name_date, col_name_expnd):
    total_expnd_net_current_year_by_body(self, col_name_date, col_name_expnd, col_name_body, body='Antiquariat')
    total_expnd_net_years(self, col_name_date)
    total_expnd_net_year(self, col_name_date, col_name_body, col_name_expnd, col_name_expnd_diff, body='Autorenbuchhandlung Marx')
    total_expnd_by_bodies_above_value(self, col_name_date, col_name_body, col_name_expnd, number=7)

    Parameters
    ----------
    DataPreparation : cls
        Parent class
    """

    def __init__(self, filename):
        """Inits Expenditures with some private variables which will be needed in methods.
        This class inherits methods and attributes from the base class DataPreparation.

        Parameters
        ----------
        filename : str
            the name of the file.

        Attributes
        ----------
        filename : str
        _date_max : str
        _curr_year : int
        _expenditures_above : pandas Series

        """
        self.filename = filename
        self._date_max = None
        self._curr_year = None
        self._expenditures_above = None
        super().__init__(filename)

    def total_expnd_net(self, col_name_date, col_name_expnd):
        """Returns the total expenditures overall.

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        col_name_expnd : str
            the name of the expenditure column.

        Returns
        -------
        float:
            the number of total expenditure overall.
        """
        self._df = self.get_specific_dates_dataframe(col_name_date)
        return self._df[col_name_expnd].sum().round(2)

    def total_expnd_mean_by_body(self, col_name_date, col_name_expnd, col_name_body, body='Antiquariat'):
        """Returns the average of expenditures for one seller or by a cost center.

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        col_name_expnd : str
            the name of the expenditure column.
        col_name_body : str
            the name of the body column.
        body : str, optional
            the name of the actual body, e.g. seller, cost center, by default 'Antiquariat'.

        Returns
        -------
        float:
            the number of total expenditure overall for seller or by cost center.
        """
        self._df = self.get_specific_dates_dataframe(col_name_date)

        return self._df[self._df[col_name_body] == body][col_name_expnd].fillna(0).mean()

    def total_expnd_net_year_by_body(self, col_name_date, col_name_body, body='Antiquariat'):
        """Returns a dataframe with total expenditures for seller or by a cost center for the years

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        col_name_body : str
            the name of the body
        body : str, optional
            the name of the actual body, e.g. seller, cost center, by default 'Antiquariat'

        Returns
        -------
        dataframe:
            with the data for one body (seller, cost center).
        """

        self._df = self.get_specific_dates_dataframe(col_name_date)

        return self._df[self._df[col_name_body] == body]

    def total_expnd_net_current_year(self, col_name_date, col_name_expnd):
        """Returns total expenditures for the current year.

        Parameters
        ----------
        col_name_date : str
            the name of the date columns.
        col_name_expnd : str
            the name of the expenditure column.

        Returns
        -------
        float:
            the number of total expenditures for the current year.
        """

        date_max = self._df[col_name_date].max()
        self._df = self._df.set_index(col_name_date)
        self._df = self._df.loc[date_max]

        return self._df[col_name_expnd].sum()

    def total_expnd_net_current_year_by_body(self, col_name_date, col_name_expnd, col_name_body, body='Antiquariat'):
        """Returns the total expenditure for a seller or by a cost center for the current year.

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        col_name_expnd : str
            the name of the expenditure column.
        col_name_body : str
            the name of the body column.
        body : str, optional
            the name of the actual body, e.g. seller, cost center, by default 'Antiquariat'

        Returns
        -------
        float:
            the number of total expenditures for a seller or by a cost center for the current year.
        """

        date_max = self._df[col_name_date].max()
        self._df = self._df.set_index(col_name_date)
        self._df = self._df.loc[date_max]

        return self._df[self._df[col_name_body] == body][col_name_expnd].sum().round(2)

    def total_expnd_net_years(self, col_name_date):
        """Returns a dataframe filtered by years for
        all retaillers / cost centre.

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        Returns
        -------
        dataframe:
            with the yearly numbers of retailler /cost centre from a set value.
        """
        # filter data by year
        self._df = self.get_specific_dates_dataframe(col_name_date)

        return self._df

    def total_expnd_net_year(self, col_name_date, col_name_body, col_name_expnd, col_name_expnd_diff, body='Antiquariat'):
        """Returns a pandas dataframe for the expenditure on one retailler / by one
        cost centre filtered by month of the actual year. Also calculates the monthly difference between
        the expenditures because of the accumulated data for every month.

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        col_name_body : str
            the name of the body column.
        col_name_expnd : str
            the name of the expenditures column
        col_name_expnd_diff : str
            the name of the new column for the monthly difference.
        body : str, optional
            the actual retailler/ cost centre, by default 'Antiquariat'

        Returns
        -------
        dataframe:
            with the monthly (difference) expenditures for one retailler / by one cost centre.
        """
        # determine current year
        self._curr_year = datetime.datetime.now().year
        # extracting current year from dataframe
        self._df = self._df[self._df[col_name_date].str.contains(
            str(self._curr_year))]
        # sorting date values
        self._df = self._df.sort_values(by=col_name_date)
        # filtering data from one body
        self._df = self._df[self._df[col_name_body] == body]
        # determine the difference, overwrite nan value for the first month
        self._df[col_name_expnd_diff] = self._df[col_name_expnd].diff().fillna(
            self._df[col_name_expnd])
        return self._df

    def total_expnd_by_bodies_above_value(self, col_name_date, col_name_body, col_name_expnd, number=7):
        """Returns a dataframe with just top n values grouped and sum by a column.
        Calls the function top_number_values within.

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        col_name_body : str
            the name of the body column.
        col_name_expnd : [type]
            the name of the expenditures column.
        number : int, optional
            top number values, by default 7

        Returns
        -------
        dataframe:
            with top number values.
        """
        # returns a dataframe with expenditures cost above a value
        self._df = self.get_specific_dates_dataframe(col_name_date)
        self._df = self._df.groupby(col_name_body)[
            col_name_expnd].sum().reset_index()
        self._df = self.top_number_values(
            col_name_sum=col_name_body, col_name_sort=col_name_expnd, number=number)

        self._df = self._df.groupby(col_name_body)[
            col_name_expnd].sum().reset_index()

        return self._df


class Collection(DataPreparation):
    """This class  is tailored for the development in collection. It is a
    child class which inherits attributes and methods from its parent class
    DataPreparation. The class has own attributes and own methods, which computes
    some basic mathematical operations using pandas.

    Attributes
    ----------

    filename : str

    Methods
    -------

    total_collection_years(self, col_name_date, col_name_callnumber):
    development_collection_current_year(self, col_name_date, col_name_shelfmark)
    development_media_type_years(self, file, col_name_media_type,
        col_name_shelfmark, col_name_date, col_name_year, col_name_copy)
    development_cumsum(self, col_name_shelfmark, col_name_date, col_name_copy,
        col_name_year='Jahr', col_name_month='Monat', col_name_cum='cum_s')
    development_collection_top_class_years(self, col_name_class,
        col_name_shelfmark, col_name_date, col_name_copy)
    development_collection_class_overall_top(self, col_name_date, col_name_shelfmark,
        col_name_class, col_name_copy)
    development_collection_class_overall_top(self, col_name_date, col_name_shelfmark,
        col_name_class, col_name_copy, number=9)

    Parameters
    ----------
    DataPreparation : cls
        Parent class
    """

    def __init__(self, filename):
        """Inits the child class Collection with methods inherited from the base class
        DataPreparation.

        Parameters
        ----------
        filename : str
            the name of the file.
        """
        self.filename = filename
        super().__init__(filename)
        self._media_types = {}
        self._curr_year = None

    def total_collection_years(self, col_name_date, col_name_shelfmark, col_name_cum_sum='Gesamt'):
        """Returns a pandas series with the collection numbers indexed by year
        and a column with cumulated sum collection numbers by year.

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        col_name_shelfmark : str
            the name of the column shelf mark.

        Returns
        -------
        Series :
            with the collection numbers indexed by year of the date column.
        """
        # filter data by year
        self._df[col_name_date] = pd.to_datetime(self._df[col_name_date])
        self._df = self._df.set_index(col_name_date)
        self._df = self._df.loc[((self._df[col_name_shelfmark] == '/') | (
            self._df[col_name_shelfmark] == 'Signatur')) | ~self._df[col_name_shelfmark].duplicated()]
        self._df = self._df.groupby(self._df.index.year).sum()
        self._df[col_name_cum_sum] = self._df.cumsum()

        return self._df

    def development_collection_current_year(self, col_name_date, col_name_shelfmark):
        """Returns a pandas series with the development of the collection over one year.

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        col_name_shelfmark : str
            the name of the shelfmark column.

        Returns
        -------
        series :
            with the development of the collection over one year.
        """
        # give back series of collection development over the current year
        self._curr_year = datetime.datetime.now().year
        self._df = self._df[self._df[col_name_date].str.contains(
            str(self._curr_year))]
        self._df[col_name_date] = pd.to_datetime(self._df[col_name_date])
        self._df = self._df.set_index(col_name_date)
        self._df = self._df.loc[((self._df[col_name_shelfmark] == '/') | (
            self._df[col_name_shelfmark] == 'Signatur')) | ~self._df[col_name_shelfmark].duplicated()]
        self._df = self._df.dropna(subset=[col_name_shelfmark])

        self._df = self._df[col_name_shelfmark].resample('M').count()
        self._df = self._df.groupby(self._df.index).sum()
        return self._df

    def development_media_type_years(self, file, col_name_media_type, col_name_shelfmark, col_name_date, col_name_year, col_name_copy):
        """Returns a dataframe which is indexed by year which is extracted from
        the date column. This is needed for representation in the charts.

        Parameters
        ----------
        file : str
            name of the file
        col_name_media_type : str
            name of the media type column.
        col_name_shelfmark : str
            name of the shelfmark column.
        col_name_date : str
            name of the date column.
        col_name_year : str
            name of the new year column.

        Returns
        -------
        dataframe:
            with the extracted year from date column as index.
        """
        self._media_types = read_csv_file_in_dict(file)
        self._df[col_name_media_type] = self._df[col_name_media_type].map(
            self._media_types)
        # drop all the duplicates in shelfmark except two parameters
        self._df = self._df.loc[((self._df[col_name_shelfmark] == '/') | (
            self._df[col_name_shelfmark] == 'Signatur')) | ~self._df[col_name_shelfmark].duplicated()]
        self._df[col_name_date] = pd.to_datetime(self._df[col_name_date])
        self._df = self._df.set_index(col_name_date)
        self._df = self._df.groupby([self._df.index.year, col_name_media_type])[
            col_name_copy].sum().reset_index()

        return self._df

    def development_by_classification(self, col_name_date, col_name_year, col_name_class, body):
        """Returns a pandas dataframe which is filtered by a main class of the RVK.

        Parameters
        ----------
        col_name_date : str
            name of the date column.
        col_name_year : str
            name of the year column which the dataframe will be indexed.
        col_name_class : str
            name of the RVK main class column.
        body : str
            name of the actual RVK main class which the dataframe is filtered.

        Returns
        -------
        dataframe:
            which is filtered by one RVK main class.
        """
        self._df[col_name_date] = pd.to_datetime(self._df[col_name_date])
        self._df[col_name_year] = self._df[col_name_date].dt.year
        self._df = self._df.set_index(col_name_year)

        return self._df[self._df[col_name_class] == body]

    def development_cumsum(self, col_name_shelfmark, col_name_date, col_name_copy, col_name_year='Jahr', col_name_month='Monat', col_name_cum='cum_s'):
        """Returns a pandas dataframe with cumulated summation of one column grouped
        by another one.

        Parameters
        ----------
        col_name_shelfmark : str
            the name of the shelfmark column.
        col_name_date : str
            the name of the date column.
        col_name_copy : str
            the name of the copy (item) column.
        col_name_year : str, optional
            the name of the new created year column, by default 'Jahr'
        col_name_month : str, optional
            the name of the new created month column, by default 'Monat'
        col_name_cum : str, optional
            the name of the new created cum_sum column, by default 'cum_s'

        Returns
        -------
        dataframe:
            pandas dataframe with cumulated summation of one column grouped by another one.
        """

        # drop all the duplicates in shelfmark except two parameters
        self._df = self._df.loc[((self._df[col_name_shelfmark] == '/') | (
            self._df[col_name_shelfmark] == 'Signatur')) | ~self._df[col_name_shelfmark].duplicated()]
        # setting col_name to datetime
        self._df[col_name_date] = pd.to_datetime(self._df[col_name_date])
        # setting col_name to index
        self._df = self._df.set_index(col_name_date)
        # summation of the copies grouped by date index and resetting index
        self._df = self._df.groupby(self._df.index)[
            col_name_copy].sum().reset_index()
        # setting col_name to index
        self._df = self._df.set_index(col_name_date)
        # creating new column year from index
        self._df[col_name_year] = self._df.index.year
        self._df[col_name_month] = self._df.index.month
        # cum sum col_name_copy grouped by year
        self._df[col_name_cum] = self._df[col_name_copy].groupby(
            self._df[col_name_year]).cumsum()

        return self._df

    def development_collection_top_class_years(self, col_name_class, col_name_shelfmark, col_name_date, col_name_copy):
        """Returns a pandas dataframe with the top ten values of one column grouped
        by years from the date column.

        Parameters
        ----------
        col_name_class : str
            the name of the classification column.
        col_name_shelfmark : str
            the name of the shelfmark column.
        col_name_date : str
            the name of the date column.
        col_name_copy : str
            the name of the copy (item) column.

        Returns
        -------
        dataframe:
            with with the top ten values of one column grouped by years from the date column.
        """
        self._df[col_name_date] = pd.to_datetime(self._df[col_name_date])
        self._df = self._df.set_index(col_name_date)
        # drop all the duplicates in shelfmark except two parameters -> REFACTOR
        self._df = self._df.loc[((self._df[col_name_shelfmark] == '/') | (
            self._df[col_name_shelfmark] == 'Signatur')) | ~self._df[col_name_shelfmark].duplicated()]
        self._df = self._df.groupby([self._df.index.year, col_name_class])[
            col_name_copy].sum().reset_index()
        self._df = self._df.sort_values(
            [col_name_copy, col_name_class], ascending=False).groupby(col_name_date).head(10)

        return self._df

    def development_collection_class_overall_top(self, col_name_date, col_name_shelfmark, col_name_class, col_name_copy, number=9):
        """Returns a series with just top n values grouped and sum by a column.
        Calls the function top_number_values within.

        Parameters
        ----------
        col_name_date : str
            the name of the date column.
        col_name_shelfmark : str
            the name of the shelfmark column.
        col_name_class : str
            the name of the classification column,
        col_name_copy : str
            the name of the copy (item) column.
        number : int, optional
            number of the top value, by default 9

        Returns
        -------
        series:
            with just top n values grouped and sum by a column
        """
        self._df[col_name_date] = pd.to_datetime(self._df[col_name_date])
        self._df = self._df.set_index(col_name_date)
        # drop all the duplicates in shelfmark except two parameters -> REFACTOR
        self._df = self._df.loc[((self._df[col_name_shelfmark] == '/') | (
            self._df[col_name_shelfmark] == 'Signatur')) | ~self._df[col_name_shelfmark].duplicated()]
        self._df = self.top_number_values(
            col_name_sum=col_name_class, col_name_sort=col_name_copy, number=number)
        self._df = self._df.groupby(col_name_class)[
            col_name_copy].sum().reset_index()

        return self._df


class ReadingRoom(DataPreparation):
    """This class is tailored for the use of the Reading room data. It is a
    child class which inherits attributes and methods from its parent class
    DataPreparation. The class has own attributes and own methods, which computes
    some basic mathematical operations using pandas.

    Attributes
    ----------

    filename : str

    Methods
    -------
    use_by_years(self, col_name_year)
    use_by_months(self, col_name_year, col_name_date, col_name_month, year=2017)


    Parameters
    ----------
    DataPreparation : cls
        Parent class
    """

    def __init__(self, filename):
        """Inits the child class ReadingRoom with methods inherited from the base class
        DataPreparation.

        Parameters
        ----------
        filename : str
            the name of the file which will be loaded to the dataframe.
        """
        self.filename = filename
        super().__init__(filename)

    def use_by_years(self, col_name_year):
        """Returns a dataframe with the use of the reading room indexed by years.

        Parameters
        ----------
        col_name_year : str
            the name of the year column

        Returns
        -------
        dataframe:
            with the numbers of use of the reading room indexed by year.
        """
        self._df = self._df.set_index(col_name_year)
        self._df.index = pd.to_datetime(self._df.index, format='%Y').year
        self._df = self._df.groupby(self._df.index).sum()

        return self._df

    def use_by_months(self, col_name_year, col_name_date, col_name_month, year=2017):
        """Returns a pandas dataframe with the numbers of monthly use of the reading room.

        Parameters
        ----------
        col_name_year : str
            name of the year column.
        col_name_date : str
            name of the date column.
        col_name_month : str
            name of the month column.
        year : int, optional
            the year by the frame filtered, by default 2017

        Returns
        -------
        dataframe:
            with the numbers of monthly for a year.
        """
        # making a new column for the date which contains the month and the year.
        self._df[col_name_date] = pd.to_datetime(
            self._df[col_name_year].astype(str) + '/' + self._df[col_name_month].astype(str) + '/01')
        # setting the date column to datetime
        self._df[col_name_date] = pd.to_datetime(self._df[col_name_date])
        # filtering the dataframe by year
        self._df = self._df[self._df[col_name_date].dt.year == year]
        # seting the date column to index
        self._df = self._df.set_index(col_name_date)
        # groupbing by the index month
        self._df = self._df.groupby([self._df.index, col_name_year]).sum()

        self._df = self._df.reset_index()
        self._df = self._df.set_index(col_name_date)

        return self._df


class LoanColl(DataPreparation):
    """This class is tailored for the use of the loan data. It is a
    child class which inherits attributes and methods from its parent class
    DataPreparation. The class has own attributes and own methods, which computes
    some basic mathematical operations using pandas.

    Attributes
    ----------

    filename : str

    Methods
    -------
    total_loans(self, col_name_year, col_name_loan)
    use_by_months(self, col_name_year, col_name_date, col_name_month, year=2017)


    Parameters
    ----------
    DataPreparation : cls
        Parent class
    """

    def __init__(self, filename):
        """Inits the child class LoanColl with methods inherited from the base class
        DataPreparation.

        Parameters
        ----------
        filename : str
            the name of the file which will be loaded to the dataframe.
        """

        self.filename = filename
        super().__init__(filename)

    def total_loans(self, col_name_year, col_name_loan, col_name_class, new_value='Sonstige', number=9):
        """Returns a pandas dataframe with all the titles indexed by years.

        Parameters
        ----------
        col_name_year : str
            the name of the year column.
        col_name_loan : str
            the name of the loan column.         
        number : int, optional
            number of the top value, by default 9

        Returns
        -------
        dataframe:
            with all the titles indexed by year.
        """
        self._df[col_name_year] = pd.to_datetime(
            self._df[col_name_year], format='%Y').dt.year

        self._df = self.top_number_values(
            col_name_sum=col_name_class, col_name_sort=col_name_loan, new_value=new_value, number=number)

        self._df = self._df.set_index(col_name_year)

        self._df = self._df.groupby(
            [self._df.index, col_name_class]).sum().reset_index()

        self._df = self._df.set_index(col_name_year)

        return self._df

    def top_loans_by_title(self, col_name_year, col_name_loan, number=5):
        """Returns a pandas dataframe with the top number of loans multi indexed
        (years).

        Parameters
        ----------
        col_name_year : str
            the name of the year column.
        col_name_loan : str
            the name of the loan column.
        number : int, optional
            number of how many rows should be shown, by default 5

        Returns
        -------
        dataframe:
            with the top number of loans over the years by year.
        """
        # returns a dataframe multi indexed by year
        # group the largest number of loans by the year
        self._df = self._df.groupby([self._df[col_name_year]]).apply(
            lambda x: x.nlargest(number, col_name_loan))

        return self._df

    def library_loan_class(self, col_name_year, col_name_class, exclude_value, col_name_loan, new_value='Sonstige', number=9):
        """Returns a pandas dataframe with the top n values of a column. It also
        excludes values from that column by an exclude value. 

        Parameters
        ----------
        col_name_year : str
            the name of the year column.
        col_name_class : str
            the name of the classification column.
        exclude_value : str
            the name of the exclude value.
        col_name_loan : str
            the name of the loan column.
        new_value : str, optional
            the name of the value which replaces the under top n, by default 'Sonstige'.
        number : int, optional
            number to include in the top n, by default 9

        Returns
        -------
        dataframe:
            with the new value for under top n and the exclusion of a certain value. 
        """
        self._df = self._df.set_index(col_name_year)
        self._df = self._df[self._df[col_name_class] != exclude_value]
        self._df = self.top_number_values(
            col_name_sum=col_name_class, col_name_sort=col_name_loan, new_value=new_value, number=number)
        self._df = self._df.groupby(col_name_class)[
            col_name_loan].sum().reset_index()

        return self._df


if __name__ == '__main__':
    pass
