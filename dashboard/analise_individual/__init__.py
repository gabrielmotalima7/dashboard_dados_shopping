from dash import Dash
from .callbacks import CALLBACK_MANAGER, SHOPPING_LIST, MAX_DATE, MIN_DATE
from .layout import get_layout_analise_individual

def init_dashboard_analise_individual(server):
    app = Dash(
        server=server,
        routes_pathname_prefix="/analise-individual/"
    )
    app.layout = get_layout_analise_individual(SHOPPING_LIST, MIN_DATE, MAX_DATE)
    CALLBACK_MANAGER.attach_to_app(app)
    return app.server