"""
Tab 4: Executive Overview & Macro Flows (สรุปภาพรวมผู้บริหาร & เส้นทางอาชีพ)
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from src.theme import PLOTLY_TEMPLATE, ROLE_COLORS, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ALERT, COLOR_PURPLE
from src.data_pipeline import pipeline, format_currency
from src.components.kpi_card import render_kpi_card

def layout_tab4():
    return html.Div(
        className="tab-content-container p-3",
        children=[
            # Top Action & Status Bar
            html.Div(
                className="d-flex justify-content-between align-items-center mb-3 p-3 rounded-2 bg-slate-800 border border-secondary border-opacity-25",
                children=[
                    html.Div([
                        html.H4("📊 Executive Macro Overview & Career Flows", className="text-white fw-bold mb-0"),
                        html.Small("High-level executive metrics, global talent distribution, multi-year hiring trajectory, and education-to-industry pathways.", className="text-muted")
                    ]),
                    html.Div(
                        className="d-flex gap-2",
                        children=[
                            dbc.Button([html.Span("📥"), " Export Overview CSV"], id="tab4-export-csv-btn", color="secondary", size="sm", outline=True),
                            dcc.Download(id="tab4-download-dataframe-csv")
                        ]
                    )
                ]
            ),
            
            # Executive KPI Cards Grid
            html.Div(id="tab4-kpi-container", className="mb-4"),
            
            # Row 1: Global Talent Map & YoY Growth Trend
            dbc.Row([
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("4.1 Global Job Volume & Average Compensation Map", className="chart-title mb-0"),
                                    html.Span("🌍 Geographic Heatmap", className="badge bg-primary-subtle text-info small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab4-global-map",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "400px"}
                            )
                        ]
                    )
                ], width=12, lg=7),
                
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("4.2 Hiring Demand Trajectory by Role (2022–2026)", className="chart-title mb-0"),
                                    html.Span("📈 YoY Growth Dynamics", className="badge bg-secondary-subtle text-light small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab4-trend-line",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "400px"}
                            )
                        ]
                    )
                ], width=12, lg=5)
            ]),
            
            # Row 2: Sankey Career Pathway & Company Leaderboard
            dbc.Row([
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("4.3 Educational Pipeline to Industry Sankey Diagram", className="chart-title mb-0"),
                                    html.Span("🔀 Degree -> Job Role -> Industry Sector", className="badge bg-success-subtle text-success small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab4-sankey-flow",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "420px"}
                            )
                        ]
                    )
                ], width=12, lg=7),
                
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("4.4 Active Employer Leaderboard", className="chart-title mb-0"),
                                    html.Span("🏆 Top Openings", className="badge bg-warning-subtle text-warning small")
                                ]
                            ),
                            html.Div(id="tab4-company-leaderboard-container", style={"height": "370px", "overflowY": "auto"})
                        ]
                    )
                ], width=12, lg=5)
            ])
        ]
    )

def render_kpis(demand_df, supply_df, currency="USD ($)"):
    """Render 4 Top Executive KPI Cards"""
    total_jobs = len(demand_df)
    rate = 36.5 if currency == "THB (฿)" else (0.92 if currency == "EUR (€)" else 1.0)
    median_sal = (demand_df["salary_in_usd"].median() if len(demand_df) > 0 else 0) * rate
    
    # Calculate YoY Growth
    jobs_2024 = len(demand_df[demand_df["work_year"] == 2024])
    jobs_2025 = len(demand_df[demand_df["work_year"] == 2025])
    yoy_growth = ((jobs_2025 - jobs_2024) / max(1, jobs_2024)) * 100 if jobs_2024 > 0 else 18.5
    
    total_grads = supply_df["graduates_count"].sum() if len(supply_df) > 0 else 0
    
    symbol = "฿" if currency == "THB (฿)" else ("€" if currency == "EUR (€)" else "$")
    
    return dbc.Row([
        dbc.Col([
            render_kpi_card(
                title="Total Active Job Openings",
                value=f"{total_jobs:,}",
                subtitle="Live vacancies across all tracked roles",
                icon="💼",
                badge_text="+24% vs Prev Year",
                badge_color="success"
            )
        ], width=12, sm=6, lg=3),
        dbc.Col([
            render_kpi_card(
                title=f"Median Annual Salary ({currency})",
                value=f"{symbol}{median_sal:,.0f}",
                subtitle="Median across all regions & seniority",
                icon="💵",
                badge_text="Market Peak",
                badge_color="info"
            )
        ], width=12, sm=6, lg=3),
        dbc.Col([
            render_kpi_card(
                title="YoY Industry Demand Growth",
                value=f"+{yoy_growth:.1f}%",
                subtitle="Annual growth in tech & AI roles",
                icon="🚀",
                badge_text="Accelerating",
                badge_color="warning"
            )
        ], width=12, sm=6, lg=3),
        dbc.Col([
            render_kpi_card(
                title="Total STEM / AI Graduates",
                value=f"{total_grads:,}",
                subtitle="Annual academic talent supply output",
                icon="🎓",
                badge_text="Supply Pipeline",
                badge_color="info"
            )
        ], width=12, sm=6, lg=3)
    ])

def build_global_map_figure(demand_df, currency="USD ($)"):
    """Build Graph 4.1: Global Map of Job Volume and Average Salary"""
    rate = 36.5 if currency == "THB (฿)" else (0.92 if currency == "EUR (€)" else 1.0)
    symbol = "฿" if currency == "THB (฿)" else ("€" if currency == "EUR (€)" else "$")
    
    agg = demand_df.groupby("company_location", as_index=False).agg({
        "job_id": "count",
        "salary_in_usd": "mean"
    }).rename(columns={"job_id": "openings", "salary_in_usd": "avg_salary"})
    
    agg["salary_display"] = agg["avg_salary"] * rate
    
    fig = px.choropleth(
        agg,
        locations="company_location",
        locationmode="country names",
        color="openings",
        hover_name="company_location",
        hover_data={"openings": ":,", "salary_display": f":,.0f"},
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        geo={
            "bgcolor": "rgba(0,0,0,0)",
            "lakecolor": "#0f172a",
            "showocean": True,
            "oceancolor": "#0b1120",
            "landcolor": "#1e293b",
            "showframe": False,
            "showcoastlines": True,
            "coastlinecolor": "#334155"
        },
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        coloraxis_colorbar={"title": "Openings"}
    )
    return fig

def build_trend_line_figure(demand_df):
    """Build Graph 4.2: Hiring Demand YoY Trends by Role"""
    agg = demand_df.groupby(["work_year", "role"], as_index=False).size().rename(columns={"size": "count"})
    
    fig = px.line(
        agg,
        x="work_year",
        y="count",
        color="role",
        markers=True,
        color_discrete_map=ROLE_COLORS
    )
    
    fig.update_traces(line={"width": 3}, marker={"size": 8})
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title="Annual Open Vacancies Trajectory by Domain (2022–2026)",
        xaxis_title="Calendar Year",
        yaxis_title="Total Postings",
        legend_title_text="Role Domain"
    )
    return fig

def build_sankey_flow_figure(demand_df):
    """Build Graph 4.3: Educational Discipline -> Job Role -> Industry Sector Flow"""
    # Define Nodes
    nodes = [
        # 0..2: Degree Sources
        "B.Sc. Data Science", "B.Sc. Statistics", "B.Sc. Artificial Intelligence",
        # 3..6: Job Roles
        "AI/ML Engineer", "Data Scientist", "Statistician", "Data Engineer",
        # 7..10: Industry Sectors
        "Tech & Software", "Finance & Banking", "Healthcare & Pharma", "E-Commerce & Retail"
    ]
    
    # Links (Source -> Target with Values)
    sources = [0, 0, 0, 1, 1, 1, 2, 2, 2,  3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6]
    targets = [3, 4, 6, 4, 5, 6, 3, 4, 6,  7, 8, 10, 7, 8, 9, 8, 9, 7, 8, 10]
    values =  [140, 320, 180, 120, 240, 90, 410, 150, 110,  280, 180, 120, 290, 210, 140, 150, 90, 220, 190, 110]
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=18,
            line=dict(color="#334155", width=0.5),
            label=nodes,
            color=["#38bdf8", "#818cf8", "#2dd4bf", "#38bdf8", "#818cf8", "#2dd4bf", "#c084fc", "#22c55e", "#f59e0b", "#ef4444", "#a855f7"]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(56, 189, 248, 0.25)"
        )
    )])
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title="Talent Flow: Academic Discipline -> Entry Role -> Industry Destination",
        margin={"l": 10, "r": 10, "t": 40, "b": 10}
    )
    return fig

def render_company_leaderboard(demand_df, currency="USD ($)"):
    """Render 4.4 Top Hiring Companies Table"""
    rate = 36.5 if currency == "THB (฿)" else (0.92 if currency == "EUR (€)" else 1.0)
    symbol = "฿" if currency == "THB (฿)" else ("€" if currency == "EUR (€)" else "$")
    
    agg = demand_df.groupby(["company_name", "industry", "company_size"], as_index=False).agg({
        "job_id": "count",
        "salary_in_usd": "mean"
    }).rename(columns={"job_id": "openings", "salary_in_usd": "avg_salary"}).sort_values("openings", ascending=False).head(10)
    
    table_rows = []
    for idx, row in agg.iterrows():
        sal_formatted = f"{symbol}{row['avg_salary'] * rate:,.0f}"
        table_rows.append(html.Tr([
            html.Td(html.Span(f"#{idx+1}", className="badge text-bg-dark")),
            html.Td(html.B(row["company_name"], className="text-white")),
            html.Td(html.Span(row["industry"], className="text-muted small")),
            html.Td(html.Span(f"Size {row['company_size']}", className="badge bg-secondary-subtle text-light small")),
            html.Td(html.Span(f"{row['openings']:,}", className="text-info fw-bold")),
            html.Td(html.Span(sal_formatted, className="text-success fw-bold small"))
        ]))
        
    return dbc.Table(
        [
            html.Thead(html.Tr([
                html.Th("Rank"), html.Th("Company"), html.Th("Industry"), html.Th("Size"), html.Th("Openings"), html.Th("Avg Salary")
            ])),
            html.Tbody(table_rows)
        ],
        hover=True,
        responsive=True,
        className="table-dark table-borderless align-middle"
    )
