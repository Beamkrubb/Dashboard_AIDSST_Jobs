# 🚀 Handoff Protocol: DS/AI/Stats Market Dashboard for Antigravity

**Document Version:** 1.1.0  
**Target Agent / Role:** Antigravity (Data Visualization & Dashboard Agent)  
**Project Name:** Global Data Science, AI & Statistics Workforce Dashboard  
**Status:** Ready for Dashboard Engineering & Data Pipeline Integration

---

## 1. Project Context & Objectives

เอกสารนี้ใช้สำหรับส่งต่อบริบทและข้อกำหนดการพัฒนา **Interactive Analytics Dashboard** ให้แก่ **Antigravity** โดยเป้าหมายคือการแปลงชุดข้อมูลเปิด (Open Data) เกี่ยวกับตลาดแรงงาน สถิติการศึกษา อัตราเงินเดือน และทักษะที่จำเป็นในสายงาน **Data Science, Artificial Intelligence (AI) และ Statistics** ให้อยู่ในรูปของ Visual Dashboard ที่โต้ตอบได้และเข้าใจง่าย

---

## 2. Comprehensive Open Data Sources Catalog (สำหรับ Ingestion)

ตารางด้านล่างคือแหล่งข้อมูลเปิด (Open Data) หลักที่ต้องใช้เป็นข้อมูลนำเข้า (Data Ingestion Pipeline) สำหรับสร้าง Dashboard:

### 2.1 ข้อมูลอัตราเงินเดือนและการจ้างงาน (Salaries & Job Market Data)

