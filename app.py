# -*- coding: utf-8 -*-
import dash

# shared global application instance, used to register callbacks by layouts
app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
