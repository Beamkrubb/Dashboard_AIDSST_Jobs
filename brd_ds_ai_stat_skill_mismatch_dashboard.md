# 📋 Business Requirements Document (BRD)
## Project: AI, Data Science & Statistics Workforce & Skill Mismatch Dashboard

* **Document Version:** 1.0.0
* **Target Developer / Agent:** Antigravity (Data & Dashboard Engineering Agent)
* **Backend Framework:** Python 3.10+ (Dash / Streamlit / FastHTML with Plotly Engine)
* **Visualization Engine:** Plotly (`plotly.graph_objects` & `plotly.express`)
* **Key Architecture Rule:** **Linked Cross-Filtering** (All charts within the same tab must reactively update based on user clicks or selections on any graph).

---

## 1. Executive Summary & Purpose

เอกสารนี้กำหนดข้อกำหนดทางธุรกิจและรายละเอียดทางเทคนิคสำหรับ **Antigravity** ในการพัฒนา **Interactive Workforce Analytics Dashboard** โดยมีวัตถุประสงค์เพื่อวิเคราะห์ความสอดคล้องระหว่าง **อุปทานบัณฑิต (Supply Side - Tab 1)** และ **อุปสงค์ของตลาดแรงงาน (Demand Side - Tab 2)** ในสาขา **AI, Data Science และ Statistics** พร้อมทั้งวิเคราะห์ **ความเหลื่อมล้ำทางทักษะ (Skill Mismatch - Tab 3)** เพื่อนำไปสู่การปรับปรุงหลักสูตรและการวางแผนกำลังคนเชิงยุทธศาสตร์

---

## 2. Technical Stack & System Architecture

1. **Backend:** Python 3.10+
2. **Visualization Core:** Plotly Engine (`plotly.express`, `plotly.graph_objects`)
3. **Dashboard Framework Recommendation:** **Plotly Dash** (แนะนำเป็นหลักเนื่องจากรองรับ State Management และ Callbacks สำหรับ Cross-filtering ได้อย่างสมบูรณ์)
4. **Cross-Filtering State Engine (Mandatory):**
   * กราฟทุกตัวใน Tab เดียวกันจะต้องเชื่อมโยงกัน (Linked Charts)
   * เมื่อ User คลิกเลือกข้อมูลในกราฟใดกราฟหนึ่ง (e.g., Click Data Event) กราฟอื่น ๆ ทั้งหมดใน Tab นั้นจะต้องทำ Dynamic Filtering และ Re-render ข้อมูลทันที
   * ต้องมีปุ่ม **Reset Filters** ในทุก Tab เพื่อคืนค่า View ทั้งหมด

---

## 3. Tab-by-Tab Functional Specifications

---

### 🎓 Tab 1: ปริมาณคนที่จบและ Skills ที่เรียนมา (Supply Side Analysis)

**วัตถุประสงค์:** วิเคราะห์สถิติการผลิตกำลังคนจากสถาบันการศึกษา หลักสูตร รายวิชาบังคับ อัตราการได้งานทำ และค่าธรรมเนียมการศึกษา

#### Required Components & Visualizations:

1. **Graph 1.1: Annual Graduate Production by Academic Program**
   * **ประเภทกราฟ:** Grouped / Stacked Bar Chart หรือ Multi-Line Chart
   * **ข้อมูลที่แสดง:** รายชื่อหลักสูตร (e.g., B.Sc. Data Science, M.Sc. AI, B.Sc. Statistics) แยกตามมหาวิทยาลัย/คณะ พร้อมจำนวนบัณฑิตที่สำเร็จการศึกษาต่อปี (ย้อนหลัง 3–5 ปี)
   * **Trigger Filter:** เมื่อเลือกหลักสูตร หรือปี กราฟ 1.2, 1.3, 1.4 จะ Filter ข้อมูลตามหลักสูตรนั้นทันที

2. **Graph 1.2: Core Compulsory Courses & Target Skill Alignment**
   * **ประเภทกราฟ:** Interactive Heatmap / Treemap / Sunburst Chart
   * **ข้อมูลที่แสดง:** รายชื่อวิชาบังคับ (Core Compulsory Courses) ของหลักสูตร และการจัดหมวดหมู่ทักษะที่เกี่ยวข้องกับสายงาน (e.g., Linear Algebra, Machine Learning, Applied Regression, MLOps, SQL)

