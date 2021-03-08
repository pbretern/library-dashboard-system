#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This file creates figures about new acquision and collection data from the library
with the help of the methods of the classes Collection and LoanColl from the module
data_prep.py. It also produces html divs with those figures which finally
will be returned as general layout for the presentation in the dashboard.
There are 4 parts in the code: Instantiating and loading the data, making 
figures of the data, making html.Divs of the figures, making the overall layout
of the tab.
"""

import plotly.express as px

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


from app import app
from src.data_prep import Collection, LoanColl

from configuration import FILEPATH_HELPER_MAT

from configuration import FILEPATH_NEWACQ_STOR, FILEPATH_LOAN_STOR


# -------------------------------Loading the essential data -------------------

# neuerwerbungen laufendes jahr
a = Collection(FILEPATH_NEWACQ_STOR)
df_new_acq_curr_year = a.development_collection_current_year(
    col_name_date='Datum', col_name_shelfmark='Signatur')

# Bestandswachstum relatives und absolutes
e = Collection(FILEPATH_NEWACQ_STOR)
df_total_collection_years = e.total_collection_years(
    col_name_date='Datum', col_name_shelfmark='Signatur')

# Bestandswachstum nach Medientyp
# wird nicht in Dashboard angezeigt
# k = Collection(FILEPATH_NEWACQ_STOR)
# df_development_media_type_years = k.development_media_type_years(FILEPATH_HELPER_MAT,
#                                                                  col_name_date='Datum',
#                                                                  col_name_media_type='0500',
#                                                                  col_name_shelfmark='Signatur',
#                                                                  col_name_year='Jahr',
#                                                                  col_name_copy='Ex')

# Bestandswachstum nach Monat / Jahr
j = Collection(FILEPATH_NEWACQ_STOR)
df_cumsum_development_years = j.development_cumsum(col_name_shelfmark='Signatur',
                                                   col_name_date='Datum',
                                                   col_name_copy='Ex')

# Top ten classes per year
i = Collection(FILEPATH_NEWACQ_STOR)
df_development_top_class_years = i.development_collection_top_class_years(col_name_class='Systematikgruppe',
                                                                          col_name_shelfmark='Signatur',
                                                                          col_name_date='Datum',
                                                                          col_name_copy='Ex')

# Top class total
k = Collection(FILEPATH_NEWACQ_STOR)
df_development_top_class_total = k.development_collection_class_overall_top(col_name_date='Datum',
                                                                            col_name_shelfmark='Signatur',
                                                                            col_name_class='Systematikgruppe',
                                                                            col_name_copy='Ex')

y = LoanColl(FILEPATH_LOAN_STOR)
df_library_loan_class = y.library_loan_class(col_name_year='year',
                                             col_name_class='Systematikgruppe',
                                             exclude_value='Buchservice',
                                             col_name_loan='cum_loans')

# ---------------------------------Figures Bestand-----------------------------

def fig_new_acq_curr_year():
    """Returns a Plotly Graph Object with collection data.
    """
    fig = px.bar(df_new_acq_curr_year,
                 x=df_new_acq_curr_year.index,
                 y='Signatur',
                 title='Monatliche Neuerwerbungen laufendes Jahr',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_layout(title_x=0.5,
                      xaxis_title='Monat',
                      yaxis_title='Anzahl der Exemplare',
                      height=500
                      )

    fig.update_xaxes(tick0='2020-01-31', dtick="M1", tickformat="%b")
    fig.update_yaxes(nticks=20)

    return fig


def fig_total_collection_years():
    """Returns a Plotly Graph Object with collection data.
    """
    fig = px.bar(df_total_collection_years,
                 x=df_total_collection_years.index,
                 y=['Gesamt', 'Ex'],
                 title='Bestandswachstum pro Jahr und Gesamt',
                 barmode='overlay',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_layout(title_x=0.5,
                      xaxis_title='Jahr',
                      yaxis_title='Anzahl der Exemplare',
                      legend_title='',
                      height=500
                      )

    fig.update_yaxes(nticks=20)

    return fig


# wird nicht in Dashboard umgesetzt.
# def fig_development_media_type_years():
#     """Returns a Plotly Graph Object with collection data.
#     """
#     fig = px.bar(df_development_media_type_years,
#                  x=df_development_media_type_years['Datum'],
#                  y='Ex',
#                  color='0500',
#                  title='Bestandswachstum Medienart pro Jahr',
#                  color_discrete_sequence=px.colors.qualitative.Pastel,
#                  template='simple_white',
#                  barmode='stack')

#     fig.update_layout(title_x=0.5, xaxis_title='Jahr',
#                       yaxis_title='Bestandswachstum Medianart',
#                       height=500
#                       )

#     fig.update_traces(marker_line_width=0)
#     #fig.update_xaxes(tick0 = '2020-01-31', dtick="M1", tickformat="%b")
#     fig.update_yaxes(nticks=20)

#     return fig


