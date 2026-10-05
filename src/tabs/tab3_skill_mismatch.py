"""
Tab 3: Skill Mismatch & Gap Intelligence (Supply vs Demand Analysis)
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from src.theme import PLOTLY_TEMPLATE, QUADRANT_COLORS, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ALERT, COLOR_TEXT_MUTED
from src.data_pipeline import pipeline, format_currency

def layout_tab3():
    return html.Div(
        className="tab-content-container p-3",
        children=[
            # Top Action & Status Bar
            html.Div(
                className="d-flex justify-content-between align-items-center mb-3 p-3 rounded-2 bg-slate-800 border border-secondary border-opacity-25",
                children=[
                    html.Div([
                        html.H4("⚠️ Skill Mismatch & Gap Intelligence Matrix", className="text-white fw-bold mb-0"),
                        html.Small("Evaluating the structural misalignment between academic curricula (Supply) and labor market requirements (Demand).", className="text-muted")
                    ]),
                    html.Div(
                        className="d-flex gap-2",
                        children=[
                            dbc.Button([html.Span("📥"), " Export Mismatch CSV"], id="tab3-export-csv-btn", color="secondary", size="sm", outline=True),
                            dbc.Button([html.Span("🔄"), " Reset Tab 3 Filter"], id="tab3-reset-btn", color="info", size="sm", outline=True),
                            dcc.Download(id="tab3-download-dataframe-csv")
                        ]
                    )
                ]
            ),
            
            # Selected Filter Indicator Alert
            html.Div(id="tab3-active-filter-alert", className="mb-3"),
            
            # Strategic Action Recommendation Cards Banner
            dbc.Row([
                dbc.Col([
                    html.Div(
                        className="p-3 rounded-3 mb-4 border border-danger border-opacity-50 bg-danger bg-opacity-10",
                        children=[
                            html.H6("🚨 Priority Deficit Skills (High Demand / Low Supply)", className="text-danger fw-bold mb-1"),
                            html.P("RAG & LLM Applications, MLOps & CI/CD, Cloud Data Warehouses, Docker. Curricula should urgently integrate hands-on project labs.", className="small text-white mb-0")
                        ]
                    )
                ], width=12, md=4),
                dbc.Col([
                    html.Div(
                        className="p-3 rounded-3 mb-4 border border-success border-opacity-50 bg-success bg-opacity-10",
                        children=[
                            html.H6("✅ Well-Aligned Core Skills (High Demand / High Supply)", className="text-success fw-bold mb-1"),
                            html.P("Python, SQL, Linear Algebra, Machine Learning Foundations, Problem Solving. Maintain depth and rigorous standards.", className="small text-white mb-0")
                        ]
                    )
                ], width=12, md=4),
                dbc.Col([
                    html.Div(
                        className="p-3 rounded-3 mb-4 border border-warning border-opacity-50 bg-warning bg-opacity-10",
                        children=[
                            html.H6("🔄 Surplus / Legacy Tech (Low Demand / High Supply)", className="text-warning fw-bold mb-1"),
                            html.P("SAS/SPSS Legacy Software, Manual Calculus drills. Consider converting compulsory hours to Modern Python/Cloud stacks.", className="small text-white mb-0")
                        ]
                    )
                ], width=12, md=4)
            ]),
            
            # 3 Core Visualizations Grid
            dbc.Row([
                # Graph 3.1: Quadrant Matrix
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("3.1 Four-Quadrant Skill Gap Matrix", className="chart-title mb-0"),
                                    html.Span("🔍 Supply vs Demand Scatter", className="badge bg-primary-subtle text-info small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab3-quadrant-scatter",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "460px"}
                            )
                        ]
                    )
                ], width=12, lg=7),
                
                # Graph 3.2: Curriculum Alignment Index
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("3.2 Program Curriculum Alignment Index (%)", className="chart-title mb-0"),
                                    html.Span("🎯 Industry Benchmark (80%)", className="badge bg-success-subtle text-success small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab3-alignment-bar",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "460px"}
                            )
                        ]
                    )
                ], width=12, lg=5)
            ]),
            
            # Graph 3.3: Mismatch Impact Bubble Chart
            dbc.Row([
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("3.3 Impact of Curriculum Alignment on Employment Rate & Starting Salary", className="chart-title mb-0"),
                                    html.Span("💡 Bubble Size = Avg Starting Salary", className="badge bg-info-subtle text-info small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab3-impact-bubble",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "400px"}
                            )
                        ]
                    )
                ], width=12)
            ])
        ]
    )

def build_quadrant_scatter_figure(skills_matrix_df, selected_role=None):
    """Build Graph 3.1: 4-Quadrant Skill Matrix Scatter Plot"""
    df = skills_matrix_df.copy()
    
    if selected_role == "AI/ML Engineer":
        y_col = "demand_ai"
        role_label = "AI/ML Engineer"
    elif selected_role == "Data Scientist":
        y_col = "demand_ds"
        role_label = "Data Scientist"
    elif selected_role == "Statistician":
        y_col = "demand_stat"
        role_label = "Statistician"
    elif selected_role == "Data Engineer":
        y_col = "demand_de"
        role_label = "Data Engineer"
    else:
        y_col = "overall_demand_score"
        role_label = "All Roles Combined"
        
    fig = px.scatter(
        df,
        x="supply_score",
        y=y_col,
        color="quadrant",
        color_discrete_map=QUADRANT_COLORS,
        text="skill",
        size=[18] * len(df),
        hover_data=["category", "type", "strategic_action", "gap_score"]
    )
    
    fig.update_traces(
        textposition="top center",
        textfont={"size": 10, "color": "#f8fafc"}
    )
    
    # Add Quadrant dividing lines at 55%
    fig.add_vline(x=55, line_width=1.5, line_dash="dash", line_color="rgba(148, 163, 184, 0.4)")
    fig.add_hline(y=55, line_width=1.5, line_dash="dash", line_color="rgba(148, 163, 184, 0.4)")
    
    # Quadrant background labels
    fig.add_annotation(x=25, y=98, text="🚨 Quadrant I: DEFICIT (High Demand / Low Supply)", showarrow=False, font={"color": "#ef4444", "size": 11, "weight": 600})
    fig.add_annotation(x=82, y=98, text="✅ Quadrant II: ALIGNED (High Demand / High Supply)", showarrow=False, font={"color": "#22c55e", "size": 11, "weight": 600})
    fig.add_annotation(x=82, y=10, text="🔄 Quadrant III: SURPLUS (Low Demand / High Supply)", showarrow=False, font={"color": "#f59e0b", "size": 11, "weight": 600})
    fig.add_annotation(x=25, y=10, text="⚙️ Quadrant IV: NICHE (Low Demand / Low Supply)", showarrow=False, font={"color": "#94a3b8", "size": 11, "weight": 600})
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title=f"Supply (% Curricula Offering) vs Demand (% Job Postings Requiring) - {role_label}",
        xaxis_title="Academic Supply Score (% Programs Teaching)",
        yaxis_title=f"Market Demand Score (% Postings for {role_label})",
        xaxis={"range": [10, 105]},
        yaxis={"range": [0, 110]},
        legend_title_text="Quadrant Classification",
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.3, "xanchor": "center", "x": 0.5}
    )
    return fig

def build_alignment_bar_figure(alignment_df):
    """Build Graph 3.2: Curriculum Alignment Index Horizontal Bar Chart"""
    df = alignment_df.sort_values(by="alignment_index", ascending=True)
    
    colors = [COLOR_SUCCESS if v >= 85 else (COLOR_PRIMARY if v >= 75 else COLOR_ALERT) for v in df["alignment_index"]]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["program_name"],
        x=df["alignment_index"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.1f}%" for v in df["alignment_index"]],
        textposition="outside"
    ))
    
    # Target Benchmark Line at 80%
    fig.add_vline(x=80, line_width=2, line_dash="dash", line_color="#38bdf8", annotation_text="Industry Target (80%)", annotation_position="top right")
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title="Program Curriculum Alignment Index (%)",
        xaxis_title="Alignment Score (%)",
        yaxis_title="",
        xaxis={"range": [0, 115]},
        margin={"l": 200}
    )
    return fig

def build_impact_bubble_figure(alignment_df, currency="USD ($)"):
    """Build Graph 3.3: Mismatch Impact Bubble Chart"""
    rate = 36.5 if currency == "THB (฿)" else (0.92 if currency == "EUR (€)" else 1.0)
    symbol = "฿" if currency == "THB (฿)" else ("€" if currency == "EUR (€)" else "$")
    
    df = alignment_df.copy()
    df["salary_display"] = df["avg_starting_salary_usd"] * rate
    
    fig = px.scatter(
        df,
        x="alignment_index",
        y="y1_emp_rate",
        size="avg_starting_salary_usd",
        color="country",
        text="program_name",
        hover_data={"salary_display": ":,.0f", "alignment_index": ":.1f", "y1_emp_rate": ":.1f"},
        size_max=32
    )
    
    fig.update_traces(textposition="top center", textfont={"size": 10, "color": "#f8fafc"})
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title=f"Correlation: Alignment Index vs 1st Year Employment Rate & Starting Pay ({currency})",
        xaxis_title="Curriculum Alignment Index (%)",
        yaxis_title="Year 1 Direct Employment Rate (%)",
        xaxis={"range": [60, 102]},
        yaxis={"range": [70, 102]},
        legend_title_text="Country"
    )
    return fig
