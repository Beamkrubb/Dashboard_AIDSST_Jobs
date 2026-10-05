"""
Data Ingestion, Synthetic Generation, Cleaning & Transformation Pipeline
DS/AI/Stats Workforce and Skill Mismatch Dashboard
"""

import pandas as pd
import numpy as np
import os

# Currency Conversion Constants
EXCHANGE_RATES = {
    "USD ($)": 1.0,
    "THB (฿)": 36.5,
    "EUR (€)": 0.92
}

CURRENCY_SYMBOLS = {
    "USD ($)": "$",
    "THB (฿)": "฿",
    "EUR (€)": "€"
}

def format_currency(val, currency="USD ($)"):
    rate = EXCHANGE_RATES.get(currency, 1.0)
    symbol = CURRENCY_SYMBOLS.get(currency, "$")
    converted = val * rate
    if currency == "THB (฿)":
        return f"{symbol}{converted:,.0f}"
    else:
        return f"{symbol}{converted:,.0f}"


class WorkforceDataPipeline:
    def __init__(self, data_dir=None):
        self.data_dir = data_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.raw_dir = os.path.join(self.data_dir, "raw")
        self.proc_dir = os.path.join(self.data_dir, "processed")
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.proc_dir, exist_ok=True)
        
        self.supply_df = None
        self.courses_df = None
        self.demand_df = None
        self.skills_demand_df = None
        self.skills_matrix_df = None
        self.alignment_df = None
        
        self.load_or_generate_all()

    def generate_supply_data(self):
        """Generate Academic Supply Side data: Programs, Graduates, Employment Tracking, Tuition"""
        np.random.seed(42)
        
        programs = [
            {"program_id": "P01", "program_name": "B.Sc. Data Science & Analytics", "degree": "B.Sc. (Bachelor)", "institution": "Chulalongkorn University", "country": "Thailand", "region": "APAC", "base_tuition_usd": 8500, "tuition_thb": 310000},
            {"program_id": "P02", "program_name": "B.Sc. Applied Statistics & Actuarial", "degree": "B.Sc. (Bachelor)", "institution": "Mahidol University", "country": "Thailand", "region": "APAC", "base_tuition_usd": 7800, "tuition_thb": 285000},
            {"program_id": "P03", "program_name": "B.Sc. Artificial Intelligence & Systems", "degree": "B.Sc. (Bachelor)", "institution": "Khon Kaen University (KKU)", "country": "Thailand", "region": "APAC", "base_tuition_usd": 6500, "tuition_thb": 240000},
            {"program_id": "P04", "program_name": "B.Sc. Computer Science & Big Data", "degree": "B.Sc. (Bachelor)", "institution": "Kasetsart University", "country": "Thailand", "region": "APAC", "base_tuition_usd": 6800, "tuition_thb": 250000},
            {"program_id": "P05", "program_name": "B.Sc. Data Science & Machine Learning", "degree": "B.Sc. (Bachelor)", "institution": "Chiang Mai University (CMU)", "country": "Thailand", "region": "APAC", "base_tuition_usd": 6200, "tuition_thb": 230000},
            {"program_id": "P06", "program_name": "M.Sc. Artificial Intelligence & Robotics", "degree": "M.Sc. (Master)", "institution": "Chulalongkorn University", "country": "Thailand", "region": "APAC", "base_tuition_usd": 12000, "tuition_thb": 440000},
            {"program_id": "P07", "program_name": "M.Sc. Data Science & Business Analytics", "degree": "M.Sc. (Master)", "institution": "NIDA Thailand", "country": "Thailand", "region": "APAC", "base_tuition_usd": 10500, "tuition_thb": 380000},
            {"program_id": "P08", "program_name": "M.Sc. Applied Statistics & Analytics", "degree": "M.Sc. (Master)", "institution": "Thammasat University", "country": "Thailand", "region": "APAC", "base_tuition_usd": 9500, "tuition_thb": 350000},
            {"program_id": "P09", "program_name": "Ph.D. Data Science & Intelligent Computing", "degree": "Ph.D. (Doctorate)", "institution": "Khon Kaen University (KKU)", "country": "Thailand", "region": "APAC", "base_tuition_usd": 15000, "tuition_thb": 550000},
            {"program_id": "P10", "program_name": "B.Sc. Data Science", "degree": "B.Sc. (Bachelor)", "institution": "UC Berkeley", "country": "United States", "region": "US", "base_tuition_usd": 48000, "tuition_thb": 1752000},
            {"program_id": "P11", "program_name": "M.Sc. Machine Learning", "degree": "M.Sc. (Master)", "institution": "Carnegie Mellon University", "country": "United States", "region": "US", "base_tuition_usd": 56000, "tuition_thb": 2044000},
            {"program_id": "P12", "program_name": "B.Sc. Statistics & Machine Learning", "degree": "B.Sc. (Bachelor)", "institution": "National University of Singapore (NUS)", "country": "Singapore", "region": "APAC", "base_tuition_usd": 32000, "tuition_thb": 1168000},
            {"program_id": "P13", "program_name": "M.Sc. Advanced Computing (AI/ML)", "degree": "M.Sc. (Master)", "institution": "Imperial College London", "country": "United Kingdom", "region": "EU", "base_tuition_usd": 42000, "tuition_thb": 1533000},
            {"program_id": "P14", "program_name": "M.Sc. Data Engineering & Analytics", "degree": "M.Sc. (Master)", "institution": "Technical University of Munich", "country": "Germany", "region": "EU", "base_tuition_usd": 4000, "tuition_thb": 146000},
            {"program_id": "P15", "program_name": "Ph.D. Statistics & Machine Learning", "degree": "Ph.D. (Doctorate)", "institution": "Stanford University", "country": "United States", "region": "US", "base_tuition_usd": 65000, "tuition_thb": 2372500}
        ]
        
        supply_records = []
        years = [2022, 2023, 2024, 2025, 2026]
        
        for prog in programs:
            base_grad = np.random.randint(45, 160) if "B.Sc." in prog["degree"] else (np.random.randint(20, 60) if "M.Sc." in prog["degree"] else np.random.randint(5, 18))
            y1_emp_base = np.random.uniform(72.0, 93.0)
            
            for y_idx, yr in enumerate(years):
                growth = 1.0 + (y_idx * 0.07) + np.random.uniform(-0.03, 0.05)
                grad_count = int(base_grad * growth)
                
                # Employment rates across 3 years post graduation
                emp_yr1 = min(98.5, max(65.0, y1_emp_base + y_idx * 1.2 + np.random.uniform(-2, 2)))
                emp_yr2 = min(99.0, max(75.0, emp_yr1 + np.random.uniform(3.0, 6.0)))
                emp_yr3 = min(99.8, max(82.0, emp_yr2 + np.random.uniform(1.5, 4.0)))
                
                direct_match_rate = min(95.0, max(55.0, emp_yr1 * np.random.uniform(0.78, 0.92)))
                avg_starting_salary_usd = (24000 if prog["country"] == "Thailand" else 88000) * (1 + y_idx * 0.05) + np.random.uniform(-2000, 3000)
                
                supply_records.append({
                    "program_id": prog["program_id"],
                    "program_name": prog["program_name"],
                    "degree": prog["degree"],
                    "institution": prog["institution"],
                    "country": prog["country"],
                    "region": prog["region"],
                    "year": yr,
                    "graduates_count": grad_count,
                    "emp_rate_year1": round(emp_yr1, 1),
                    "emp_rate_year2": round(emp_yr2, 1),
                    "emp_rate_year3": round(emp_yr3, 1),
                    "direct_field_match_pct": round(direct_match_rate, 1),
                    "tuition_fee_usd": prog["base_tuition_usd"],
                    "tuition_fee_thb": prog["tuition_thb"],
                    "avg_starting_salary_usd": round(avg_starting_salary_usd, 0)
                })
                
        self.supply_df = pd.DataFrame(supply_records)
        self.supply_df.to_csv(os.path.join(self.proc_dir, "supply_graduates.csv"), index=False)

    def generate_courses_and_skills_data(self):
        """Generate Course Curriculum & Skill Alignment Matrix"""
        courses = [
            # Machine Learning & AI
            {"course_id": "CS101", "course_name": "Foundations of Machine Learning", "category": "Machine Learning & AI", "credits": 3, "core_skill": "Machine Learning", "domain": "AI/DS"},
            {"course_id": "CS102", "course_name": "Deep Learning & Neural Networks", "category": "Machine Learning & AI", "credits": 3, "core_skill": "PyTorch / TensorFlow", "domain": "AI"},
            {"course_id": "CS103", "course_name": "Generative AI & LLMs (RAG)", "category": "Machine Learning & AI", "credits": 3, "core_skill": "RAG & LLMs", "domain": "AI"},
            {"course_id": "CS104", "course_name": "Computer Vision & Image Processing", "category": "Machine Learning & AI", "credits": 3, "core_skill": "Computer Vision", "domain": "AI"},
            {"course_id": "CS105", "course_name": "Natural Language Processing (NLP)", "category": "Machine Learning & AI", "credits": 3, "core_skill": "NLP / Transformers", "domain": "AI/DS"},
            
            # Mathematical & Statistical Foundations
            {"course_id": "ST201", "course_name": "Linear Algebra & Vector Calculus", "category": "Math & Statistics", "credits": 4, "core_skill": "Linear Algebra", "domain": "Core Math"},
            {"course_id": "ST202", "course_name": "Probability & Mathematical Statistics", "category": "Math & Statistics", "credits": 4, "core_skill": "Statistical Inference", "domain": "Stats"},
            {"course_id": "ST203", "course_name": "Applied Regression & GLM", "category": "Math & Statistics", "credits": 3, "core_skill": "Applied Regression", "domain": "Stats/DS"},
            {"course_id": "ST204", "course_name": "Time Series Analysis & Forecasting", "category": "Math & Statistics", "credits": 3, "core_skill": "Time Series Forecasting", "domain": "Stats/DS"},
            {"course_id": "ST205", "course_name": "Multivariate Statistical Analysis", "category": "Math & Statistics", "credits": 3, "core_skill": "Multivariate Analysis", "domain": "Stats"},
            {"course_id": "ST206", "course_name": "Bayesian Methods & Modeling", "category": "Math & Statistics", "credits": 3, "core_skill": "Bayesian Statistics", "domain": "Stats"},

            # Data Engineering & Cloud
            {"course_id": "DE301", "course_name": "Database Systems & Advanced SQL", "category": "Data Engineering", "credits": 3, "core_skill": "SQL & Relational DBs", "domain": "Data Eng/DS"},
            {"course_id": "DE302", "course_name": "Distributed Data Systems (Spark/Hadoop)", "category": "Data Engineering", "credits": 3, "core_skill": "Spark / Big Data", "domain": "Data Eng"},
            {"course_id": "DE303", "course_name": "Data Warehousing (Snowflake/BigQuery)", "category": "Data Engineering", "credits": 3, "core_skill": "Cloud Data Warehouses", "domain": "Data Eng"},
            {"course_id": "DE304", "course_name": "MLOps & Continuous Deployment", "category": "Data Engineering", "credits": 3, "core_skill": "MLOps & CI/CD", "domain": "AI/Data Eng"},
            {"course_id": "DE305", "course_name": "Cloud Infrastructure (AWS/GCP/Azure)", "category": "Data Engineering", "credits": 3, "core_skill": "Cloud Platforms", "domain": "Data Eng"},

            # Software & Analytics Tools
            {"course_id": "SE401", "course_name": "Python for Scientific Computing", "category": "Software & Tools", "credits": 3, "core_skill": "Python Programming", "domain": "Core Programming"},
            {"course_id": "SE402", "course_name": "R Programming for Statistical Analysis", "category": "Software & Tools", "credits": 3, "core_skill": "R Programming", "domain": "Stats Programming"},
            {"course_id": "SE403", "course_name": "Data Visualization & Dashboarding (Plotly/Tableau)", "category": "Software & Tools", "credits": 3, "core_skill": "Data Storytelling & Viz", "domain": "DS/Analytics"},
            {"course_id": "SE404", "course_name": "Data Structures & Algorithms", "category": "Software & Tools", "credits": 4, "core_skill": "Data Structures & OOP", "domain": "Core CS"},
            
            # Domain & Capstone
            {"course_id": "DP501", "course_name": "Business Analytics & Problem Formulation", "category": "Domain & Soft Skills", "credits": 3, "core_skill": "Business Acumen", "domain": "Soft Skill"},
            {"course_id": "DP502", "course_name": "AI Ethics, Governance & Privacy", "category": "Domain & Soft Skills", "credits": 2, "core_skill": "AI Ethics & Governance", "domain": "Governance"},
            {"course_id": "DP503", "course_name": "Industry Capstone & Agile Project", "category": "Domain & Soft Skills", "credits": 6, "core_skill": "Agile & Teamwork", "domain": "Soft Skill"}
        ]
        
        self.courses_df = pd.DataFrame(courses)
        self.courses_df.to_csv(os.path.join(self.proc_dir, "courses_curriculum.csv"), index=False)

    def generate_demand_and_jobs_data(self):
        """Generate Market Demand Side: 12,500+ Open Job Records with Salaries, Roles, Skills, Locations"""
        np.random.seed(101)
        
        roles = [
            {"role": "AI/ML Engineer", "prob": 0.32, "base_salary_usd": 138000, "std_usd": 32000},
            {"role": "Data Scientist", "prob": 0.35, "base_salary_usd": 122000, "std_usd": 28000},
            {"role": "Statistician", "prob": 0.12, "base_salary_usd": 96000, "std_usd": 22000},
            {"role": "Data Engineer", "prob": 0.21, "base_salary_usd": 128000, "std_usd": 26000}
        ]
        
        exp_levels = [
            {"exp": "Entry-Level (EN)", "code": "EN", "prob": 0.22, "multiplier": 0.65},
            {"exp": "Mid-Level (MI)", "code": "MI", "prob": 0.44, "multiplier": 1.00},
            {"exp": "Senior / Lead (SE)", "code": "SE", "prob": 0.28, "multiplier": 1.45},
            {"exp": "Executive / Expert (EX)", "code": "EX", "prob": 0.06, "multiplier": 1.95}
        ]
        
        locations = [
            {"country": "United States", "region": "US", "code": "US", "prob": 0.48, "loc_mult": 1.15},
            {"country": "Thailand", "region": "APAC", "code": "TH", "prob": 0.14, "loc_mult": 0.32},
            {"country": "United Kingdom", "region": "EU", "code": "GB", "prob": 0.10, "loc_mult": 0.88},
            {"country": "Germany", "region": "EU", "code": "DE", "prob": 0.08, "loc_mult": 0.85},
            {"country": "Singapore", "region": "APAC", "code": "SG", "prob": 0.07, "loc_mult": 0.90},
            {"country": "Canada", "region": "US", "code": "CA", "prob": 0.05, "loc_mult": 0.86},
            {"country": "Japan", "region": "APAC", "code": "JP", "prob": 0.04, "loc_mult": 0.80},
            {"country": "Australia", "region": "APAC", "code": "AU", "prob": 0.04, "loc_mult": 0.92}
        ]
        
        company_sizes = ["S", "M", "L"]
        comp_size_probs = [0.18, 0.52, 0.30]
        
        industries = [
            "Tech & Software", "Finance & Banking", "Healthcare & Pharma", 
            "E-Commerce & Retail", "Consulting & Professional Services", "Manufacturing & Auto"
        ]
        
        top_companies = {
            "Tech & Software": ["Google", "Microsoft", "Meta", "Amazon AWS", "OpenAI", "NVIDIA", "Agoda", "Sea Group", "LINE MAN Wongnai"],
            "Finance & Banking": ["SCB TechX", "Kasikorn Business-Technology Group (KBTG)", "JPMorgan Chase", "Goldman Sachs", "Citigroup", "Krungthai Bank"],
            "Healthcare & Pharma": ["Roche Diagnostics", "Pfizer", "Bumrungrad International", "Johnson & Johnson", "Novartis"],
            "E-Commerce & Retail": ["Shopee", "Lazada", "Central Retail Digital", "Target", "Walmart Global Tech"],
            "Consulting & Professional Services": ["McKinsey QuantumBlack", "BCG X", "Deloitte Digital", "PwC Data Analytics", "Accenture AI"],
            "Manufacturing & Auto": ["Tesla", "Toyota Tsusho AI", "SCG Chemicals Digital", "PTT Digital Solutions"]
        }
        
        n_samples = 12500
        
        role_choices = np.random.choice([r["role"] for r in roles], size=n_samples, p=[r["prob"] for r in roles])
        exp_choices = np.random.choice([e["exp"] for e in exp_levels], size=n_samples, p=[e["prob"] for e in exp_levels])
        loc_indices = np.random.choice(len(locations), size=n_samples, p=[l["prob"] for l in locations])
        size_choices = np.random.choice(company_sizes, size=n_samples, p=comp_size_probs)
        years = np.random.choice([2022, 2023, 2024, 2025, 2026], size=n_samples, p=[0.12, 0.18, 0.24, 0.28, 0.18])
        remote_ratios = np.random.choice(["Onsite", "Hybrid (50%)", "Fully Remote (100%)"], size=n_samples, p=[0.25, 0.45, 0.30])
        
        role_map = {r["role"]: r for r in roles}
        exp_map = {e["exp"]: e for e in exp_levels}
        
        records = []
        for i in range(n_samples):
            r_name = role_choices[i]
            r_info = role_map[r_name]
            e_name = exp_choices[i]
            e_info = exp_map[e_name]
            l_info = locations[loc_indices[i]]
            c_size = size_choices[i]
            yr = years[i]
            rem = remote_ratios[i]
            
            # Annual YoY inflation/growth modifier
            yr_mod = 1.0 + ((yr - 2022) * 0.045)
            
            # Calculate USD salary
            salary_raw = np.random.normal(r_info["base_salary_usd"], r_info["std_usd"])
            salary_usd = max(18000, salary_raw * e_info["multiplier"] * l_info["loc_mult"] * yr_mod)
            
            # Pick industry & company
            ind = np.random.choice(industries)
            comp = np.random.choice(top_companies[ind])
            
            records.append({
                "job_id": f"JOB-{yr}-{i+10000}",
                "work_year": yr,
                "role": r_name,
                "experience_level": e_name,
                "exp_code": e_info["code"],
                "company_location": l_info["country"],
                "country_code": l_info["code"],
                "region": l_info["region"],
                "company_size": c_size,
                "remote_ratio": rem,
                "industry": ind,
                "company_name": comp,
                "salary_in_usd": round(salary_usd, 0),
                "salary_in_thb": round(salary_usd * EXCHANGE_RATES["THB (฿)"], 0),
                "salary_in_eur": round(salary_usd * EXCHANGE_RATES["EUR (€)"], 0)
            })
            
        self.demand_df = pd.DataFrame(records)
        self.demand_df.to_csv(os.path.join(self.proc_dir, "demand_jobs.csv"), index=False)

    def generate_skill_taxonomy_and_gap_matrix(self):
        """Generate Skill Supply vs Demand metrics, Quadrant analysis, and Alignment Index"""
        skills = [
            # Hard Skills
            {"skill": "Python", "category": "Programming & Languages", "type": "Hard Skill", "supply_score": 96.0, "demand_ai": 94.0, "demand_ds": 98.0, "demand_stat": 75.0, "demand_de": 88.0},
            {"skill": "SQL & Relational DBs", "category": "Data Management", "type": "Hard Skill", "supply_score": 92.0, "demand_ai": 72.0, "demand_ds": 95.0, "demand_stat": 70.0, "demand_de": 96.0},
            {"skill": "PyTorch / Deep Learning", "category": "AI & Modeling", "type": "Hard Skill", "supply_score": 58.0, "demand_ai": 92.0, "demand_ds": 78.0, "demand_stat": 32.0, "demand_de": 25.0},
            {"skill": "RAG & LLM Application", "category": "AI & Modeling", "type": "Hard Skill", "supply_score": 28.0, "demand_ai": 89.0, "demand_ds": 68.0, "demand_stat": 18.0, "demand_de": 42.0},
            {"skill": "MLOps & CI/CD", "category": "Infrastructure & Cloud", "type": "Hard Skill", "supply_score": 24.0, "demand_ai": 84.0, "demand_ds": 62.0, "demand_stat": 12.0, "demand_de": 80.0},
            {"skill": "Cloud Platforms (AWS/GCP/Azure)", "category": "Infrastructure & Cloud", "type": "Hard Skill", "supply_score": 45.0, "demand_ai": 76.0, "demand_ds": 70.0, "demand_stat": 28.0, "demand_de": 92.0},
            {"skill": "Cloud Data Warehouses (Snowflake/BigQuery)", "category": "Data Management", "type": "Hard Skill", "supply_score": 35.0, "demand_ai": 45.0, "demand_ds": 66.0, "demand_stat": 22.0, "demand_de": 89.0},
            {"skill": "Spark & Big Data Processing", "category": "Data Management", "type": "Hard Skill", "supply_score": 42.0, "demand_ai": 55.0, "demand_ds": 64.0, "demand_stat": 25.0, "demand_de": 94.0},
            {"skill": "Applied Regression & GLM", "category": "Math & Statistics", "type": "Hard Skill", "supply_score": 90.0, "demand_ai": 48.0, "demand_ds": 82.0, "demand_stat": 95.0, "demand_de": 30.0},
            {"skill": "Time Series Forecasting", "category": "Math & Statistics", "type": "Hard Skill", "supply_score": 68.0, "demand_ai": 62.0, "demand_ds": 74.0, "demand_stat": 88.0, "demand_de": 35.0},
            {"skill": "R Programming", "category": "Programming & Languages", "type": "Hard Skill", "supply_score": 78.0, "demand_ai": 22.0, "demand_ds": 52.0, "demand_stat": 92.0, "demand_de": 15.0},
            {"skill": "SAS & SPSS", "category": "Legacy Statistics", "type": "Hard Skill", "supply_score": 72.0, "demand_ai": 5.0, "demand_ds": 18.0, "demand_stat": 48.0, "demand_de": 4.0},
            {"skill": "Linear Algebra & Calculus", "category": "Math & Statistics", "type": "Hard Skill", "supply_score": 95.0, "demand_ai": 82.0, "demand_ds": 70.0, "demand_stat": 85.0, "demand_de": 40.0},
            {"skill": "Docker & Containerization", "category": "Infrastructure & Cloud", "type": "Hard Skill", "supply_score": 38.0, "demand_ai": 78.0, "demand_ds": 58.0, "demand_stat": 16.0, "demand_de": 88.0},
            {"skill": "Data Storytelling & Visualization", "category": "Analytics & BI", "type": "Hard Skill", "supply_score": 82.0, "demand_ai": 50.0, "demand_ds": 86.0, "demand_stat": 74.0, "demand_de": 48.0},
            {"skill": "Bayesian Statistics", "category": "Math & Statistics", "type": "Hard Skill", "supply_score": 54.0, "demand_ai": 45.0, "demand_ds": 48.0, "demand_stat": 76.0, "demand_de": 12.0},
            
            # Soft Skills
            {"skill": "Problem Solving & Analytical Thinking", "category": "Soft Skills", "type": "Soft Skill", "supply_score": 85.0, "demand_ai": 92.0, "demand_ds": 95.0, "demand_stat": 90.0, "demand_de": 88.0},
            {"skill": "Communication & Stakeholder Translation", "category": "Soft Skills", "type": "Soft Skill", "supply_score": 62.0, "demand_ai": 80.0, "demand_ds": 92.0, "demand_stat": 75.0, "demand_de": 72.0},
            {"skill": "Agile & Cross-Functional Teamwork", "category": "Soft Skills", "type": "Soft Skill", "supply_score": 55.0, "demand_ai": 86.0, "demand_ds": 84.0, "demand_stat": 60.0, "demand_de": 88.0},
            {"skill": "Business Acumen & Value Creation", "category": "Soft Skills", "type": "Soft Skill", "supply_score": 48.0, "demand_ai": 68.0, "demand_ds": 88.0, "demand_stat": 52.0, "demand_de": 58.0}
        ]
        
        matrix_records = []
        for s in skills:
            # Weighted average demand across all 4 roles
            overall_demand = (s["demand_ai"] * 0.32 + s["demand_ds"] * 0.35 + s["demand_stat"] * 0.12 + s["demand_de"] * 0.21)
            supply = s["supply_score"]
            
            # Quadrant categorization (thresholds: 55% demand, 55% supply)
            if overall_demand >= 55.0 and supply < 55.0:
                quad = "Skill Deficit (High Demand / Low Supply)"
                action = "Urgent Curriculum Upgrade Needed"
            elif overall_demand >= 55.0 and supply >= 55.0:
                quad = "Well-Aligned (High Demand / High Supply)"
                action = "Maintain High Academic Standard"
            elif overall_demand < 55.0 and supply >= 55.0:
                quad = "Skill Surplus (Low Demand / High Supply)"
                action = "Reduce Course Hours / Modernize"
            else:
                quad = "Niche Skills (Low Demand / Low Supply)"
                action = "Elective Specialty Offering"
                
            matrix_records.append({
                "skill": s["skill"],
                "category": s["category"],
                "type": s["type"],
                "supply_score": supply,
                "overall_demand_score": round(overall_demand, 1),
                "demand_ai": s["demand_ai"],
                "demand_ds": s["demand_ds"],
                "demand_stat": s["demand_stat"],
                "demand_de": s["demand_de"],
                "quadrant": quad,
                "strategic_action": action,
                "gap_score": round(overall_demand - supply, 1) # Positive = Deficit, Negative = Surplus
            })
            
        self.skills_matrix_df = pd.DataFrame(matrix_records)
        self.skills_matrix_df.to_csv(os.path.join(self.proc_dir, "skill_mismatch_matrix.csv"), index=False)
        
        # Calculate Curriculum Alignment Index for academic programs
        programs_alignment = [
            {"program_name": "B.Sc. Data Science & Analytics (Chula)", "degree": "B.Sc.", "country": "Thailand", "alignment_index": 88.5, "y1_emp_rate": 93.2, "avg_starting_salary_usd": 28500},
            {"program_name": "B.Sc. Artificial Intelligence (KKU)", "degree": "B.Sc.", "country": "Thailand", "alignment_index": 86.0, "y1_emp_rate": 91.5, "avg_starting_salary_usd": 27000},
            {"program_name": "B.Sc. Applied Statistics (Mahidol)", "degree": "B.Sc.", "country": "Thailand", "alignment_index": 71.5, "y1_emp_rate": 81.0, "avg_starting_salary_usd": 22500},
            {"program_name": "B.Sc. Computer Science & Big Data (KU)", "degree": "B.Sc.", "country": "Thailand", "alignment_index": 82.0, "y1_emp_rate": 88.0, "avg_starting_salary_usd": 25500},
            {"program_name": "B.Sc. Data Science & ML (CMU)", "degree": "B.Sc.", "country": "Thailand", "alignment_index": 84.0, "y1_emp_rate": 89.5, "avg_starting_salary_usd": 26000},
            {"program_name": "M.Sc. Artificial Intelligence (Chula)", "degree": "M.Sc.", "country": "Thailand", "alignment_index": 92.5, "y1_emp_rate": 96.8, "avg_starting_salary_usd": 38000},
            {"program_name": "M.Sc. Data Science & Analytics (NIDA)", "degree": "M.Sc.", "country": "Thailand", "alignment_index": 87.0, "y1_emp_rate": 92.0, "avg_starting_salary_usd": 34000},
            {"program_name": "M.Sc. Applied Statistics (TU)", "degree": "M.Sc.", "country": "Thailand", "alignment_index": 68.0, "y1_emp_rate": 79.5, "avg_starting_salary_usd": 24000},
            {"program_name": "Ph.D. Data Science & AI (KKU)", "degree": "Ph.D.", "country": "Thailand", "alignment_index": 90.0, "y1_emp_rate": 98.0, "avg_starting_salary_usd": 45000},
            {"program_name": "B.Sc. Data Science (UC Berkeley)", "degree": "B.Sc.", "country": "United States", "alignment_index": 94.0, "y1_emp_rate": 95.5, "avg_starting_salary_usd": 115000},
            {"program_name": "M.Sc. Machine Learning (CMU US)", "degree": "M.Sc.", "country": "United States", "alignment_index": 97.0, "y1_emp_rate": 98.5, "avg_starting_salary_usd": 142000},
            {"program_name": "B.Sc. Stats & ML (NUS)", "degree": "B.Sc.", "country": "Singapore", "alignment_index": 91.0, "y1_emp_rate": 94.0, "avg_starting_salary_usd": 78000},
            {"program_name": "M.Sc. Computing AI/ML (Imperial)", "degree": "M.Sc.", "country": "United Kingdom", "alignment_index": 93.0, "y1_emp_rate": 96.0, "avg_starting_salary_usd": 92000},
            {"program_name": "M.Sc. Data Engineering (TUM)", "degree": "M.Sc.", "country": "Germany", "alignment_index": 91.5, "y1_emp_rate": 94.5, "avg_starting_salary_usd": 86000}
        ]
        self.alignment_df = pd.DataFrame(programs_alignment)
        self.alignment_df.to_csv(os.path.join(self.proc_dir, "curriculum_alignment.csv"), index=False)

    def load_or_generate_all(self):
        """Generate all datasets if not cached, or load from CSV"""
        self.generate_supply_data()
        self.generate_courses_and_skills_data()
        self.generate_demand_and_jobs_data()
        self.generate_skill_taxonomy_and_gap_matrix()

    def get_filtered_demand(self, countries=None, roles=None, exp_levels=None, year_range=None):
        df = self.demand_df.copy()
        if countries and "All" not in countries and len(countries) > 0:
            df = df[df["company_location"].isin(countries)]
        if roles and roles != "All Roles":
            if isinstance(roles, list):
                if "All Roles" not in roles:
                    df = df[df["role"].isin(roles)]
            else:
                df = df[df["role"] == roles]
        if exp_levels and len(exp_levels) > 0:
            df = df[df["experience_level"].isin(exp_levels)]
        if year_range and len(year_range) == 2:
            df = df[(df["work_year"] >= year_range[0]) & (df["work_year"] <= year_range[1])]
        return df

    def get_filtered_supply(self, countries=None, degrees=None, year_range=None, selected_program=None):
        df = self.supply_df.copy()
        if selected_program:
            df = df[df["program_name"] == selected_program]
        if countries and "All" not in countries and len(countries) > 0:
            df = df[df["country"].isin(countries)]
        if degrees and len(degrees) > 0:
            df = df[df["degree"].isin(degrees)]
        if year_range and len(year_range) == 2:
            df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
        return df

# Singleton instance for quick imports
pipeline = WorkforceDataPipeline()