def fig_cumsum_development_years():
    """Returns a Plotly Graph Object with collection data.
    """
    fig = px.line(df_cumsum_development_years,
                  x=df_cumsum_development_years['Monat'],
                  y='cum_s',
                  color='Jahr',
                  title='Jährliche Bestandsentwicklung nach Monaten',
                  height=500,
                  color_discrete_sequence=px.colors.qualitative.Pastel,
                  template='simple_white')

    fig.update_layout(title_x=0.5,
                      xaxis_title='Monat',
                      yaxis_title='Anzahl der Exemplare',
                      # height=400
                      )

    fig.update_xaxes(dtick="M1")

    return fig


def fig_development_top_class_years():
    """Returns a Plotly Graph Object with collection data.
    """
    fig = px.bar(df_development_top_class_years,
                 x=df_development_top_class_years['Datum'],
                 y='Ex',
                 color='Systematikgruppe',
                 title='Top 10 RVK-Fachsystematiken pro Jahr',
                 barmode='stack',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')

    fig.update_layout(title_x=0.5,
                      xaxis_title='Jahr',
                      yaxis_title='Anzahl der Exemplare',
                      height=500
                      )

    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(nticks=10)

    return fig


def fig_development_top_class_total():
    """Returns a Plotly Graph Object with collection data.
    """
    
    fig = px.bar(df_development_top_class_total,
                 x='Systematikgruppe',
                 y='Ex',
                 color='Systematikgruppe',
                 title='Top RVK-Fachsystematiken Bestand mit Sonstige',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')
    
    fig.update_layout(title_x=0.5,
                      xaxis_title='RVK-Systematikstellen',
                      yaxis_title='Anzahl der Exemplare',
                      height=500
                      )
    

    fig.update_yaxes(nticks=10)
    fig.update_xaxes(categoryorder='total descending')

    return fig


def fig_top_loan_dist():
    """Returns a Plotly Graph Object with loan data.
    """
    fig = px.bar(df_library_loan_class,
                 y='cum_loans',
                 x='Systematikgruppe',
                 color='Systematikgruppe',
                 title='Top RVK-Fachsystematiken Ausleihe mit Sonstige',
                 height=500,
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template='simple_white')
    
    fig.update_layout(title_x=0.5,
                      xaxis_title='RVK-Systematikstellen',
                      yaxis_title='Anzahl der Ausleihen',
                      height=500
                      )
    
    fig.update_xaxes(categoryorder='total ascending')
        
    
    return fig

# ---------------------------HTML Figure---------------------------------------


def html_fig_cumsum_development_years():
    """Returns a html Div with a Plotly Graph Object returned by 
    'fig_cumsum_development_years', which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='cumsum_development_years',
                        figure=fig_cumsum_development_years()
                    ),
                ], className="six columns chart_div", style={'margin-top': '20px','margin-left': '10px'}
            ),
        ],
    )


def html_fig_new_acq_curr_year():
    """Returns a html Div with a Plotly Graph Object returned by 
    'fig_new_acq_curr_year', which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='new_acq_curr_year',
                        figure=fig_new_acq_curr_year()
                    ),
                ], className="five columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ],
    )


def html_fig_total_collection_years():
    """Returns a html Div with a Plotly Graph Object returned by 
    'fig_total_collection_years', which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='total_collection_years',
                        figure=fig_total_collection_years()
                    ),
                ], className="six columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ],
    )


# Wird nicht in Dashboard umgesetzt
# def html_fig_development_media_type_years():
#     """Returns a html Div with a Plotly Graph Object returned by
#     'fig_development_media_type_years', which is called inside this function.
#     """
#     return html.Div(
#         [
#             html.Div(
#                 [
#                     dcc.Graph(
#                         id='development_media_type_years',
#                         figure=fig_development_media_type_years()
#                     ),
#                 ], className="five columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
#             ),
#         ],
#     )


def html_fig_development_top_class_years():
    """Returns a html Div with a Plotly Graph Object returned by
    'fig_development_top_class_years', which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='development_top_class_years',
                        figure=fig_development_top_class_years()
                    ),
                ], className="five columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
            ),
        ],
    )


def html_fig_development_top_class_total():
    """Returns a html Div with a Plotly Graph Object returned by
    'fig_development_top_class_total', which is called inside this function.
    """
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='development_top_class_years',
                        figure=fig_development_top_class_total()
                    ),
                ], className="five columns chart_div", style={'margin-top': '20px', 'margin-left': '10px'}
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
                html.H6('Neuerwerbungen und Bestand'),
                html_fig_new_acq_curr_year(),
                html_fig_cumsum_development_years(),
            ], className='row'),
            
            html.Div([
                html_fig_total_collection_years(),
                #html_fig_development_media_type_years(),
                html_fig_development_top_class_years(),
            ], className='row'),
            
            html.Div([
                html.H6('Ausleihe und Bestand'),
                html_fig_top_loan_dist(),
                html_fig_development_top_class_total()
            ], className='row')

        ]
        )

    return layout
