# -*- coding: utf-8 -*-
import collections
import random
import statistics

import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output
from pyrbn import RBN

layout = html.Div(
    children=[
        html.H1("RBN Explorer - multiple"),
        html.Div("Collective information about various RBN measurements"),
        html.Table(
            [
                html.Tr(
                    [
                        html.Td("n (min)"),
                        html.Td(dcc.Input(id="rbn_n_min", type="number", value=5)),
                    ]
                ),
                html.Tr(
                    [
                        html.Td("n (max"),
                        html.Td(dcc.Input(id="rbn_n_max", type="number", value=25)),
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
        dcc.Graph(id="cycle-length", figure={}),
    ]
)


@app.callback(
    [Output("cycle-length", "figure")],
    [Input("rbn_n_min", "value"), Input("rbn_n_max", "value"), Input("rbn_k", "value")],
)
def callback_seed(n_min, n_max, k):
    if n_min is None:
        return [{}]
    if n_max is None:
        return [{}]
    if n_max < n_min + 10:
        return [{}]

    # median
    # area plot Q1 & Q3
    # area plot lower/upper inner fence (Q1 - 1.5*IQ, Q3 + 1.5*IQ)
    # TODO area plot lower/upper output fence (Q1 - 3*IQ, Q3 + 3*IQ)
    # TODO extreme outliers as semi-transparent dots

    counters = []
    ns = list(range(n_min, n_max + 1, (n_max - n_min) // 10))
    for n in ns:
        lengths = collections.Counter()
        for i in range(1000):
            rbn = RBN.from_random(random.Random(i), n, k)
            cycle = rbn.get_cycle()
            cycle_len = len(cycle)
            lengths[cycle_len] += 1
        counters.append(lengths)
        # data = {"y": tuple(lengths.elements()), "type": "box", "name": f"n={n}"}
        # datas.append(data)

    lower_inner_fences = []
    lower_quartiles = []
    medians = []
    upper_quartiles = []
    upper_inner_fences = []
    for n, counter in zip(ns, counters):
        # requires pyhton 3.8+
        lower_quartile, median, upper_quartile = statistics.quantiles(
            counter.elements()
        )
        inter_quartile = upper_quartile - lower_quartile
        min_n = min(counter.elements())
        max_n = max(counter.elements())
        lower_inner_fence = max((min_n, lower_quartile - (1.5 * inter_quartile)))
        upper_inner_fence = min((max_n, upper_quartile + (1.5 * inter_quartile)))

        lower_inner_fences.append(lower_inner_fence)
        lower_quartiles.append(lower_quartile)
        medians.append(median)
        upper_quartiles.append(upper_quartile)
        upper_inner_fences.append(upper_inner_fence)

    figure = {
        "data": [
            {"x": ns, "y": medians, "name": "median"},
            {"x": ns, "y": lower_inner_fences, "name": "lower inner fence"},
            {
                "x": ns,
                "y": upper_inner_fences,
                "fill": "tonexty",
                "name": "upper inner fence",
            },
            {"x": ns, "y": lower_quartiles, "name": "lower quartile"},
            {
                "x": ns,
                "y": upper_quartiles,
                "fill": "tonexty",
                "name": "upper quartile",
            },
        ],
        "layout": {
            "title": "RBN Cycle Length",
            # "yaxis": {"type": "log"},
        },
    }
    return (figure,)
