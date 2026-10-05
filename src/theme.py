"""
Theme and Color Configuration for DS/AI/Stats Workforce Dashboard
Modern Dark Theme (#0f172a slate background, #1e293b card surface, #38bdf8 cyan accent)
"""

# Base Palette
COLOR_BG = "#0f172a"          # Slate 900
COLOR_SURFACE = "#1e293b"     # Slate 800
COLOR_SURFACE_LIGHT = "#334155" # Slate 700
COLOR_BORDER = "#334155"      # Slate 700
COLOR_TEXT = "#f8fafc"        # Slate 50
COLOR_TEXT_MUTED = "#94a3b8"  # Slate 400

# Accent & Status Colors
COLOR_PRIMARY = "#38bdf8"     # Sky / Cyan
COLOR_SECONDARY = "#818cf8"   # Indigo
COLOR_SUCCESS = "#22c55e"     # Green
COLOR_WARNING = "#f59e0b"     # Amber
COLOR_ALERT = "#ef4444"       # Red
COLOR_PURPLE = "#c084fc"      # Purple
COLOR_TEAL = "#2dd4bf"        # Teal

# Role Color Mapping
ROLE_COLORS = {
    "AI/ML Engineer": "#38bdf8",     # Cyan
    "Data Scientist": "#818cf8",     # Indigo
    "Statistician": "#2dd4bf",       # Teal
    "Data Engineer": "#c084fc",      # Purple
    "All Roles": "#f8fafc"
}

# Quadrant Colors
QUADRANT_COLORS = {
    "Skill Deficit (High Demand / Low Supply)": "#ef4444",   # Urgent Red
    "Well-Aligned (High Demand / High Supply)": "#22c55e",  # Success Green
    "Skill Surplus (Low Demand / High Supply)": "#f59e0b",  # Warning Amber
    "Niche Skills (Low Demand / Low Supply)": "#94a3b8"     # Muted Slate
}

# Degree Level Colors
DEGREE_COLORS = {
    "B.Sc. (Bachelor)": "#38bdf8",
    "M.Sc. (Master)": "#818cf8",
    "Ph.D. (Doctorate)": "#c084fc"
}

# Experience Level Colors
EXP_COLORS = {
    "Entry-Level (EN)": "#2dd4bf",
    "Mid-Level (MI)": "#38bdf8",
    "Senior / Lead (SE)": "#818cf8",
    "Executive / Expert (EX)": "#c084fc"
}

# Plotly Dark Layout Template Standard
PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter, system-ui, -apple-system, sans-serif",
            "color": COLOR_TEXT,
            "size": 12
        },
        "title": {
            "font": {
                "family": "Inter, system-ui, -apple-system, sans-serif",
                "color": COLOR_TEXT,
                "size": 15
            },
            "x": 0.02,
            "xanchor": "left"
        },
        "xaxis": {
            "gridcolor": "#334155",
            "zerolinecolor": "#475569",
            "tickfont": {"color": COLOR_TEXT_MUTED, "size": 11},
            "title": {"font": {"color": COLOR_TEXT, "size": 12}}
        },
        "yaxis": {
            "gridcolor": "#334155",
            "zerolinecolor": "#475569",
            "tickfont": {"color": COLOR_TEXT_MUTED, "size": 11},
            "title": {"font": {"color": COLOR_TEXT, "size": 12}}
        },
        "legend": {
            "font": {"color": COLOR_TEXT, "size": 11},
            "bgcolor": "rgba(30, 41, 59, 0.7)",
            "bordercolor": "#334155",
            "borderwidth": 1
        },
        "margin": {"l": 50, "r": 30, "t": 50, "b": 50},
        "hoverlabel": {
            "bgcolor": "#1e293b",
            "font": {"color": "#f8fafc", "family": "Inter, sans-serif"},
            "bordercolor": "#38bdf8"
        }
    }
}
