#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This file creates figures about readingroom use and loan from the library
collection with the help of help of the methods of the classes ReadingRoom and
LoanColl from the module data_prep.py. Besides the usual plotly express,
it uses plotly graph objects for making a table. It also produces html divs with
those figures which finally will be returned as general layout for the presentation
in the dashboard. It also handles the interactivity for part of the figures by
a callback decorator function. There are several parts in the code: 
Instantiating and loading the data, making figures of the data, making html.Divs 
of the figures and dropdown, making the overall layout, 
and a callback decorator function for interactivity.
There are two functions from utils.py which help to create the dropdown menu
(create_dropdown_list, get_list_from_df).
They will be called by the function get_dropdown_menu inside this file.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from src.data_prep import ReadingRoom, LoanColl

from src.utils_dash import create_dropdown_list, get_list_from_df

from configuration import FILEPATH_LOAN_STOR, FILEPATH_READING_STOR


# -------------------------------Loading the essential data -------------------

# liste Jahr für dropdown
df_liste_year_reading = pd.read_csv(FILEPATH_READING_STOR)

# Jahresnutzung Lesesaal
a = ReadingRoom(FILEPATH_READING_STOR)
df_use_years = a.use_by_years(col_name_year='Jahr')

# mtl. Nutzung Lesesaal
c = ReadingRoom(FILEPATH_READING_STOR)
df_use_months = c.use_by_months(
    col_name_year='Jahr',
    col_name_date='Datum',
    col_name_month='Monat',
    year=2020)

# Ausleihe Jahre
x = LoanColl(FILEPATH_LOAN_STOR)
df_loan_dist = x.total_loans(
    col_name_year='year',
    col_name_loan='cum_loans',
    col_name_class='Systematikgruppe', new_value='Bibliothek', number=1)

y = LoanColl(FILEPATH_LOAN_STOR)
df_loan_years = y.total_loans(
    col_name_year='year',
    col_name_loan='cum_loans',
    col_name_class='Systematikgruppe', new_value='Sonstiges', number=9)

# Top Ausleihe
z = LoanColl(FILEPATH_LOAN_STOR)
df_top_loans = z.top_loans_by_title(
    col_name_year='year', col_name_loan='cum_loans', number=5)


# ---------------------------------Figures Ausleihe----------------------------

def fig_use_by_years():
    """Returns a Plotly Graph Object with use data.
    """
    fig = px.bar(df_use_years,
                 x=df_use_years.index,
                 y=['10.00 - 12.30', '12.30 - 15.00',
                     '15.00 - 17.00', '17.00 - 18.30'],
                 title='Jährliche Lesesaalnutzung nach Service-Zeiten',
                 barmode='group',
                 height=400,
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_layout(title_x=0.5,
                      xaxis_title='Jahr',
                      yaxis_title='Anzahl der Nutzer:innen',
                      legend_title='Service-Zeiten')
    return fig


def fig_use_by_month(year=2017):
    """Returns a Plotly Graph Object for readinngroom use by month / year.

    Parameters
    ----------
    year : int, optional
        filter year, by default 2017

    """
    # Instanciating an object and filtering after the parameter by a method of
    # the class ReadingRoom
    e = ReadingRoom(FILEPATH_READING_STOR)
    df = e.use_by_months(
        col_name_year='Jahr',
        col_name_date='Datum',
        col_name_month='Monat',
        year=year)

    fig = px.line(df,
                  x=df.index,
                  y=['10.00 - 12.30', '12.30 - 15.00',
                      '15.00 - 17.00', '17.00 - 18.30'],
                  title='Monatliche Anzahl der Nutzer:innen nach Service-Zeiten',
                  color_discrete_sequence=px.colors.qualitative.Pastel,
                  template='simple_white'
                  )
    # Update the layout of the plotly graph
    fig.update_layout(title_x=0.5,
                      xaxis_title='Monat',
                      yaxis_title='Anzahl der Nutzer:innen',
                      height=400,
                      legend_title='Service-Zeiten'
                      )

    fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
    fig.update_yaxes(nticks=20)

    return fig


def fig_top_loan_years():
    """Returns a Plotly Graph Object with loan data.
    """
    fig = px.bar(df_loan_years,
                 y=df_loan_years.index,
                 x='cum_loans',
                 orientation='h',
                 color='Systematikgruppe',
                 title='Ausleihe Top RVK-Fachsystematiken mit Buchservice und Sonstige',
                 barmode='stack',
                 height=500,
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_layout(title_x=0.5,
                      xaxis_title='Anzahl Ausleihen',
                      yaxis_title='Jahr')

    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(nticks=20)

    return fig


def fig_top_loan_dist():
    """Returns a Plotly Graph Object with loan data.
    """

    fig = px.pie(df_loan_dist,
                 values='cum_loans',
                 names='Systematikgruppe',
                 title='Gesamtverteilung Ausleihe Buchservice / Bibliothek',
                 height=500,
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_xaxes(categoryorder='total descending')

    fig.update_layout(title_x=0.5)

    return fig


def fig_top_loan_title():
    """Returns a Plotly Graph Object with use data.
    """
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=['Jahr', 'Signatur', 'Titel', 'Anzahl der Ausleihen'],
                            fill_color='rgb(179,226,205)',
                            align='left'),
                cells=dict(values=(df_top_loans.year,
                                   df_top_loans.shelfmark,
                                   df_top_loans.shorttitle,
                                   df_top_loans.cum_loans),
                           fill_color='white',
                           line_color='darkslategray',
                           align='left'),
                columnwidth=[20, 80, 100, 20])
        ])

    fig.update_layout(title='Tabellarische Darstellung der 5 besonders nachgefragten Titel nach Jahren',
                      title_x=0.5,
                      height=1400,
                      plot_bgcolor='#fffcfc',
                      paper_bgcolor='#fffcfc')

    return fig


