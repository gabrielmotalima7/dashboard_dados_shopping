import plotly.express as px
from dashboard.data_handling import FilteredShoppingData


def plot_por_faixa_horaria(filtered_shopping_data: FilteredShoppingData, time_interval: float):
    flow_by_time_interval = filtered_shopping_data.get_average_flow_by_time_interval(time_interval)
    fig = px.bar(flow_by_time_interval, x=flow_by_time_interval.index,
                 y=flow_by_time_interval.keys(), barmode="group")
    return fig


def plot_por_dia(filtered_shopping_data: FilteredShoppingData):
    flow_by_day = filtered_shopping_data.get_flow_by_day()
    fig = px.line(flow_by_day, x=flow_by_day.index, y=flow_by_day.keys())
    return fig


def plot_por_mes(filtered_shopping_data: FilteredShoppingData):
    flow_by_business_month = filtered_shopping_data.get_flow_by_month()
    fig = px.line(flow_by_business_month, x=flow_by_business_month.index, y=flow_by_business_month.keys())
    return fig


def plot_por_trimestre(filtered_shopping_data: FilteredShoppingData):
    flow_by_quarter = filtered_shopping_data.get_flow_by_quarter()
    fig = px.line(flow_by_quarter, x=flow_by_quarter.index, y=flow_by_quarter.keys())
    return fig


def plot_fluxo_medio_por_dia_da_semana(filtered_shopping_data: FilteredShoppingData):
    flow_by_week_day = filtered_shopping_data.get_average_flow_by_week_day()
    fig = px.bar(flow_by_week_day, x=flow_by_week_day.index, y=flow_by_week_day.keys())
    return fig


def plot_variacao_com_relacao_a_media(filtered_shopping_data: FilteredShoppingData):
    variacao = filtered_shopping_data.get_variacao_media_com_relacao_a_media(2)
    fig = px.bar(variacao, x=variacao.index, y=variacao.keys())
    return fig
