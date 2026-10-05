"""
Tab 1: Supply Side Analysis (อุปทานบัณฑิต & ทักษะที่เรียนมา)
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from src.theme import PLOTLY_TEMPLATE, DEGREE_COLORS, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ALERT, COLOR_BG, COLOR_SURFACE
from src.data_pipeline import pipeline, format_currency

def layout_tab1():
    return html.Div(
        className="tab-content-container p-3",
        children=[
            # Top Action & Status Bar
            html.Div(
                className="d-flex justify-content-between align-items-center mb-3 p-3 rounded-2 bg-slate-800 border border-secondary border-opacity-25",
                children=[
                    html.Div([
                        html.H4("🎓 Academic Supply Side Analysis", className="text-white fw-bold mb-0"),
                        html.Small("Analysis of university graduate production, curriculum structure, multi-year employment tracking, and tuition costs.", className="text-muted")
                    ]),
                    html.Div(
                        className="d-flex gap-2",
                        children=[
                            dbc.Button([html.Span("📥"), " Export Supply CSV"], id="tab1-export-csv-btn", color="secondary", size="sm", outline=True),
                            dbc.Button([html.Span("🔄"), " Reset Tab 1 Filter"], id="tab1-reset-btn", color="info", size="sm", outline=True),
                            dcc.Download(id="tab1-download-dataframe-csv")
                        ]
                    )
                ]
            ),
            
            # Selected Filter Indicator Badge
            html.Div(id="tab1-active-filter-alert", className="mb-3"),
            
            # 4 Linked Charts Grid (2x2)
            dbc.Row([
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("1.1 Annual Graduate Production by Program", className="chart-title mb-0"),
                                    html.Span("👆 Click any bar to cross-filter other charts", className="badge bg-primary-subtle text-info small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab1-graduates",
                                config={"displayModeBar": True, "displaylogo": False, "toImageButtonOptions": {"format": "png", "filename": "graduate_production"}},
                                style={"height": "380px"}
                            )
                        ]
                    )
                ], width=12, lg=6),
                
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("1.2 Core Courses & Target Skill Hierarchy", className="chart-title mb-0"),
                                    html.Span("🗂️ Treemap / Sunburst Drill-down", className="badge bg-secondary-subtle text-light small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab1-courses-treemap",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "380px"}
                            )
                        ]
                    )
                ], width=12, lg=6)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("1.3 Multi-Year Employment Progression (Years 1, 2, 3)", className="chart-title mb-0"),
                                    html.Span("📈 Career Outcome Tracking", className="badge bg-success-subtle text-success small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab1-employment",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "380px"}
                            )
                        ]
                    )
                ], width=12, lg=6),
                
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("1.4 Program Tuition Fee vs Salary ROI", className="chart-title mb-0"),
                                    html.Span("💰 Cost & Compensation Benchmark", className="badge bg-warning-subtle text-warning small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab1-tuition",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "380px"}
                            )
                        ]
                    )
                ], width=12, lg=6)
            ])
        ]
    )

def build_graduates_figure(df, selected_program=None):
    """Build Graph 1.1: Annual Graduate Production Bar Chart"""
    agg = df.groupby(["program_name", "year", "degree"], as_index=False)["graduates_count"].sum()
    
    fig = px.bar(
        agg,
        x="program_name",
        y="graduates_count",
        color="degree",
        barmode="group",
        color_discrete_map=DEGREE_COLORS,
        custom_data=["program_name", "degree", "year"]
    )
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title="Annual Graduates by Program & Degree Level",
        xaxis_title="",
        yaxis_title="Total Graduates",
        xaxis_tickangle=-30,
        legend_title_text="Degree Level"
    )
    
    # Highlight selected program if any
    if selected_program:
        for trace in fig.data:
            trace.opacity = 0.3
        fig.add_annotation(
            text=f"Selected: {selected_program}",
            xref="paper", yref="paper",
            x=0.98, y=0.95, showarrow=False,
            font={"color": COLOR_PRIMARY, "size": 12},
            bgcolor="rgba(15, 23, 42, 0.8)", bordercolor=COLOR_PRIMARY, borderwidth=1
        )
    return fig

def build_courses_treemap_figure(courses_df, selected_program=None):
    """Build Graph 1.2: Core Courses and Skill Alignment Treemap"""
    fig = px.treemap(
        courses_df,
        path=["category", "core_skill", "course_name"],
        values="credits",
        color="category",
        color_discrete_sequence=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ALERT]
    )
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title="Curriculum Knowledge Hierarchy (Credits by Category & Skill)",
        margin={"l": 10, "r": 10, "t": 40, "b": 10}
    )
    return fig

def build_employment_figure(df, selected_program=None):
    """Build Graph 1.3: Multi-Year Employment Tracking (Years 1, 2, 3)"""
    agg = df.groupby("program_name", as_index=False).agg({
        "emp_rate_year1": "mean",
        "emp_rate_year2": "mean",
        "emp_rate_year3": "mean",
        "direct_field_match_pct": "mean"
    })
    
    if selected_program and selected_program in agg["program_name"].values:
        agg = agg[agg["program_name"] == selected_program]
        
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Year 1 Employed (%)",
        x=agg["program_name"],
        y=agg["emp_rate_year1"],
        marker_color=COLOR_PRIMARY
    ))
    fig.add_trace(go.Bar(
        name="Year 2 Employed (%)",
        x=agg["program_name"],
        y=agg["emp_rate_year2"],
        marker_color=COLOR_SECONDARY
    ))
    fig.add_trace(go.Bar(
        name="Year 3 Employed (%)",
        x=agg["program_name"],
        y=agg["emp_rate_year3"],
        marker_color=COLOR_SUCCESS
    ))
    fig.add_trace(go.Scatter(
        name="Direct Field Match (%)",
        x=agg["program_name"],
        y=agg["direct_field_match_pct"],
        mode="lines+markers",
        line={"color": COLOR_ALERT, "width": 3},
        marker={"size": 8}
    ))
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title="Graduate Employment Rates Over Time (Years 1–3 Post Graduation)",
        barmode="group",
        xaxis_title="",
        yaxis_title="Employment Rate (%)",
        xaxis_tickangle=-30,
        yaxis={"range": [0, 105]}
    )
    return fig

def build_tuition_figure(df, currency="USD ($)", selected_program=None):
    """Build Graph 1.4: Tuition Fee Comparison & Starting Salary"""
    agg = df.groupby(["program_name", "degree", "country"], as_index=False).agg({
        "tuition_fee_usd": "mean",
        "avg_starting_salary_usd": "mean"
    })
    
    rate = 36.5 if currency == "THB (฿)" else (0.92 if currency == "EUR (€)" else 1.0)
    symbol = "฿" if currency == "THB (฿)" else ("€" if currency == "EUR (€)" else "$")
    
    agg["tuition_converted"] = agg["tuition_fee_usd"] * rate
    agg["salary_converted"] = agg["avg_starting_salary_usd"] * rate
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=f"Total Tuition Fee ({symbol})",
        x=agg["program_name"],
        y=agg["tuition_converted"],
        marker_color=COLOR_WARNING
    ))
    fig.add_trace(go.Bar(
        name=f"Avg Starting Salary ({symbol})",
        x=agg["program_name"],
        y=agg["salary_converted"],
        marker_color=COLOR_SUCCESS
    ))
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title=f"Program Investment (Tuition Fee) vs Starting Compensation ({currency})",
        barmode="group",
        xaxis_title="",
        yaxis_title=f"Amount in {currency}",
        xaxis_tickangle=-30
    )
    return fig
