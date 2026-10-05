# 🌐 AI, Data Science & Statistics Workforce & Skill Mismatch Dashboard

> **Interactive Workforce Analytics & Skill Gap Intelligence Platform**  
> Built for educational institutions, policy makers, students, and employers to analyze the alignment between academic supply and job market demand in Data Science, Artificial Intelligence, and Statistics.

---

## 📌 Project Overview

The **DS/AI/Stats Market & Skill Mismatch Dashboard** is a comprehensive, interactive data analytics system designed to bridge the gap between higher education outputs (**Supply Side**) and real-world employment demands (**Demand Side**). By tracking academic curriculum alignment, graduate production, career trajectories, salary distributions, and in-demand skills, the dashboard provides actionable strategic intelligence.

---

## 🎯 Key Objectives

1. **Supply Side Intelligence:** Monitor university graduate outputs across Data Science, AI, and Statistics programs, tracking course structures, tuition fees, and multi-year employment rates (Years 1–3).
2. **Demand Side Dynamics:** Track live and historical job postings, salary benchmarks across experience levels (EN, MI, SE, EX), hiring leaderboards, and top technical/soft skills.
3. **Skill Mismatch & Gap Analysis:** Formulate a **4-Quadrant Skill Matrix** (Deficit, Surplus, Well-Aligned, Niche) and compute a **Curriculum Alignment Index (%)** to evaluate program efficacy against market needs.
4. **Linked Cross-Filtering:** Enable real-time reactive graph-to-graph cross-filtering across all views, allowing instant drill-down analysis with sub-second response times (<1.2s).

---

## 🏗️ System Architecture & Visual Structure

The platform incorporates a unified multi-tab analytical layout powered by a high-performance Python visualization stack:

```
Dashboard_AIDSST_Jobs/
├── assets/                       # Custom CSS, dark theme styling, logos, icons
├── data/
│   ├── raw/                      # Ingested open datasets & survey files
│   └── processed/                # Normalized & structured pipeline datasets
├── src/
│   ├── data_pipeline.py          # Data ingestion, cleaning, currency conversion & scoring
│   ├── components/               # Reusable UI components, KPI cards, filter panels
│   ├── tabs/
│   │   ├── tab1_supply.py        # Supply Side: Graduates, courses, employment & fees
│   │   ├── tab2_demand.py        # Demand Side: Job vacancies, skills, hiring & salaries
│   │   ├── tab3_skill_mismatch.py# Skill Mismatch: Quadrant analysis & alignment index
│   │   └── tab4_overview.py      # Executive Overview: Global heatmap, YoY trends & Sankey
│   └── callbacks/                # Linked cross-filtering state engine & export handlers
├── app.py                        # Main Plotly Dash application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── PROJECT_STATUS.md             # Real-time implementation progress tracker
├── antigravity_handoff_ds_ai_dashboard.md
└── brd_ds_ai_stat_skill_mismatch_dashboard.md
```

---

## 📊 Dashboard Modules & Tabs

### 🎓 Tab 1: Supply Side Analysis (อุปทานบัณฑิต & ทักษะที่เรียนมา)
* **Graph 1.1 - Annual Graduate Production:** Historical graduation counts across degree levels (B.Sc., M.Sc., Ph.D.) and academic institutions.
* **Graph 1.2 - Core Compulsory Course & Skill Alignment:** Interactive Sunburst/Treemap mapping core curriculum to fundamental technical skill pillars.
* **Graph 1.3 - Graduate Employment Tracking:** Multi-year career tracking (% in-field employment in Year 1, Year 2, and Year 3 post-graduation).
* **Graph 1.4 - Tuition Fee Comparison:** Total degree investment box plot comparing programs, institutions, and degree levels.

