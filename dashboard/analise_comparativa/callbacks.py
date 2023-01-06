from datetime import datetime
from dashboard.callback_manager import CallBackManager
from dash import Input, Output
from dash.exceptions import PreventUpdate
from dashboard.data_handling import FilteredShoppingData, GlobalShoppingData
from .graphs import *
from typing import List

FLOW_DATA_PATH = "data/contagem_ids_por_hora_shoppings_mock.csv"
SHOPPING_INFO_PATH = "data/Shoppings_SiiLA_estoque existente.xlsx"
DATA_HOLDER = GlobalShoppingData.create_data_holder_from_files(FLOW_DATA_PATH, SHOPPING_INFO_PATH)
STATE_NAMES = DATA_HOLDER.get_state_names()
CITY_NAMES = DATA_HOLDER.get_city_names()
SHOPPING_NAMES = DATA_HOLDER.get_shopping_names()
MIN_DATE = DATA_HOLDER.get_min_date()
MAX_DATE = DATA_HOLDER.get_max_date()
CALLBACK_MANAGER = CallBackManager()


def parse_date(date_str: str):
    date_object = datetime.strptime(date_str, "%Y-%m-%d")
    return date_object


@CALLBACK_MANAGER.callback(Output("cidade", "options"),
                           Input("estado", "value"),
                           Input("cidade", "value"))
def set_selectable_cities(state_name: str, selected_cities: List[str]) -> List[str]:
    if not state_name in STATE_NAMES:
        raise PreventUpdate()
    city_names = DATA_HOLDER.get_cities_in_state(state_name)
    city_names = city_names + selected_cities if selected_cities else city_names
    return city_names


@CALLBACK_MANAGER.callback(Output("shoppings", "options"),
                           [Input("cidade", "value"),
                           Input("shoppings", "value")])
def set_selectable_shoppings(cities: List[str], selected_shoppings: List[str]) -> List[str]:
    if not cities:
        raise PreventUpdate()
    valid_city_names = [city_name for city_name in cities if city_name in CITY_NAMES]
    shopping_names = DATA_HOLDER.get_shoppings_in_cities(valid_city_names)
    shopping_names = shopping_names + selected_shoppings if selected_shoppings else shopping_names
    return shopping_names


@CALLBACK_MANAGER.callback([Output("evolucao_horaria", "figure"), Output("fluxo_agregado", "figure"),
                            Output("faixa_horaria", "figure")],
                           [Input("shoppings", "value"), Input("date_picker", "start_date"),
                            Input("date_picker", "end_date"),
                            Input("evolucao_horaria", "figure"),
                            Input("fluxo_agregado", "figure"), Input("faixa_horaria", "figure")])
def update_shopping_specific_graphs(shoppings: List[str], start_date: str, end_date: str, *old_maps):
    if shoppings and start_date < end_date:
        start_date, end_date = parse_date(start_date), parse_date(end_date)
        filtered_data = FilteredShoppingData.create_filtered_data(DATA_HOLDER, shoppings, start_date, end_date)
        grafico_evolucao_horaria = plot_flow_data_serie(filtered_data)
        grafico_fluxo_agregado = plot_aggregate_flow(filtered_data)
        grafico_faixa_horaria = plot_flow_by_time_interval(filtered_data, time_interval=1.5)
        return grafico_evolucao_horaria, grafico_fluxo_agregado, grafico_faixa_horaria
    else:
        return old_maps


@CALLBACK_MANAGER.callback(Output("fluxo_por_municipio", "figure"),
                           [Input("filtro_estado", "value"),
                            Input("date_picker", "start_date"),
                            Input("date_picker", "end_date"),
                            Input("fluxo_por_municipio", "figure"),
                            ])
def update_city_specific_graphs(state_name, start_date, end_date, old_map):
    print("*******************************************************", state_name)
    if state_name in STATE_NAMES and start_date < end_date:
        start_date, end_date = parse_date(start_date), parse_date(end_date)
        filtered_data = FilteredShoppingData(DATA_HOLDER)
        filtered_data.set_date_bounds(start_date, end_date)
        return plot_flow_by_city(filtered_data, state_name)
    else:
        return old_map