3. **Graph 1.3: Graduate Employment Tracking (Years 1, 2, and 3)**
   * **ประเภทกราฟ:** Stacked Bar Chart หรือ Grouped Column Chart
   * **ข้อมูลที่แสดง:** จำนวนและสัดส่วนของบัณฑิตที่ได้งานทำตรงสายงาน (AI, DS, Stat) แยกตามช่วงเวลาหลังเรียนจบ: **ปีที่ 1**, **ปีที่ 2** และ **ปีที่ 3**

4. **Graph 1.4: Program Tuition Fee Comparison**
   * **ประเภทกราฟ:** Box Plot หรือ Horizontal Bar Chart
   * **ข้อมูลที่แสดง:** ค่าธรรมเนียมการศึกษาตลอดหลักสูตร (Tuition Fees) เปรียบเทียบตามหลักสูตร ระดับปริญญา และสถาบันการศึกษา

---

### 💼 Tab 2: ปริมาณงานที่จ้างและ Skills ที่ต้องการ (Demand Side Analysis)

**วัตถุประสงค์:** วิเคราะห์ความต้องการของตลาดแรงงานจริง ปริมาณตำแหน่งงาน ทักษะที่ตลาดต้องการ บริษัทผู้ว่าจ้าง และระดับเงินเดือน

#### Required Components & Visualizations:

1. **Graph 2.1: Open Job Vacancies Volume by Role**
   * **ประเภทกราฟ:** Donut Chart / Bar Chart + Summary KPI Cards
   * **ข้อมูลที่แสดง:** ปริมาณตำแหน่งงานว่างที่เปิดรับสมัคร (Active Job Openings) แยกตามบทบาทหลัก (`AI/ML Engineer`, `Data Scientist`, `Statistician`, `Data Engineer`)
   * **Trigger Filter:** เมื่อเลือกรุ่น/ตำแหน่งงาน กราฟ 2.2, 2.3, 2.4 จะปรับการแสดงผลตามสายงานนั้น

2. **Graph 2.2: Top Required Skills Ranking**
   * **ประเภทกราฟ:** Horizontal Bar Chart หรือ Radar Chart
   * **ข้อมูลที่แสดง:** อันดับทักษะ (Hard Skills & Soft Skills) ที่ถูกระบุไว้ในประกาศรับสมัครงานบ่อยที่สุด (e.g., Python, SQL, PyTorch, RAG, Time Series Forecasting, Cloud Data Warehouses) พร้อม % สัดส่วนความต้องการ

3. **Graph 2.3: Active Hiring Companies Breakdown**
   * **ประเภทกราฟ:** Treemap หรือ Interactive Leaderboard
   * **ข้อมูลที่แสดง:** รายชื่อบริษัท/องค์กรที่เปิดรับสมัครงานตำแหน่ง AI/DS/Stat มากที่สุด แยกตามกลุ่มอุตสาหกรรม (e.g., Finance/Banking, Tech/Software, Retail, Healthcare)

4. **Graph 2.4: Salary Distribution across Career Levels**
   * **ประเภทกราฟ:** Box Plot หรือ Violin Plot
   * **ข้อมูลที่แสดง:** โครงสร้างเงินเดือน (Min, Median, Max) แยกตามระดับประสบการณ์:
     * **Entry-Level (EN)**
     * **Mid-Level (MI)**
     * **Senior / Lead (SE)**
     * **Executive / Expert (EX)**

---

### ⚠️ Tab 3: วิเคราะห์ Skill Mismatch (Supply vs Demand Analysis)

**วัตถุประสงค์:** เปรียบเทียบและวิเคราะห์ช่องว่างระหว่างทักษะที่หลักสูตรเปิดสอน (Tab 1) กับทักษะที่ตลาดต้องการจริง (Tab 2) เพื่อระบุทักษะที่ขาดแคลนหรือล้นตลาด

#### Required Components & Visualizations:

