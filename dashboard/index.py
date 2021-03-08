#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""With this file you can actually start the webserver / three-tab dashboard.
It's the entry point for running the app.
It contains some layout functionalities for the dashboard and it loaded the
specific layout from the single tabs and the different tabs.
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from app import app
from tabs import expenditures_tab #, loan_read_tab, newacq_coll_tab

# defining the layout for the three tabbed dashboard
app.layout = html.Div(
    [
        html.Div(
            [
                html.Span('Library Dashboard', className='app-title')
            ],
            className='row header'
        ),

        html.Div(
            [
                dcc.Tabs(
                    id='tabs',
                    style={"height": "100", "verticalAlign": "middle"},
                    children=[
                        dcc.Tab(label='Umsatz und Budget',
                                value='umsatz_budget_tab'),
                        dcc.Tab(label='Lesesaal und Ausleihe',
                                value='lesesaal_ausl_tab'),
                        dcc.Tab(label='Neuerwerbungen und Bestand',
                                value='neuerw_bestand_tab')
                    ],
                    value='umsatz_budget_tab'
                )
            ],
            className='row tabs_div'
        ),

        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"})
    ], className='row', style={'margin': '0%'}
)


@app.callback(Output('tab_content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    """Returns the single app and layout based on the value which iss
    choosen.
    """
    if tab == 'umsatz_budget_tab':
        return expenditures_tab.generate_layout()
    if tab == 'lesesaal_ausl_tab':
        return None
    if tab == 'neuerw_bestand_tab':
        return None
    return None


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
    