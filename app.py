"""
Main Application Entry Point: AI, Data Science & Statistics Workforce & Skill Mismatch Dashboard
Interactive Analytics & Linked Cross-Filtering Engine
"""

import os
import dash
from dash import Dash, html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd

from src.data_pipeline import pipeline
from src.components.header import render_header
from src.tabs.tab1_supply import (
    layout_tab1,
    build_graduates_figure,
    build_courses_treemap_figure,
    build_employment_figure,
    build_tuition_figure
)
from src.tabs.tab2_demand import (
    layout_tab2,
    build_vacancies_donut_figure,
    build_skills_bar_figure,
    build_companies_treemap_figure,
    build_salary_box_figure
)
from src.tabs.tab3_skill_mismatch import (
    layout_tab3,
    build_quadrant_scatter_figure,
    build_alignment_bar_figure,
    build_impact_bubble_figure
)
from src.tabs.tab4_overview import (
    layout_tab4,
    render_kpis,
    build_global_map_figure,
    build_trend_line_figure,
    build_sankey_flow_figure,
    render_company_leaderboard
)

# Initialize Dash App
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="AI/DS/Stats Workforce & Skill Mismatch Dashboard"
)
server = app.server

# Root App Layout
app.layout = dbc.Container(
    fluid=True,
    className="p-3 p-md-4 min-vh-100 bg-slate-900",
    children=[
        # Client-Side Filter State Stores
        dcc.Store(id="tab1-selected-program", data=None),
        dcc.Store(id="tab2-selected-role", data=None),
        
        # Header & Global Controls
        render_header(),
        
        # Navigation Tabs
        dbc.Tabs(
            id="main-tabs",
            active_tab="tab-overview",
            className="custom-nav-tabs mb-3",
            children=[
                dbc.Tab(label="📊 Executive Overview & Macro Flows", tab_id="tab-overview"),
                dbc.Tab(label="🎓 Tab 1: Academic Supply Analysis", tab_id="tab-supply"),
                dbc.Tab(label="💼 Tab 2: Market Demand Analysis", tab_id="tab-demand"),
                dbc.Tab(label="⚠️ Tab 3: Skill Mismatch & Gap Intelligence", tab_id="tab-mismatch"),
            ]
        ),
        
        # Dynamic Tab Content Area
        html.Div(id="tab-content-area", className="mt-2"),
        
        # Footer
        html.Footer(
            className="mt-5 pt-3 pb-4 border-top border-secondary border-opacity-25 text-center text-muted small",
            children=[
                html.P("© 2026 AI, Data Science & Statistics Labor Market Intelligence. Powered by Plotly Dash & Antigravity Agent.", className="mb-1"),
                html.Span("Data sources: Kaggle DS Salaries, aijobs.net, US BLS OEWS, NCES IPEDS, UNESCO UIS, O*NET Taxonomy.", className="text-secondary")
            ]
        )
    ]
)

# ==========================================================
# CALLBACKS: TAB SWITCHING
# ==========================================================
@app.callback(
    Output("tab-content-area", "children"),
    Input("main-tabs", "active_tab")
)
def render_active_tab(active_tab):
    if active_tab == "tab-supply":
        return layout_tab1()
    elif active_tab == "tab-demand":
        return layout_tab2()
    elif active_tab == "tab-mismatch":
        return layout_tab3()
    else:
        return layout_tab4()

