from dash import html, dcc


header_component = html.Div([
    html.Div(id='logo'),
    html.H1('Fluxo de Shoppings (PoC) | Análise Comparativa', className='app-header'),
], className='header'
)


def get_layout_analise_comparativa(state_names, min_date, max_date):
    dash_app_layout = html.Div([
        header_component,
        html.Div([dcc.Dropdown(options=state_names,
                               placeholder="Estado",
                               id="estado"),
                  dcc.Dropdown(options=[],
                               placeholder="Cidade",
                               id="cidade",
                               multi=True),
                  dcc.Dropdown(options=[],
                               placeholder="Shoppings",
                               id="shoppings", multi=True),
                  dcc.DatePickerRange(
                      id="date_picker",
                      min_date_allowed=min_date,
                      max_date_allowed=max_date,
                      start_date='2022-02-01',
                      end_date='2022-02-07',
                      display_format='DD/MM/Y'
                  )
                  ]),
        html.Div([dcc.Graph(figure={}, id="evolucao_horaria"),
                  dcc.Graph(figure={}, id="fluxo_agregado"),
                  dcc.Graph(figure={}, id="faixa_horaria")]),
        html.Div([dcc.Dropdown(options=state_names, placeholder="Estado", id="filtro_estado")]),
        html.Div([dcc.Graph(figure={}, id="fluxo_por_municipio")])
    ])
    return dash_app_layout
