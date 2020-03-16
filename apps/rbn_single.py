# -*- coding: utf-8 -*-
import itertools
import random

import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output, State
from pyrbn import RBN

# Load extra layouts, slow!
# cyto.load_extra_layouts()

layout = html.Div(
    children=[
        html.H1("RBN Explorer - single"),
        html.Div("An explorer of Random Boolean Networks"),
        html.Table(
            [
                html.Tr(
                    [
                        html.Td("seed"),
                        html.Td(dcc.Input(id="seed", type="number", value=1)),
                    ]
                ),
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
        html.Table(
            [
                html.Tr([html.Td("cycle length"), html.Td(id="cycle_length")]),
                html.Tr([html.Td("cycle flashing"), html.Td(id="cycle_flashing")]),
                html.Tr([html.Td("cycle flashes"), html.Td(id="cycle_flashes")]),
                html.Tr([html.Td("cycle total"), html.Td(id="cycle_total")]),
                html.Tr([html.Td("cycle proportion"), html.Td(id="cycle_proportion")]),
            ]
        ),
        html.Div(
            [
                cyto.Cytoscape(
                    id="rbn-network",
                    # layout={"name": "breadthfirst", "circle":"true"},
                    layout={"name": "circle"},
                    style={"width": "100%", "height": "400px"},
                    elements=[],
                    stylesheet=[
                        {"selector": "node", "style": {"content": "data(label)"}},
                        {
                            "selector": "edge",
                            "style": {
                                # The default curve style doesnt do arrows
                                "curve-style": "bezier",
                                "target-arrow-shape": "triangle",
                                "arrow-scale": 2,
                            },
                        },
                    ],
                )
            ]
        ),
        html.Div(
            [
                cyto.Cytoscape(
                    id="state-network",
                    layout={"name": "cose"},
                    style={"width": "100%", "height": "400px"},
                    elements=[],
                )
            ]
        ),
    ]
)


@app.callback(
    [
        Output("cycle_length", "children"),
        Output("cycle_flashing", "children"),
        Output("cycle_flashes", "children"),
        Output("cycle_total", "children"),
        Output("cycle_proportion", "children"),
        Output("rbn-network", "elements"),
    ],
    [Input("seed", "value"), Input("rbn_n", "value"), Input("rbn_k", "value")],
    [State("rbn-network", "elements")],
)
def callback_seed(i, n, k, elements):
    rbn = RBN.from_random(random.Random(i), n, k)
    cycle = rbn.get_cycle()
    cycle_states = zip(*reversed(cycle))  # have a list of each nodes states

    # calculate the various statistics on the cycle
    # TODO move to pyrbn

    # number of unique states before repeating
    cycle_length = len(cycle)

    # the number of nodes that have two states
    cycle_flashing = len(
        tuple(filter(lambda x: x == 2, (len(x) for x in map(set, cycle_states))))
    )

    # the number of times a node changes state
    cycle_flashes = sum(
        (
            sum((node_states[i] != node_states[i - 1] for i in range(len(node_states))))
            for node_states in cycle_states
        )
    )

    cycle_total = sum((sum((1 if x else -1 for x in state)) for state in cycle))

    cycle_proportion = (cycle_total / (2 * n * len(cycle))) + 0.5

    #  turn the rbn into an elements object to plot
    rbn_network = []
    for i in range(n):
        label = "".join(("T" if s else "F" for s in rbn.funcs[i]))
        rbn_network.append({"data": {"id": f"{i}", "label": label}})
    for i in range(n):
        for j in range(k):
            rbn_network.append(
                {"data": {"source": f"{rbn.inputs[i][j]}", "target": f"{i}"}}
            )

    return (
        cycle_length,
        cycle_flashing,
        cycle_flashes,
        cycle_total,
        cycle_proportion,
        rbn_network,
    )


@app.callback(
    [Output("state-network", "elements")],
    [Input("seed", "value"), Input("rbn_n", "value"), Input("rbn_k", "value")],
    [State("state-network", "elements")],
)
def callback_states(i, n, k, elements):
    elements = []
    # if n is too big dont try to calculate
    # would need 2**n states
    if n >= 10:
        return elements

    rbn = RBN.from_random(random.Random(i), n, k)
    statemap = {}
    for state in itertools.product((False, True), repeat=n):
        nextstate = rbn.next_state(state)
        statemap[state] = nextstate
        node_id = "".join(("T" if s else "F" for s in state))
        elements.append({"data": {"id": node_id}})

    for state in statemap:
        node_id = "".join(("T" if s else "F" for s in state))
        node_id_next = "".join(("T" if s else "F" for s in statemap[state]))
        elements.append({"data": {"source": node_id, "target": node_id_next}})

    return (elements,)
