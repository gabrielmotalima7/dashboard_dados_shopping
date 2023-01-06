from dash import Dash
from .callbacks import CALLBACK_MANAGER, STATE_NAMES, DATA_HOLDER, MIN_DATE, MAX_DATE
from .layout import get_layout_analise_comparativa

def init_dashboard_analise_comparativa(server):
    app = Dash(
        server=server,
        routes_pathname_prefix="/analise-comparativa/"
    )
    app.layout = get_layout_analise_comparativa(STATE_NAMES, MIN_DATE, MAX_DATE)
    CALLBACK_MANAGER.attach_to_app(app)
    return app.server