| แหล่งข้อมูล (Data Source) | คำอธิบายชุดข้อมูล (Description) | รูปแบบไฟล์ | ลิงก์ดาวน์โหลด / API | ฟิลด์ข้อมูลสำคัญ (Key Fields) |
| :--- | :--- | :--- | :--- | :--- |
| **Kaggle Data Science Job Salaries** *(CC0 License)* | ข้อมูลเงินเดือนจริงทั่วโลกในสายงาน AI/DS/ML ย้อนหลังถึงปัจจุบัน | CSV / API | [Download Dataset](https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs/data) | `work_year`, `experience_level`, `job_title`, `salary_in_usd`, `company_location`, `company_size` |
| **aijobs.net Open Data** | ข้อมูลการจ้างงานสาย Tech & AI รายวันจากทั่วโลก | CSV / JSON | [Access Open Data](https://aijobs.net/) | `job_title`, `salary_currency`, `salary_usd`, `location`, `remote_ratio`, `employment_type` |
| **AI & Data Job Market Roles & Skills** | ข้อมูลประกาศรับสมัครงานกว่า 11,000+ ตำแหน่ง ระบุวุฒิและทักษะ | CSV | [Download Dataset](https://www.kaggle.com/datasets/anujsaha0123456789/ai-and-data-job-market-2023-roles-skills-and) | `job_id`, `role`, `required_skills`, `degree_requirement`, `experience_years` |
| **U.S. BLS OEWS Open Data** | สถิติทางการของรัฐบาลสหรัฐฯ สำหรับ Data Scientists & Statisticians | CSV / XLSX | [US BLS OEWS Tables](https://www.bls.gov/oes/tables.htm) | `occ_code`, `occ_title`, `tot_emp`, `jobs_1000`, `a_mean`, `a_median` |

### 2.2 ข้อมูลผู้สำเร็จการศึกษาและการศึกษาขั้นสูง (Education & Graduate Data)

| แหล่งข้อมูล (Data Source) | คำอธิบายชุดข้อมูล (Description) | รูปแบบไฟล์ | ลิงก์ดาวน์โหลด / API | ฟิลด์ข้อมูลสำคัญ (Key Fields) |
| :--- | :--- | :--- | :--- | :--- |
| **NCES IPEDS Data Center** | สถิติจำนวนผู้จบการศึกษาปริญญาตรี-เอก สาขา DS, AI, Stats ในสหรัฐฯ | CSV / ZIP | [NCES IPEDS Portal](https://nces.ed.gov/ipeds/use-the-data) | `unitid`, `cipcode` (11.0401, 27.0501), `award_level`, `graduates_count` |
| **UNESCO Institute for Statistics** | สถิติการศึกษาและ STEM Graduates ระดับนานาชาติ | CSV / JSON | [UNESCO UIS Data](http://data.uis.unesco.org/) | `country_code`, `year`, `field_of_study`, `degree_level`, `count` |
| **NSF NCSES Doctorate Survey** | สำรวจผู้จบปริญญาเอกสาขา Math, Statistics, Computer Science | CSV / XLSX | [NSF NCSES SED](https://ncses.nsf.gov/surveys/earned-doctorates/) | `phd_year`, `field_detailed`, `institution`, `postgrad_plans` |
| **Kaggle ML & Data Science Survey** | แบบสำรวจผู้เรียนและผู้ทำงานด้าน DS/AI ทั่วโลก | CSV | [Kaggle Survey Datasets](https://www.kaggle.com/datasets) | `education_level`, `major`, `current_role`, `years_coding`, `tech_stack` |

### 2.3 ข้อมูลมาตรฐานทักษะและคำนิยามสายงาน (Skills Taxonomy Data)

| แหล่งข้อมูล (Data Source) | คำอธิบายชุดข้อมูล (Description) | รูปแบบไฟล์ | ลิงก์ดาวน์โหลด / API | ฟิลด์ข้อมูลสำคัญ (Key Fields) |
| :--- | :--- | :--- | :--- | :--- |
| **O*NET OnLine (US Dept of Labor)** | ฐานข้อมูลวิเคราะห์ทักษะและหน้าที่งาน Data Scientists (15-2051.00) & Statisticians (15-2041.00) | Web API / TXT | [O*NET Data Center](https://www.onetonline.org/) | `element_id`, `element_name`, `importance_score`, `related_technology` |

---

## 3. Dashboard Architecture & Visual Structure

กำหนดให้ Antigravity ออกแบบ Dashboard โดยแบ่งออกเป็น **4 หน้าหลัก (Tabs/Pages)** ดังนี้:

### 📊 Page 1: Executive Overview & Market Summary
* **KPI Cards (Top Banner):**
  * Total Active Job Postings (Count)
  * Median Global Salary (USD & Converted THB)
  * YoY Job Growth Rate (%)
  * Total Yearly STEM/DS/AI Graduates
* **Visuals:**
  * **Global Heatmap / Map Chart:** แสดงปริมาณงานและฐานเงินเดือนเฉลี่ยแยกตามประเทศ (`company_location`)
  * **Trend Line Chart:** แนวโน้มการเปิดรับสมัครงานตำแหน่ง AI vs Data Science vs Statistician ย้อนหลัง

### 💰 Page 2: Compensation & Career Level Breakdown
* **Visuals:**
  * **Box Plot / Bar Chart:** เปรียบเทียบช่วงเงินเดือน (Median, 25th, 75th percentile) ตาม **Career Level**:
    * Entry-Level (EN)
    * Mid-Level (MI)
    * Senior / Lead (SE)
    * Executive / Expert (EX)
  * **Donut Chart:** สัดส่วนรูปแบบการทำงาน (`Remote` vs `Hybrid` vs `Onsite`)
  * **Scatter Plot:** ความสัมพันธ์ระหว่างระดับการศึกษา (Bachelor, Master, PhD) กับฐานเงินเดือนเริ่มต้น

### 🧠 Page 3: Skills Demand & Job Posting Matrix
* **Visuals:**
  * **Horizontal Bar Chart / Word Cloud:** Top 15 Required Hard Skills (e.g., Python, SQL, PyTorch, RAG, MLOps, Snowflake)
  * **Stacked Bar Chart:** เปรียบเทียบทักษะทางเทคนิคที่ต้องการแยกตามบทบาทงาน (`AI Engineer` vs `Data Scientist` vs `Statistician`)
  * **Grouped Bar Chart:** ความต้องการระหว่าง Soft Skills กับ Hard Skills

### 🏢 Page 4: Educational Pipeline & Hiring Companies
* **Visuals:**
  * **Sankey Diagram / Flow Chart:** เส้นทางจากวุฒิการศึกษา (Graduate Field) -> สายงานแรก (Entry Level Role) -> ประเภทบริษัท
  * **Company Leaderboard Table:** ตารางอันดับบริษัทที่เปิดรับสมัครงานด้าน AI & DS มากที่สุด พร้อมปุ่ม Filter เลือกตามขนาดบริษัท (`S`, `M`, `L`)

---

## 4. Interactive Filters & User Controls

Antigravity จะต้องติดตั้ง **Global Filter Panel** สำหรับผู้ใช้งาน ดังนี้:

| Filter Name | UI Control Type | Default Value | Options / Scope |
| :--- | :--- | :--- | :--- |
| **Region / Country** | Multi-select Dropdown | Global (All) | US, EU, APAC, Thailand, etc. |
| **Career Level** | Checklist Buttons | All | Entry (EN), Mid (MI), Senior (SE), Executive (EX) |
| **Role Category** | Radio Group | All | Data Scientist, AI/ML Engineer, Statistician, Data Engineer |
| **Salary Currency** | Toggle Switch | USD ($) | USD ($), THB (฿), EUR (€) |
| **Year Filter** | Slider / Range | 2022–2026 | Multi-year selector |

---

## 5. Technical & Design Guidelines for Antigravity

1. **Theme & Style:** Modern Dark Mode Theme (Slate/Navy `#0f172a`, Primary Accent Teal/Cyan `#38bdf8`, Success Green `#22c55e`)
2. **Responsiveness:** รองรับการแสดงผลทั้ง Desktop (1920x1080) และ Tablet (1024x768)
3. **Data Refresh Protocol:** ออกแบบโครงสร้างรองรับการดึงข้อมูลสดผ่าน REST API หรือ CSV File Upload
4. **Export Capabilities:** เพิ่มปุ่ม **Export Dashboard as PDF** และ **Download Raw Data (CSV)** ในทุกหน้า visual

---

## 6. Antigravity Execution Instructions

```bash
# Instruction Checklist for Antigravity Agent:
1. Ingest datasets from provided schema links in Section 2.
2. Clean and merge datasets using Pandas / Polars pipeline (Map experience levels & currencies).
3. Construct interactive layouts matching Page 1 to Page 4 specifications.
4. Apply state management for Global Filters.
5. Render dynamic summary text explaining key insights per visual.
```