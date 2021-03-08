
#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" These module contains functions which do not affect objects (self). Nevertheless
they will be needed for doing some basic jobs, e.g. making a dict from file, making a
list of from file. Find below a list of functions within this module. They will be
used for the dashboard app to not overload the dasboard app files."""


import dash_html_components as html
import dash_bootstrap_components as dbc


def get_list_from_df(df, column_name):
    """getting a list from column with unique values

    Returns
    -------
    list:
        a list with unique names of a column.
    """

    return df[column_name].unique()


def create_dropdown_list(lst):
    """Returns a list of dictionaries.

    Parameters
    ----------
    lst :
        with values

    Returns
    -------
    list:
        of dictionaries
    """
    dropdown_list = [{'label': label, 'value': label}
                     for label in sorted(lst)]

    return dropdown_list


def generate_card_content(card_header, card_value):
    """[summary]

    Parameters
    ----------
    card_header : str, int...
        title for the card.
    card_value : number (float, int) can also be a str like '5'
        which will be cast into an int

    Returns
    -------
    list:
        with the elements card_header card_body
    """

    card_head_style = {'textAlign': 'center', 'fontSize': '100%'}
    card_body_style = {'textAlign': 'center', 'fontSize': '150%'}
    card_header = dbc.CardHeader(card_header, style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H5(f'{int(card_value):,} EUR'.format(card_value).replace(',', '.'),
                    className="card-title", style=card_body_style),
        ]
    )
    card = [card_header, card_body]
    return card


if __name__ == '__main__':
    pass
