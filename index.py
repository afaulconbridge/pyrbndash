# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from app import app
from apps import index, rbn_multi, rbn_single
from dash.dependencies import Input, Output

# shared layout for all child apps
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),  # url address bar
        html.Div(id="page-content"),  # main content pane
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return index.layout
    elif pathname == "/rbn-single":
        return rbn_single.layout
    elif pathname == "/rbn-multi":
        return rbn_multi.layout
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=True)