### 💼 Tab 2: Demand Side Analysis (อุปสงค์ตลาดแรงงาน & ทักษะที่ต้องการ)
* **Graph 2.1 - Open Job Vacancies Volume:** Active job listings categorized by core domain (`AI/ML Engineer`, `Data Scientist`, `Statistician`, `Data Engineer`).
* **Graph 2.2 - Top Required Skills Ranking:** Frequency and proportion of required Hard Skills (Python, SQL, PyTorch, RAG, MLOps, Snowflake) and Soft Skills.
* **Graph 2.3 - Active Hiring Companies Breakdown:** Industry breakdown and top hiring organizations across Tech, Banking, Healthcare, and Retail.
* **Graph 2.4 - Salary Distribution by Career Level:** Compensation percentile analysis (Min, 25th, Median, 75th, Max) across Entry-Level (EN), Mid-Level (MI), Senior (SE), and Executive (EX).

### ⚠️ Tab 3: Skill Mismatch & Gap Intelligence (วิเคราะห์ช่องว่างทักษะ)
* **Graph 3.1 - 4-Quadrant Skill Matrix:**
  * **Quadrant I (Skill Deficit):** High Demand / Low Supply *(Curriculum Update Urgency)*
  * **Quadrant II (Well-Aligned):** High Demand / High Supply
  * **Quadrant III (Skill Surplus):** Low Demand / High Supply *(Market Saturation)*
  * **Quadrant IV (Niche/Emerging):** Low Demand / Low Supply
* **Graph 3.2 - Curriculum Alignment Index (%):** Program-by-program benchmark score against industry requirements.
* **Graph 3.3 - Mismatch Impact on Employment & Salary:** Bubble chart evaluating how alignment index directly correlates with Year 1 employment and starting pay.

### 📈 Tab 4: Executive Overview & Macro Trends
* **Executive KPI Banners:** Total Active Jobs, Global Median Salary (USD & THB), YoY Growth Rate, Total STEM/AI Graduates.
* **Global Talent & Salary Heatmap:** Geographic concentration of vacancies and compensation.
* **Education-to-Industry Sankey Flow:** Degree discipline -> Entry-level job role -> Industry sector.

---

## 🎛️ Interactive Controls & Global Filters

| Filter Control | UI Type | Default | Scope |
| :--- | :--- | :--- | :--- |
| **Region / Country** | Multi-select Dropdown | Global (All) | US, EU, APAC, Thailand, UK, etc. |
| **Career Experience** | Checklist / Button Group | All Levels | Entry (EN), Mid (MI), Senior (SE), Executive (EX) |
| **Role Category** | Pill Radio Group | All Roles | Data Scientist, AI/ML Engineer, Statistician, Data Engineer |
| **Currency Switcher** | Toggle | USD ($) | USD ($), THB (฿), EUR (€) |
| **Year Slider** | Range Slider | 2022 – 2026 | Multi-year historical timeline |
| **Reset Filters** | Action Button | — | Clears cross-filtering state across active tab |

---

## 🛠️ Technology Stack

* **Language:** Python 3.10+
* **Dashboard Framework:** Plotly Dash (`dash`, `dash_bootstrap_components`)
* **Visualization Engine:** Plotly (`plotly.express`, `plotly.graph_objects`)
* **Data Processing:** Pandas, NumPy
* **UI Theme:** Modern Dark Slate Theme (`#0f172a` Canvas, `#1e293b` Surface Cards, `#38bdf8` Cyan Accent, `#22c55e` Success)
* **Export Utilities:** Raw CSV Data Export & High-Resolution Vector/Raster Plot Export

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Installation
```bash
# Clone repository
git clone https://github.com/Beamkrubb/Dashboard_AIDSST_Jobs.git
cd Dashboard_AIDSST_Jobs

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:8050/`.

---

## 📄 License & Attribution
- Open Data sources under CC0 and Open Government Data licenses (Kaggle, aijobs.net, US BLS, NCES IPEDS, UNESCO UIS, O*NET).
- Developed for academic workforce planning and data science labor market analytics.