1. **Graph 3.1: Skill Gap Quadrant Analysis (Supply vs Demand Matrix)**
   * **ประเภทกราฟ:** 4-Quadrant Scatter Plot หรือ Diverging Bar Chart
   * **แกน X (Supply Score):** สัดส่วนหลักสูตรที่เปิดสอนทักษะนั้น (%)
   * **แกน Y (Demand Score):** สัดส่วนประกาศรับสมัครงานที่ต้องการทักษะนั้น (%)
   * **การแบ่ง Quadrant:**
     * **High Demand / Low Supply (Skill Deficit):** ทักษะขาดแคลน ตลาดต้องการสูง แต่สอนน้อย *(Priority for Curriculum Update)*
     * **High Demand / High Supply (Well Aligned):** ทักษะที่สอดคล้องสมบูรณ์
     * **Low Demand / High Supply (Skill Surplus):** ทักษะที่มีการสอนมาก แต่ความต้องการตลาดต่ำ
     * **Low Demand / Low Supply (Niche Skills):** ทักษะเฉพาะทาง

2. **Graph 3.2: Curriculum Alignment Index by Academic Program**
   * **ประเภทกราฟ:** Horizontal Bar Chart พร้อม Target Threshold Line (%)
   * **ข้อมูลที่แสดง:** คะแนนดัชนีความสอดคล้อง (% Curriculum Alignment Index) ของแต่ละหลักสูตรเทียบกับความต้องการจริงของตลาดงาน

3. **Graph 3.3: Mismatch Impact on Employment & Starting Salary**
   * **ประเภทกราฟ:** Bubble Chart
   * **ข้อมูลที่แสดง:**
     * **แกน X:** Curriculum Alignment Index (%)
     * **แกน Y:** อัตราการได้งานทำในปีแรก (% Year 1 Employment Rate)
     * **ขนาด Bubble:** เงินเดือนเริ่มต้นเฉลี่ยของบัณฑิต

---

## 4. Cross-Filtering Architecture Blueprint (Python/Plotly Dash Example)

Antigravity ต้องเขียน Callback Engine เพื่อรองรับ Linked Filtering ภายในแต่ละ Tab ดังโครงสร้างตัวอย่างนี้:

```python
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Callback Architecture for Tab 1 Cross-Filtering
@app.callback(
    [
        Output('graph-courses-heatmap', 'figure'),
        Output('graph-employment-rate', 'figure'),
        Output('graph-tuition-fee', 'figure')
    ],
    [
        Input('graph-graduates-bar', 'clickData'),
        Input('reset-tab1-btn', 'n_clicks')
    ]
)
def update_tab1_linked_charts(click_data, reset_clicks):
    # Determine filter context from User Click Event
    selected_program = None
    if click_data:
        selected_program = click_data['points'][0]['x']
        
    filtered_df = filter_supply_dataset(selected_program)
    
    # Re-render all linked figures reactively
    fig_courses = build_courses_figure(filtered_df)
    fig_employment = build_employment_figure(filtered_df)
    fig_tuition = build_tuition_figure(filtered_df)
    
    return fig_courses, fig_employment, fig_tuition
```

---

## 5. UI/UX & Non-Functional Specifications

1. **Theme Aesthetics:** Modern Dark Mode Scheme
   * Background: `#0f172a`
   * Card Component: `#1e293b`
   * Primary Accent: `#38bdf8` (Cyan/Teal)
   * Success: `#22c55e` | Warning: `#f59e0b` | Alert: `#ef4444`
2. **Performance Requirement:** การตอบสนองของการ Re-render กราฟแบบ Cross-filtering ต้องใช้เวลาน้อยกว่า **1.2 วินาที**
3. **Data Export Features:** มีปุ่ม Export Data (CSV) และ Export Chart (PNG/PDF) ในทุกหน้า Tab

---

## 6. Antigravity Execution Checklist

- [ ] เตรียม Data Pipelines สำหรับ Supply Data, Demand Data และ Skill Matrix
- [ ] พัฒนา Tab 1 พร้อมระบบ Cross-filtering ระหว่างทั้ง 4 กราฟ
- [ ] พัฒนา Tab 2 พร้อมระบบ Cross-filtering ระหว่างทั้ง 4 กราฟ
- [ ] พัฒนา Tab 3 สำหรับคำนวณและแสดงผล Quadrant Matrix & Alignment Index
- [ ] ตรวจสอบ Event Callbacks และ Reset State Management ในทุกหน้า