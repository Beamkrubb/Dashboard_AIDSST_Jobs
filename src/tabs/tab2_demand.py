"""
Tab 2: Demand Side Analysis (อุปสงค์ตลาดแรงงาน & ทักษะที่ต้องการ)
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from src.theme import PLOTLY_TEMPLATE, ROLE_COLORS, EXP_COLORS, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ALERT, COLOR_PURPLE, COLOR_TEAL
from src.data_pipeline import pipeline, format_currency

def layout_tab2():
    return html.Div(
        className="tab-content-container p-3",
        children=[
            # Top Action & Status Bar
            html.Div(
                className="d-flex justify-content-between align-items-center mb-3 p-3 rounded-2 bg-slate-800 border border-secondary border-opacity-25",
                children=[
                    html.Div([
                        html.H4("💼 Labor Market Demand Side Analysis", className="text-white fw-bold mb-0"),
                        html.Small("Analysis of open job vacancies, required technical/soft skills, hiring enterprises, and compensation benchmarks.", className="text-muted")
                    ]),
                    html.Div(
                        className="d-flex gap-2",
                        children=[
                            dbc.Button([html.Span("📥"), " Export Demand CSV"], id="tab2-export-csv-btn", color="secondary", size="sm", outline=True),
                            dbc.Button([html.Span("🔄"), " Reset Tab 2 Filter"], id="tab2-reset-btn", color="info", size="sm", outline=True),
                            dcc.Download(id="tab2-download-dataframe-csv")
                        ]
                    )
                ]
            ),
            
            # Selected Filter Indicator Alert
            html.Div(id="tab2-active-filter-alert", className="mb-3"),
            
            # 4 Linked Charts Grid (2x2)
            dbc.Row([
                dbc.Col([
                    html.Div(
                        className="chart-card p-3 rounded-3 mb-4",
                        children=[
                            html.Div(
                                className="d-flex justify-content-between align-items-center mb-2",
                                children=[
                                    html.H5("2.1 Active Job Postings by Role Volume", className="chart-title mb-0"),
                                    html.Span("👆 Click slice to cross-filter role", className="badge bg-primary-subtle text-info small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab2-vacancies-donut",
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
                                    html.H5("2.2 Top 15 Most Demanded Skills", className="chart-title mb-0"),
                                    html.Span("📊 Hard vs Soft Skill Frequency", className="badge bg-secondary-subtle text-light small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab2-skills-bar",
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
                                    html.H5("2.3 Top Hiring Enterprises & Industry Sectors", className="chart-title mb-0"),
                                    html.Span("🏢 Industry Distribution", className="badge bg-success-subtle text-success small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab2-companies-treemap",
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
                                    html.H5("2.4 Compensation Range across Career Experience", className="chart-title mb-0"),
                                    html.Span("💵 Salary Quartiles (EN, MI, SE, EX)", className="badge bg-warning-subtle text-warning small")
                                ]
                            ),
                            dcc.Graph(
                                id="graph-tab2-salary-box",
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"height": "380px"}
                            )
                        ]
                    )
                ], width=12, lg=6)
            ])
        ]
    )

def build_vacancies_donut_figure(df, selected_role=None):
    """Build Graph 2.1: Open Job Vacancies Donut Chart"""
    agg = df["role"].value_counts().reset_index()
    agg.columns = ["role", "count"]
    
    fig = px.pie(
        agg,
        names="role",
        values="count",
        hole=0.55,
        color="role",
        color_discrete_map=ROLE_COLORS
    )
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title=f"Job Openings Share by Role ({len(df):,} Total Positions)",
        showlegend=True,
        annotations=[{
            "text": f"<b>{len(df):,}</b><br>Jobs",
            "x": 0.5, "y": 0.5,
            "font_size": 14,
            "showarrow": False,
            "font_color": "#ffffff"
        }]
    )
    return fig

def build_skills_bar_figure(skills_matrix_df, selected_role=None):
    """Build Graph 2.2: Top Skills Ranking Horizontal Bar Chart"""
    df = skills_matrix_df.copy()
    
    if selected_role == "AI/ML Engineer":
        val_col = "demand_ai"
    elif selected_role == "Data Scientist":
        val_col = "demand_ds"
    elif selected_role == "Statistician":
        val_col = "demand_stat"
    elif selected_role == "Data Engineer":
        val_col = "demand_de"
    else:
        val_col = "overall_demand_score"
        
    df_sorted = df.sort_values(by=val_col, ascending=True).tail(15)
    
    fig = px.bar(
        df_sorted,
        x=val_col,
        y="skill",
        orientation="h",
        color="type",
        color_discrete_map={"Hard Skill": COLOR_PRIMARY, "Soft Skill": COLOR_TEAL},
        text=val_col
    )
    
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title=f"Top Skills In-Demand (% Job Postings Mentioning) - {selected_role or 'All Roles'}",
        xaxis_title="Market Demand (% Postings)",
        yaxis_title="",
        xaxis={"range": [0, 115]},
        legend_title_text="Skill Type"
    )
    return fig

def build_companies_treemap_figure(df, selected_role=None):
    """Build Graph 2.3: Hiring Companies & Industry Breakdown"""
    comp_agg = df.groupby(["industry", "company_name"], as_index=False).size().rename(columns={"size": "openings"})
    top_comps = comp_agg.sort_values("openings", ascending=False).groupby("industry").head(5)
    
    fig = px.treemap(
        top_comps,
        path=["industry", "company_name"],
        values="openings",
        color="industry",
        color_discrete_sequence=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_ALERT, COLOR_PURPLE]
    )
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title="Top Hiring Companies by Industry Sector",
        margin={"l": 10, "r": 10, "t": 40, "b": 10}
    )
    return fig

def build_salary_box_figure(df, currency="USD ($)", selected_role=None):
    """Build Graph 2.4: Salary Distribution across Career Experience Boxplot"""
    rate = 36.5 if currency == "THB (฿)" else (0.92 if currency == "EUR (€)" else 1.0)
    symbol = "฿" if currency == "THB (฿)" else ("€" if currency == "EUR (€)" else "$")
    
    df_plot = df.copy()
    df_plot["converted_salary"] = df_plot["salary_in_usd"] * rate
    
    fig = px.box(
        df_plot,
        x="experience_level",
        y="converted_salary",
        color="experience_level",
        color_discrete_map=EXP_COLORS,
        points="outliers",
        category_orders={"experience_level": ["Entry-Level (EN)", "Mid-Level (MI)", "Senior / Lead (SE)", "Executive / Expert (EX)"]}
    )
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(
        title=f"Compensation Benchmark ({currency}) by Experience Level - {selected_role or 'All Roles'}",
        xaxis_title="Career Experience Level",
        yaxis_title=f"Annual Salary in {currency}",
        showlegend=False
    )
    return fig
