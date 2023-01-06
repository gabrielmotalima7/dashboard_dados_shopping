from dashboard.callback_manager import CallBackManager
from dashboard.data_handling import FilteredShoppingData, GlobalShoppingData
from dash import Input, Output, ctx
from dash.exceptions import PreventUpdate
from .graphs import *
from datetime import datetime

CALLBACK_MANAGER = CallBackManager()
FLOW_DATA_PATH = "data/contagem_ids_por_hora_shoppings_mock.csv"
SHOPPING_INFO_PATH = "data/Shoppings_SiiLA_estoque existente.xlsx"
DATA_HOLDER = GlobalShoppingData.create_data_holder_from_files(FLOW_DATA_PATH, SHOPPING_INFO_PATH)
SHOPPING_LIST = DATA_HOLDER.get_shopping_names()
MIN_DATE = DATA_HOLDER.get_min_date()
MAX_DATE = DATA_HOLDER.get_max_date()

def parse_date(date_str: str):
    date_object = datetime.strptime(date_str, "%Y-%m-%d")
    return date_object

@CALLBACK_MANAGER.callback([Output("faixa_horaria_store", "data"),
                            Output("dias_store", "data"),
                            Output("meses_store", "data"),
                            Output("trimestre_store", "data")],
                           [Input("shopping_selector", "value"),
                            Input("date_picker", "start_date"),
                            Input("date_picker", "end_date"),
                            Input("faixa_horaria_store", "data"), Input("dias_store", "data"),
                            Input("meses_store", "data"), Input("trimestre_store", "data")
                            ])
def update_stored_graphs(selected_shopping, start_date, end_date, *stored_plots):
    if selected_shopping in SHOPPING_LIST and start_date < end_date:
        start_date, end_date = parse_date(start_date), parse_date(end_date)
        filtered_data = FilteredShoppingData.create_filtered_data(DATA_HOLDER, [selected_shopping], start_date, end_date)
        faixa_horaria = plot_por_faixa_horaria(filtered_data, 2)
        dados_diarios = plot_por_dia(filtered_data)
        dados_mensais = plot_por_mes(filtered_data)
        dados_trimestrais = plot_por_trimestre(filtered_data)
        print(dados_mensais)
        return faixa_horaria, dados_diarios, dados_mensais, dados_trimestrais
    else:
        return stored_plots


@CALLBACK_MANAGER.callback(Output("visible_graph", "figure"),
                           [Input("btn_meses", "n_clicks"),
                            Input("meses_store", "data"),
                            Input("visible_graph", "figure")])
def set_monthly_plot_as_visible(monthly_button, meses_store, visible_graph):
    if "btn_meses" != ctx.triggered_id:
        raise PreventUpdate()
    return meses_store


@CALLBACK_MANAGER.callback(Output("visible_graph", "figure"),
                           [Input("btn_tri", "n_clicks"),
                            Input("trimestre_store", "data"),
                            Input("visible_graph", "figure")])
def set_quarterly_graph_as_visible(quarterly_button, trimestres_store, visible_graph):
    if "btn_tri" != ctx.triggered_id:
         raise PreventUpdate()
    return trimestres_store

def update_secondary_graphs(): pass


def update_cards(): pass