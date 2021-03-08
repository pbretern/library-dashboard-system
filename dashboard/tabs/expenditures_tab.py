#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This file creates figures about expenditure data from the library
collection with the help of the methods of the class Expenditure from the module
data_prep.py. It also produces html divs with those figures which finally
will be returned as general layout for the presentation in the dashboard. It also
handles the interactivity for part of the figures by a callback decorator function.
There are several parts in the code: Instantiating and loading the data, getting the list
for the dropdown, making figures of the data, making cards, making html.Divs of the figures,
cards and dropdown, making the overall layout, and a callback decorator function for interactivity.
of the tab. There are two functions from utils_dash.py which help to create the dropdown menu
(create_dropdown_list, get_list_from_df) and the cards (generate_card_content).
They will be called by the function get_dropdown_menu inside this file.
"""

import pandas as pd
import plotly.express as px

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app
from src.data_prep import Expenditures
from src.utils_dash import create_dropdown_list, get_list_from_df, generate_card_content

from configuration import FILEPATH_UMSATZ_STOR, FILEPATH_BUDGET_STOR


# -------------------------------Loading the essential data -------------------


# für die DropdownListe
df_list_retailler = pd.read_csv(FILEPATH_UMSATZ_STOR)

# Gesamtumsatz
h = Expenditures(FILEPATH_UMSATZ_STOR)
df_total_expnd = h.total_expnd_net_years('Datum')

# Top-Gesamtumsatz
j = Expenditures(FILEPATH_UMSATZ_STOR)
# df_gesamtumsatz_top
df_top_expnd = j.total_expnd_by_bodies_above_value('Datum',
                                                   'Lieferant Abk.',
                                                   'Umsatz (EUR)', 9)
# Gesamtbudget
i = Expenditures(FILEPATH_BUDGET_STOR)
df_total_budget = i.total_expnd_net_years('Datum')

# Top-Gesamtbudget
i = Expenditures(FILEPATH_BUDGET_STOR)
df_top_budget = i.total_expnd_by_bodies_above_value('Datum',
                                                    'Bezeichnung',
                                                    'Ausg. ges.', 4)

# ---------------------------------Figures Umsatz------------------------------


def fig_bookseller_trends(body='Antiquariat'):
    """Returns a Plotly Graph Object with expenditure data. 
    There is a need for the interactivity to instanciating an object from the 
    class Expenditures and to invoke a method for filtering the data by the parameter.

    Parameters
    ----------
    body : str, optional
        by default 'Antiquariat'

    """

    # Instanciaring an object.
    f = Expenditures(FILEPATH_UMSATZ_STOR)
    df_net_year_body = f.total_expnd_net_year_by_body(
        col_name_date='Datum', col_name_body='Lieferant Abk.', body=body)

    # making the plot
    fig = px.bar(df_net_year_body,
                 x='Datum',
                 y='Umsatz (EUR)',
                 title='Gesamtumsatz Lieferant nach Jahren',
                 template='simple_white')

    # avoids reformatting xaxis as (float) numbers
    # https://github.com/plotly/plotly.js/issues/135
    fig.update_xaxes(type='category')

    fig.update_layout(title_x=0.5,
                      xaxis_title="Jahr",
                      yaxis_title='Umsatz (EUR)',
                      height=400)
    # set the color of the bars
    fig.update_traces(marker_color='#66C5CC')

    return fig


def fig_total_expnd():
    """Returns a Plotly Graph Object with expenditure data.
    """
    fig = px.bar(df_total_expnd,
                 x='Umsatz (EUR)',
                 y='Datum',
                 orientation='h',
                 color='Lieferant Abk.',
                 title='Gesamtumsatz Lieferanten nach Jahren',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_layout(title_x=0.5,
                      xaxis_title='Umsatz (EUR)',
                      yaxis_title='Jahr',
                      height=500)

    fig.update_xaxes(nticks=20)
    return fig


def fig_top_expnd():
    """Returns a Plotly Graph Object with expenditure data.
    """
    fig = px.bar(df_top_expnd,
                  y='Umsatz (EUR)',
                  x='Lieferant Abk.',
                  title = 'Top 10 Lieferanten mit Sonstige',
                  color='Lieferant Abk.',
                  color_discrete_sequence=px.colors.qualitative.Pastel,
                  template='simple_white')
    

    fig.update_layout(title_x=0.5, 
                      xaxis_title='Lieferant',
                      yaxis_title='Umsatz (EUR)',
                      height=500)
    
    fig.update_xaxes(categoryorder='total descending')
    
    return fig

def fig_expnd_diff(body='Antiquariat'):
    """Returns a Plotly Graph Object with expenditure data. 
    There is a need for the interactivity to instanciating an object from the 
    class Expenditures and to invoke a method for filtering the data by the parameter.

    Parameters
    ----------
    body : str, optional
        by default 'Antiquariat'

    """

    h = Expenditures(FILEPATH_UMSATZ_STOR)
    df_expnd_diff = h.total_expnd_net_year(col_name_date='Datum',
                                           col_name_body='Lieferant Abk.',
                                           col_name_expnd='Umsatz (EUR)',
                                           col_name_expnd_diff='Umsatz Diff',
                                           body=body)

    fig = px.bar(df_expnd_diff,
                 x='Datum',
                 y='Umsatz Diff',
                 title='Lieferant Umsatz pro Monat laufendes Jahr',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_layout(title_x=0.5,
                      xaxis_title='Monat',
                      yaxis_title='Umsatz (EUR)',
                      height=400)

    fig.update_xaxes(tick0='2020-01-01', dtick="M1", tickformat="%b")
    

    return fig


# ---------------------------------Figures Budget------------------------------
def fig_total_budget_years():
    """Returns a Plotly Graph Object with expenditure data.
    """
    fig = px.bar(df_total_budget,
                 x='Ausg. ges.',
                 y='Datum',
                 orientation='h',
                 color='Bezeichnung',
                 title='Gesamtbudget Kostenstellen nach Jahren',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_layout(title_x=0.5,
                      xaxis_title='Kosten (EUR)',
                      yaxis_title='Jahr',
                      height=500)
    
    fig.update_xaxes(nticks=20)

    return fig


def fig_budget_top():
    """Returns a Plotly Graph Object with expenditure data.
    """
    fig = px.pie(df_top_budget,
                 values='Ausg. ges.',
                 names='Bezeichnung',
                 title='Top 5 Kostenstellen mit Sonstige',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_layout(title_x=0.5, height=500)
    return fig


# ---------------------------------Cards Umsatz--------------------------------

def generate_cards_total():
    """Returns a HtmL Div with with dash bootstrap components for cards. It is
    filled with the values calculated by methods of the class Expenditure (total,
    and total per current year.)
    """
    i = Expenditures(FILEPATH_UMSATZ_STOR)
    bookseller_total = i.total_expnd_net(col_name_date='Datum',
                                         col_name_expnd='Umsatz (EUR)')
    
    bookseller_total_year = i.total_expnd_net_current_year(col_name_date='Datum',
                                                           col_name_expnd='Umsatz (EUR)')

    cards = html.Div(
        [
            dbc.Card(generate_card_content(
                'Gesamtumsatz', bookseller_total),
                color='success',
                inverse=True),

            dbc.Card(generate_card_content(
                'Gesamtumsatz laufendes Jahr', bookseller_total_year),
                color='success',
                inverse=True),

        ], className="one columns chart_div"
    )
    return cards

def generate_cards_for_body(body='Antiquariat'):
    """Returns a HtmL Div with with dash bootstrap components for cards. It is
    filled with the values calculated by methods of the class Expenditure (total
    expenditures for body and mean for body)

    Parameters
    ----------
    body : str, optional
        the name of the body, by default 'Antiquariat'

    Returns
    -------
    html.Div:
       with the calculated values.
    """

    i = Expenditures(FILEPATH_UMSATZ_STOR)
    bookseller_total_current_year = i.total_expnd_net_current_year_by_body(col_name_date='Datum',
                                                                           col_name_expnd='Umsatz (EUR)',
                                                                           col_name_body='Lieferant Abk.',
                                                                           body=body)
    i = Expenditures(FILEPATH_UMSATZ_STOR)
    current_year_mean = i.total_expnd_mean_by_body(col_name_date='Datum',
                                                   col_name_expnd='Umsatz (EUR)',
                                                   col_name_body='Lieferant Abk.',
                                                   body=body)
    cards = html.Div(
        [
            dbc.Card(generate_card_content(
                'Umsatz laufendes Jahr', bookseller_total_current_year),
                color='success',
                inverse=True),

            dbc.Card(generate_card_content(
                'Jahresdurchschnitt', current_year_mean),
                color='success',
                inverse=True),
        ], id='umsatz_card', className="one columns chart_div"
    )
    return cards


# ---------------------------HTML-UMSATZ---------------------------------------

def html_fig_bookseller_trends():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_bookseller_trends',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='expnd_net_year_by_body',
                        figure=fig_bookseller_trends('Antiquariat')
                    ),
                ], className="five columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ],
    )


def html_fig_total_expnd():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_total_expnd',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='gesamtumsatz',
                        figure=fig_total_expnd()
                    ),
                ], className="six columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ]
    )


def html_fig_expnd_diff():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_expnd_diff',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='umsatz_diff',
                        figure=fig_expnd_diff('Antiquariat')
                    ),
                ], className="six columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ]
    )


def html_fig_top_expnd():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_top_expnd',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='gesamtumsatz_top',
                        figure=fig_top_expnd()
                    ),
                ], className="five columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ]
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
                [html.Label('Auswahl Lieferant'),
                 dcc.Dropdown(id='my-id'+str(id),
                              options=create_dropdown_list(
                                  get_list_from_df(df_list_retailler, 'Lieferant Abk.')),
                              value='Antiquariat'
                              ),
                 ], className='eleven columns', style={'margin-left': '10px'}
            )
        ], className="row", style={}
    )

# ---------------------------HTML-Budget---------------------------------------

def html_fig_total_budget_years():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_top_expnd',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='total_budget',
                        figure=fig_total_budget_years()
                    ),
                ], className="six columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ]
    )


def html_fig_budget_top():
    """Returns a html Div with a Plotly Graph Object returned by 'fig_budget_top',
    which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='budget_top',
                        figure=fig_budget_top()
                    ),
                ], className="five columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ]
    )


