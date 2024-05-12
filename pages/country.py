from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, all_cont

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
                html.Div([
                html.H3("Подробная информация о выбранной стране"),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )
    ]),

    html.Br(),

    dbc.Row ([
        dbc.Col([
            html.P("Выберите континент:")
        ],width=2),
        dbc.Col([
            dcc.Dropdown(
                id = 'crossfilter-cont',
                # заполняем дропдаун уникальными значениями континентоы из датасета
                options = [{'label': i, 'value': i} for i in all_cont],
                # значение континента, выбранное по умолчанию
                value = all_cont[0],
                # возможность множественного выбора
                multi = False
            )
        ],width=3),
        dbc.Col([
             html.P("Выберите страну:")
        ],width=2),
        dbc.Col([
             dcc.Dropdown(
                id = 'crossfilter-count',
                multi = False
            )
        ],width=3)
    ]),

    html.Br(),

        dbc.Row ([
            dbc.Col([
                dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Уровень жизни")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/img/money.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='card_text1',
                                className="card-value"),
                            )], width= 8),
                    ])
                ], color = "success", outline=True, style={'textAlign': 'center'}),
            ],width=3),
            dbc.Col([
                dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Численность населения")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/img/religious.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='card_text1',
                                className="card-value"),
                            )], width= 8),
                    ])
                ], color = "success", outline=True, style={'textAlign': 'center'}),
            ],width=3),
            dbc.Col([
                dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Образование")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/img/diploma.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='card_text1',
                                className="card-value"),
                            )], width= 8),
                    ])
                ], color = "success", outline=True, style={'textAlign': 'center'}),
            ],width=3),
            dbc.Col([
                dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Статус")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/img/globe.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='card_text1',
                                className="card-value"),
                            )], width= 8),
                    ])
                ], color = "success", outline=True, style={'textAlign': 'center'}),
            ],width=3)
    ]),

    html.Br(),
   
    dbc.Container([
        dbc.Row ([
            dbc.Col([
                html.H5('Уровень ВВп по странам континента на 2015 год'),
                dcc.Graph(id= 'choroleth', config={'displayModeBar':False}),
            ],width=8),
            dbc.Col([
                dbc.Row([
                    html.Div(id='card1')
                ]),
                html.Br(),
                dbc.Row([
                    html.H5('Топ 5 стран по ВВП'),
                    html.Div(id='table1'),
                ], style={'textAlign':'center'})
            ],width=4)
        ], style={'textAlign':'center'}),
    ])

])


@callback(
    [Output('crossfilter-count', 'options'),
    Output('crossfilter-count', 'value'),
    ],
    Input('crossfilter-cont', 'value')
)
def update_region(cont):
    all_count=df[(df['continent'] == cont)]['Country'].unique()
    dd_count = [{'label': i, 'value': i} for i in all_count]
    dd_count_value = all_count[0]
    return dd_count, dd_count_value

@callback(
    [Output ('card_text1', 'children'), 
    Output ('card_text2', 'children'), 
    Output ('card _text3', 'children'), 
    Output ('card_text4', 'children'),
    Output ('card1', 'children'), 
    Output ('table1', 'children'),
    Output('choropleth1', 'figure')
    ],
    [Input ('crossfilter-count', 'value'), 
    Input( 'crossfilter-cont', 'value'),
    ]
)









def update_card (count, cont):
    df_count=df[(df['Country'] == count)&(df['Year'] == 2015)]
    df_count14=df[(df['Country'] == count)&(df['Year'] == 2014)]
    gdp_count=df[(df['continent'] == cont)&(df['Year'] == 2015)].sort_values(by='GDP', ascending=False)

    ct1=df_count.iloc[0]['Life expectancy']
    ct2=df_count.iloc[0]['Population']
    ct3=df_count.iloc[0]['Schooling']
    ct4=df_count.iloc[0]['Status']
    gdp=df_count.iloc[0]['GDP']
    gdp_table=gdp_count.iloc[0:5][['Country','GDP']]
    delta_gpd=round((gdp15-gdp15)/gdp14, 2)*100

    card1 = dbc.Card([
        dbc.Row([
            dbc.CardHeader("Валовый внутренний продукт"),    
        ]),
        dbc.Row([
            html.Div([
                html.H5(gdp15),
                html.Div([
                    html.I(delta_gdp),
                ]),
                html.I(' в % к 2014 году'),
            ])
        ],)
    ], style={'textAlign': 'center'})

    table = dbc.Table.from_dataframe(
        gdp_table, striped=True, bordered=True, hover=True, index=False
    )