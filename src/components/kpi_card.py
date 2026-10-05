"""
Reusable Modern KPI Card Component for Dash
"""
from dash import html

def render_kpi_card(title, value, subtitle=None, icon=None, badge_text=None, badge_color="success", card_id=None):
    """
    Renders a polished dark-themed metric card
    """
    badge_style = {
        "success": {"bg": "rgba(34, 197, 94, 0.15)", "color": "#22c55e", "border": "1px solid rgba(34, 197, 94, 0.3)"},
        "warning": {"bg": "rgba(245, 158, 11, 0.15)", "color": "#f59e0b", "border": "1px solid rgba(245, 158, 11, 0.3)"},
        "info": {"bg": "rgba(56, 189, 248, 0.15)", "color": "#38bdf8", "border": "1px solid rgba(56, 189, 248, 0.3)"},
        "alert": {"bg": "rgba(239, 68, 68, 0.15)", "color": "#ef4444", "border": "1px solid rgba(239, 68, 68, 0.3)"}
    }
    
    b_conf = badge_style.get(badge_color, badge_style["info"])
    
    return html.Div(
        className="kpi-card",
        id=card_id if card_id else "",
        children=[
            html.Div(
                className="d-flex justify-content-between align-items-start mb-2",
                children=[
                    html.Span(title, className="kpi-title"),
                    html.Span(icon if icon else "📊", className="kpi-icon")
                ]
            ),
            html.Div(
                className="d-flex align-items-baseline gap-2 mb-1",
                children=[
                    html.H2(value, className="kpi-value mb-0"),
                    html.Span(
                        badge_text,
                        className="kpi-badge",
                        style={
                            "backgroundColor": b_conf["bg"],
                            "color": b_conf["color"],
                            "border": b_conf["border"],
                            "display": "inline-block" if badge_text else "none"
                        }
                    ) if badge_text else None
                ]
            ),
            html.Small(subtitle if subtitle else "", className="kpi-subtitle")
        ]
    )
