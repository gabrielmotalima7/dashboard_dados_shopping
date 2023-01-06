import plotly.express as px
from dashboard.data_handling import FilteredShoppingData


def plot_flow_data_serie(filtered_shopping_data: FilteredShoppingData):
    flow_series = filtered_shopping_data.get_flow_series()
    fig = px.line(flow_series, x=flow_series.index, y=flow_series.keys())
    return fig


def plot_flow_by_time_interval(filtered_shopping_data: FilteredShoppingData, time_interval: float):
    flow_by_time_interval = filtered_shopping_data.get_average_flow_by_time_interval(time_interval)
    fig = px.bar(flow_by_time_interval, x=flow_by_time_interval.index,
                 y=flow_by_time_interval.keys(), barmode="group")
    return fig


def plot_aggregate_flow(filtered_shopping_data: FilteredShoppingData):
    aggregate_flow = filtered_shopping_data.get_aggregate_flow()
    fig = px.bar(aggregate_flow)
    return fig


def plot_flow_by_city(filtered_shopping_data: FilteredShoppingData, state_name: str):
    flow_by_city = filtered_shopping_data.get_flow_by_city_in_state(state_name)
    fig = px.line(flow_by_city, x=flow_by_city.index, y=flow_by_city.keys())
    return fig


def plot_flow_by_state(filtered_shopping_data: FilteredShoppingData):
    flow_by_state = filtered_shopping_data.get_flow_by_state()
    fig = px.line(flow_by_state, x=flow_by_state.index, y=flow_by_state.keys())
    return fig