# ==========================================================
# CALLBACKS: GLOBAL RESET BUTTON
# ==========================================================
@app.callback(
    [
        Output("global-country-filter", "value"),
        Output("global-role-filter", "value"),
        Output("global-exp-filter", "value"),
        Output("global-year-slider", "value"),
        Output("global-currency-toggle", "value"),
        Output("tab1-selected-program", "data", allow_duplicate=True),
        Output("tab2-selected-role", "data", allow_duplicate=True)
    ],
    Input("global-reset-all-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_global_reset(n_clicks):
    return (
        ["All"],
        "All Roles",
        ["Entry-Level (EN)", "Mid-Level (MI)", "Senior / Lead (SE)", "Executive / Expert (EX)"],
        [2022, 2026],
        "USD ($)",
        None,
        None
    )

# ==========================================================
# CALLBACKS: TAB 1 LINKED CROSS-FILTERING
# ==========================================================
@app.callback(
    [
        Output("tab1-selected-program", "data"),
        Output("tab1-active-filter-alert", "children")
    ],
    [
        Input("graph-tab1-graduates", "clickData"),
        Input("tab1-reset-btn", "n_clicks")
    ],
    State("tab1-selected-program", "data"),
    prevent_initial_call=True
)
def manage_tab1_filter_state(click_data, reset_clicks, current_program):
    triggered_id = ctx.triggered_id
    if triggered_id == "tab1-reset-btn":
        return None, None
        
    if click_data and "points" in click_data:
        clicked_prog = click_data["points"][0].get("x")
        if clicked_prog:
            alert = dbc.Alert(
                [
                    html.Span("🎯 Active Cross-Filter: ", className="fw-bold"),
                    html.Span(f"Program = '{clicked_prog}'. Showing synchronized metrics across all charts. "),
                    dbc.Button("Clear Filter", id="tab1-inline-clear-btn", color="danger", size="sm", className="ms-2 py-0 px-2", n_clicks=0)
                ],
                color="info",
                className="py-2 px-3 d-flex align-items-center mb-0"
            )
            return clicked_prog, alert
            
    return current_program, None

@app.callback(
    [
        Output("graph-tab1-graduates", "figure"),
        Output("graph-tab1-courses-treemap", "figure"),
        Output("graph-tab1-employment", "figure"),
        Output("graph-tab1-tuition", "figure")
    ],
    [
        Input("global-country-filter", "value"),
        Input("global-year-slider", "value"),
        Input("global-currency-toggle", "value"),
        Input("tab1-selected-program", "data")
    ]
)
def update_tab1_linked_graphs(countries, year_range, currency, selected_program):
    df = pipeline.get_filtered_supply(countries=countries, year_range=year_range)
    
    fig_graduates = build_graduates_figure(df, selected_program=selected_program)
    fig_courses = build_courses_treemap_figure(pipeline.courses_df, selected_program=selected_program)
    fig_employment = build_employment_figure(df, selected_program=selected_program)
    fig_tuition = build_tuition_figure(df, currency=currency, selected_program=selected_program)
    
    return fig_graduates, fig_courses, fig_employment, fig_tuition

@app.callback(
    Output("tab1-download-dataframe-csv", "data"),
    Input("tab1-export-csv-btn", "n_clicks"),
    [
        State("global-country-filter", "value"),
        State("global-year-slider", "value"),
        State("tab1-selected-program", "data")
    ],
    prevent_initial_call=True
)
def export_tab1_csv(n_clicks, countries, year_range, selected_prog):
    df = pipeline.get_filtered_supply(countries=countries, year_range=year_range, selected_program=selected_prog)
    return dcc.send_data_frame(df.to_csv, "supply_graduates_data.csv", index=False)

# ==========================================================
# CALLBACKS: TAB 2 LINKED CROSS-FILTERING
# ==========================================================
@app.callback(
    [
        Output("tab2-selected-role", "data"),
        Output("tab2-active-filter-alert", "children")
    ],
    [
        Input("graph-tab2-vacancies-donut", "clickData"),
        Input("tab2-reset-btn", "n_clicks")
    ],
    State("tab2-selected-role", "data"),
    prevent_initial_call=True
)
def manage_tab2_filter_state(click_data, reset_clicks, current_role):
    triggered_id = ctx.triggered_id
    if triggered_id == "tab2-reset-btn":
        return None, None
        
    if click_data and "points" in click_data:
        clicked_role = click_data["points"][0].get("label")
        if clicked_role:
            alert = dbc.Alert(
                [
                    html.Span("🎯 Active Cross-Filter: ", className="fw-bold"),
                    html.Span(f"Role = '{clicked_role}'. Linked skills, companies, and compensation updated. "),
                    dbc.Button("Clear Filter", id="tab2-inline-clear-btn", color="danger", size="sm", className="ms-2 py-0 px-2", n_clicks=0)
                ],
                color="info",
                className="py-2 px-3 d-flex align-items-center mb-0"
            )
            return clicked_role, alert
            
    return current_role, None

@app.callback(
    [
        Output("graph-tab2-vacancies-donut", "figure"),
        Output("graph-tab2-skills-bar", "figure"),
        Output("graph-tab2-companies-treemap", "figure"),
        Output("graph-tab2-salary-box", "figure")
    ],
    [
        Input("global-country-filter", "value"),
        Input("global-role-filter", "value"),
        Input("global-exp-filter", "value"),
        Input("global-year-slider", "value"),
        Input("global-currency-toggle", "value"),
        Input("tab2-selected-role", "data")
    ]
)
def update_tab2_linked_graphs(countries, global_role, exp_levels, year_range, currency, clicked_role):
    active_role = clicked_role if clicked_role else global_role
    df = pipeline.get_filtered_demand(
        countries=countries,
        roles=active_role,
        exp_levels=exp_levels,
        year_range=year_range
    )
    
    fig_vacancies = build_vacancies_donut_figure(pipeline.get_filtered_demand(countries=countries, year_range=year_range), selected_role=active_role)
    fig_skills = build_skills_bar_figure(pipeline.skills_matrix_df, selected_role=active_role)
    fig_companies = build_companies_treemap_figure(df, selected_role=active_role)
    fig_salaries = build_salary_box_figure(df, currency=currency, selected_role=active_role)
    
    return fig_vacancies, fig_skills, fig_companies, fig_salaries

@app.callback(
    Output("tab2-download-dataframe-csv", "data"),
    Input("tab2-export-csv-btn", "n_clicks"),
    [
        State("global-country-filter", "value"),
        State("global-role-filter", "value"),
        State("global-exp-filter", "value"),
        State("global-year-slider", "value")
    ],
    prevent_initial_call=True
)
def export_tab2_csv(n_clicks, countries, role, exp_levels, year_range):
    df = pipeline.get_filtered_demand(countries=countries, roles=role, exp_levels=exp_levels, year_range=year_range)
    return dcc.send_data_frame(df.to_csv, "demand_jobs_data.csv", index=False)

# ==========================================================
# CALLBACKS: TAB 3 SKILL MISMATCH
# ==========================================================
@app.callback(
    [
        Output("graph-tab3-quadrant-scatter", "figure"),
        Output("graph-tab3-alignment-bar", "figure"),
        Output("graph-tab3-impact-bubble", "figure")
    ],
    [
        Input("global-role-filter", "value"),
        Input("global-currency-toggle", "value")
    ]
)
def update_tab3_graphs(role, currency):
    fig_quadrant = build_quadrant_scatter_figure(pipeline.skills_matrix_df, selected_role=role)
    fig_alignment = build_alignment_bar_figure(pipeline.alignment_df)
    fig_impact = build_impact_bubble_figure(pipeline.alignment_df, currency=currency)
    return fig_quadrant, fig_alignment, fig_impact

@app.callback(
    Output("tab3-download-dataframe-csv", "data"),
    Input("tab3-export-csv-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_tab3_csv(n_clicks):
    return dcc.send_data_frame(pipeline.skills_matrix_df.to_csv, "skill_mismatch_matrix.csv", index=False)

# ==========================================================
# CALLBACKS: TAB 4 EXECUTIVE OVERVIEW
# ==========================================================
@app.callback(
    [
        Output("tab4-kpi-container", "children"),
        Output("graph-tab4-global-map", "figure"),
        Output("graph-tab4-trend-line", "figure"),
        Output("graph-tab4-sankey-flow", "figure"),
        Output("tab4-company-leaderboard-container", "children")
    ],
    [
        Input("global-country-filter", "value"),
        Input("global-role-filter", "value"),
        Input("global-exp-filter", "value"),
        Input("global-year-slider", "value"),
        Input("global-currency-toggle", "value")
    ]
)
def update_tab4_overview(countries, role, exp_levels, year_range, currency):
    demand_df = pipeline.get_filtered_demand(countries=countries, roles=role, exp_levels=exp_levels, year_range=year_range)
    supply_df = pipeline.get_filtered_supply(countries=countries, year_range=year_range)
    
    kpis = render_kpis(demand_df, supply_df, currency=currency)
    fig_map = build_global_map_figure(demand_df, currency=currency)
    fig_trend = build_trend_line_figure(demand_df)
    fig_sankey = build_sankey_flow_figure(demand_df)
    leaderboard = render_company_leaderboard(demand_df, currency=currency)
    
    return kpis, fig_map, fig_trend, fig_sankey, leaderboard

@app.callback(
    Output("tab4-download-dataframe-csv", "data"),
    Input("tab4-export-csv-btn", "n_clicks"),
    [
        State("global-country-filter", "value"),
        State("global-role-filter", "value"),
        State("global-exp-filter", "value"),
        State("global-year-slider", "value")
    ],
    prevent_initial_call=True
)
def export_tab4_csv(n_clicks, countries, role, exp_levels, year_range):
    demand_df = pipeline.get_filtered_demand(countries=countries, roles=role, exp_levels=exp_levels, year_range=year_range)
    return dcc.send_data_frame(demand_df.to_csv, "executive_overview_data.csv", index=False)


if __name__ == "__main__":
    print("Starting DS/AI/Stats Workforce Analytics Dashboard on http://127.0.0.1:8050/ ...")
    app.run(host="127.0.0.1", port=8050, debug=False)
