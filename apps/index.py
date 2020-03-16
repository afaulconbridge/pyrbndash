# -*- coding: utf-8 -*-
import itertools
import random

import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output, State
from pyrbn import RBN

layout = html.Div(
    children=[
        html.H1("RBN Dashboard"),
        html.Div(dcc.Link("Single RBN information", href="/rbn-single")),
        html.Div(dcc.Link("Collective RBN information", href="/rbn-multi")),
    ]
)
