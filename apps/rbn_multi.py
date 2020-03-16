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
        html.H1("RBN Explorer - multiple"),
        html.Div("Collective information about various RBN measurements"),
        html.Table(
            [
                html.Tr(
                    [
                        html.Td("n"),
                        html.Td(dcc.Input(id="rbn_n", type="number", value=5)),
                    ]
                ),
                html.Tr(
                    [
                        html.Td("k"),
                        html.Td(dcc.Input(id="rbn_k", type="number", value=2)),
                    ]
                ),
            ]
        ),
    ]
)