# ---------------------------------------Tab-Layout----------------------------

def generate_layout():
    """Returns the layout for this tab, that will be used in index.py
    """
    layout = html.Div(
        [
            
            html.Div([
                html.H6('Umsatz'),
                html_fig_total_expnd(),
                html_fig_top_expnd(),
                generate_cards_total(),
            ], className='row'),
            
            html.Div([
                get_dropdown_menu(id=1),
             ], className='row'),
            
             html.Div([
                html_fig_bookseller_trends(),
                html_fig_expnd_diff(),
                generate_cards_for_body(),
                ], className='row'),
            
            html.Div([
                html.H6('Budget'),
                html_fig_total_budget_years(),
                html_fig_budget_top()
            ], className='row')
        ]
    )
    return layout


# ----------------------------------Callback(s)--------------------------------

@app.callback([
    Output(component_id='expnd_net_year_by_body', component_property='figure'),
    Output(component_id='umsatz_diff', component_property='figure'),
    Output(component_id='umsatz_card', component_property='children')],
    [Input(component_id='my-id1', component_property='value')])
def update_output_div(input_value):
    """Changed the output for three functions (fig_bookseller_trends,
    fig_expnd_diff, generate_cards_for_body )which are modified by the values of
    the dropdown list. The "inputs" and "outputs" are described declaratively as 
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
    return fig_bookseller_trends(input_value), fig_expnd_diff(input_value), generate_cards_for_body(input_value)
