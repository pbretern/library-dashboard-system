#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""see: https://dash.plotly.com/urls
The Dash instance is defined in a separate app.py, while the entry point for 
running the app is index.py. This separation is required to avoid circular 
imports: the files containing the callback definitions require access to the 
Dash app instance however if this were imported from index.py, 
the initial loading of index.py would ultimately
require itself to be already imported, which cannot be satisfied.
"""
import dash

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
