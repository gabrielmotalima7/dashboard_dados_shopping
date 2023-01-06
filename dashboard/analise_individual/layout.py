from dash import html, dcc
import dash_bootstrap_components as dbc

header_component = html.Div([
    html.Div(id="logo"),
    html.H1("Fluxo de Shoppings (PoC) | Análise Individual", className="app-header"),
], className="header"
)


def get_layout_analise_individual(shopping_names, min_date, max_date):
    dash_app_layout = html.Div([
        header_component,
        html.Div([dcc.Dropdown(options=shopping_names, placeholder="Shopping", id="shopping_selector"),
                  dcc.DatePickerRange(
                      id="date_picker",
                      min_date_allowed=min_date,
                      max_date_allowed=max_date,
                      start_date="2022-02-01",
                      end_date="2022-02-07",
                      display_format="DD/MM/Y"
                  )
                  ]),
        dbc.Row([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Estado"),
                        html.H1(id="estado_text")
                    ])
                ], color="light"),
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Município:"),
                        html.H1(id="cidade_text"),

                    ])
                ], color="light"),
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Ano de Entrega"),
                        html.H1(id="ano_text")
                    ])
                ], color="light"),
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Área Total (m²)"),
                        html.H1(style={"color": "#e31c79"}, id="area_text"),
                    ])
                ], color="light"),
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Classe"),
                        html.H1(id="classe_text")
                    ])
                ], color="light"),
            ], className="cards")
        ], id="rowcards"),
        html.Div([
            html.Div([
                html.Div([
                    dbc.Button(id="btn_meses", children="Meses", color="light"),
                    dbc.Button(id="btn_tri", children="Trimestres", color="light"),
                    dbc.Button(id="btn_dia", children="Dias", n_clicks=1, color="light"),
                    dbc.Button(id="btn_faixa", children="Faixa Horária", color="light"),
                    html.Div(id="output_container", className="mt-4")
                ],
                    className="buttons"
                ),
                dcc.Graph(figure={}, id="visible_graph")]),
            dcc.Graph(figure={}, id="variacao_com_relacao_a_mediana"),
            dcc.Graph(figure={}, id="media_por_dia_da_semana")
        ]),
        dcc.Store(data={}, id="faixa_horaria_store"),
        dcc.Store(data={}, id="dias_store"),
        dcc.Store(data={}, id="meses_store"),
        dcc.Store(data={}, id="trimestre_store")
    ]
    )
    return dash_app_layout

# from dash import Dash
# app = Dash(__name__)
# app.layout = get_layout_analise_individual(["oi", "tchau"], "2022-01-01", "2022-02-01")
# app.run()
