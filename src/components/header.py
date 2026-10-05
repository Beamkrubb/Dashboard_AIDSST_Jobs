"""
Dashboard Header & Global Filter Controls Component
"""
from dash import html, dcc
import dash_bootstrap_components as dbc

def render_header():
    return html.Div(
        className="app-header mb-4 p-4 rounded-3",
        children=[
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Span("🚀 ANTIGRAVITY INTELLIGENCE", className="badge text-bg-primary px-3 py-1 mb-2 fw-semibold text-uppercase"),
                        html.H1("AI, Data Science & Statistics Workforce & Skill Mismatch Dashboard", className="fw-bold fs-3 text-white mb-1"),
                        html.P("Real-Time Analytics on Academic Supply, Market Demand Dynamics, and Skill Gap Alignment", className="text-secondary mb-0")
                    ])
                ], width=12, lg=8),
                dbc.Col([
                    html.Div(
                        className="d-flex justify-content-lg-end align-items-center gap-2 mt-3 mt-lg-0",
                        children=[
                            html.Div([
                                html.Span("Currency", className="filter-label d-block text-muted small"),
                                dcc.RadioItems(
                                    id="global-currency-toggle",
                                    options=[
                                        {"label": " USD ($)", "value": "USD ($)"},
                                        {"label": " THB (฿)", "value": "THB (฿)"},
                                        {"label": " EUR (€)", "value": "EUR (€)"}
                                    ],
                                    value="USD ($)",
                                    inline=True,
                                    className="custom-radio-group"
                                )
                            ], className="px-3 py-2 bg-dark rounded border border-secondary border-opacity-25"),
                            dbc.Button(
                                [html.Span("🔄"), " Reset All"],
                                id="global-reset-all-btn",
                                color="outline-info",
                                size="sm",
                                className="px-3 py-2 fw-semibold"
                            )
                        ]
                    )
                ], width=12, lg=4)
            ]),
            
            # Global Filter Bar
            html.Div(
                className="filter-panel mt-4 p-3 rounded-2 border border-secondary border-opacity-25",
                children=[
                    dbc.Row([
                        dbc.Col([
                            html.Label("🌍 Region / Country", className="filter-label text-info fw-semibold small"),
                            dcc.Dropdown(
                                id="global-country-filter",
                                options=[
                                    {"label": "🌐 Global (All Countries)", "value": "All"},
                                    {"label": "🇹🇭 Thailand", "value": "Thailand"},
                                    {"label": "🇺🇸 United States", "value": "United States"},
                                    {"label": "🇬🇧 United Kingdom", "value": "United Kingdom"},
                                    {"label": "🇩🇪 Germany", "value": "Germany"},
                                    {"label": "🇸🇬 Singapore", "value": "Singapore"},
                                    {"label": "🇨🇦 Canada", "value": "Canada"},
                                    {"label": "🇯🇵 Japan", "value": "Japan"},
                                    {"label": "🇦🇺 Australia", "value": "Australia"}
                                ],
                                value=["All"],
                                multi=True,
                                placeholder="Select countries...",
                                className="custom-dropdown"
                            )
                        ], width=12, md=3),
                        
                        dbc.Col([
                            html.Label("🎯 Role Category", className="filter-label text-info fw-semibold small"),
                            dcc.Dropdown(
                                id="global-role-filter",
                                options=[
                                    {"label": "🌟 All Roles", "value": "All Roles"},
                                    {"label": "🤖 AI/ML Engineer", "value": "AI/ML Engineer"},
                                    {"label": "📊 Data Scientist", "value": "Data Scientist"},
                                    {"label": "📈 Statistician", "value": "Statistician"},
                                    {"label": "⚙️ Data Engineer", "value": "Data Engineer"}
                                ],
                                value="All Roles",
                                clearable=False,
                                className="custom-dropdown"
                            )
                        ], width=12, md=3),
                        
                        dbc.Col([
                            html.Label("💼 Career Level", className="filter-label text-info fw-semibold small"),
                            dcc.Dropdown(
                                id="global-exp-filter",
                                options=[
                                    {"label": "🌱 Entry-Level (EN)", "value": "Entry-Level (EN)"},
                                    {"label": "🚀 Mid-Level (MI)", "value": "Mid-Level (MI)"},
                                    {"label": "⭐ Senior / Lead (SE)", "value": "Senior / Lead (SE)"},
                                    {"label": "👑 Executive / Expert (EX)", "value": "Executive / Expert (EX)"}
                                ],
                                value=["Entry-Level (EN)", "Mid-Level (MI)", "Senior / Lead (SE)", "Executive / Expert (EX)"],
                                multi=True,
                                className="custom-dropdown"
                            )
                        ], width=12, md=3),
                        
                        dbc.Col([
                            html.Label("📅 Year Range (2022 - 2026)", className="filter-label text-info fw-semibold small"),
                            dcc.RangeSlider(
                                id="global-year-slider",
                                min=2022,
                                max=2026,
                                step=1,
                                marks={y: {"label": str(y), "style": {"color": "#94a3b8"}} for y in range(2022, 2027)},
                                value=[2022, 2026],
                                className="custom-slider pt-2"
                            )
                        ], width=12, md=3)
                    ])
                ]
            )
        ]
    )