# ---------------------------HTML-Lesesaal-------------------------------------

def html_fig_use_by_years():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_use_by_years',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='use_by_years',
                        figure=fig_use_by_years()
                    ),
                ], className="five columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ],
    )


def html_fig_use_by_month():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_use_by_month',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='use_by_month',
                        figure=fig_use_by_month(year=2017)
                    ),
                ], className="six columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ],
    )

def get_dropdown_menu(id):
    """Returns a html Div with the dropdown element. Calls inside a function
    which creates tthe dropdown list.

    Parameters
    ----------
    id : should be int
        must be unique for identification of the dropdoown element, important for
        the callback.
    """
    return html.Div(
        [
            html.Div(
                [html.Label('Auswahl Jahr'),
                 dcc.Dropdown(id='my-id'+str(id),
                              options=create_dropdown_list(
                                  get_list_from_df(df_liste_year_reading, 'Jahr')),
                              value=2017
                              ),
                 ], className='six columns', style={'margin-top': '20px', 'margin-left': '10px'}
            )
        ], className="row", style={}
    )


# ---------------------------HTML-Ausleihe-------------------------------------

def html_fig_top_loan_years():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_top_loan_years',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='top_loan_years',
                        figure=fig_top_loan_years()
                    ),
                ], className="six columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ],
    )


def html_fig_top_loan_title():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_top_loan_title',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='top_loan',
                        figure=fig_top_loan_title()
                    ),
                ], className="twelve columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ],
    )


def html_fig_top_loan_dist():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_top_loan_dist',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='top_loan_dist',
                        figure=fig_top_loan_dist()
                    ),
                ], className="five columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ],
    )


# ---------------------------------------Tab-Layout----------------------------

def generate_layout():
    """Returns the layout for this tab, that will be used in index.py
    """
    layout = html.Div(
        [
            html.Div([
                html.H6('Lesesaalnutzung'),
                get_dropdown_menu(id=2),
            ],className='row'),
            
            html.Div([
                html_fig_use_by_month(),
                html_fig_use_by_years(),
            ],className='row'),
            
             html.Div([
                html.H6('Ausleihe'),
                html_fig_top_loan_years(),
                html_fig_top_loan_dist(),
            ],className='row'),
             
            html.Div([
                html_fig_top_loan_title()
            ],className='row')

        ])

    return layout

# ----------------------------------Callback(s)--------------------------------


@app.callback(
    Output(component_id='use_by_month', component_property='figure'),
    [Input(component_id='my-id2', component_property='value')])
def update_output_div(input_value):
    """Changed the output for one function (fig_use_by_month)
    which is modified by the values of the dropdown list. 
    The "inputs" and "outputs" are described declaratively as 
    the arguments of the @app.callback decorator.

    see: https://dash.plotly.com/basic-callbacks

    Parameters
    ----------
    input_value : str
        the value of the dropdown list.

    Returns
    -------
    functions:
        which are modified by the input value.
    """

    return fig_use_by_month(input_value)
