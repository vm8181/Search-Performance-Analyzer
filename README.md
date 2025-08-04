# 🔍 Know Your Share of Search – Power BI Dashboard

This repository contains an end-to-end automated solution to track and analyze the **Share of Search performance** of the *Yogabar* brand across Amazon and Flipkart. The project automates keyword performance extraction, database integration, data cleaning, and builds an interactive Power BI dashboard to generate insights on brand visibility, product performance, and competitive benchmarking.

---

## 🚀 Project Overview

- **Objective**: Track and benchmark the online visibility of Yogabar products across Amazon & Flipkart using relevant keywords.
- **Tools Used**:
  - 🐍 Python (Selenium, Pandas, SqlAlchemy)
  - 🧾 SQL Server / Azure Data Studio
  - 🧪 Power Query (Power BI)
  - 📊 Power BI (DAX, Visuals, Bookmarks, Drillthrough)
  - 🟩Micorosoft Excel(Pivot Tables)

---

## 🧩 Workflow Summary

### 1. Data Collection (Python + Selenium)
- Automated scraping of:
  - **Keyword-based crawling**
  - **Organic vs Sponsored results**
  - **Product name, code, price, placement, brand**
- Platform: **Amazon & Flipkart**
- Output: Cleaned `.xlsx` file created per run

### 2. Data Integration
- Automated ingestion into **SQL Server** / **Azure Data Studio**
- **View layer** created for unified, cleaned datasets:
  - Removes duplicates, harmonizes formats, categorizes keywords

### 3. Data Preparation (Power Query)
- Import SQL view using native SQL connector
- Perform light transformations:
  - Date parsing, categorization
  - Custom columns for branded/generic/competitor types

### 4. Report Development (Power BI)
Three core sections:
#### 🔍 **Search Section**
- Overall keyword performance (% share)
- Trends in brand vs competitor search visibility
- Organic vs Sponsored split

![image](https://github.com/user-attachments/assets/12206002-b589-4126-9038-04e2017237e1)

#### 🥊 **Competitive Benchmarking**
- Brand share vs key competitors (Kellogg’s, RiteBite, etc.)
- Platform-specific comparison (Amazon vs Flipkart)
- Share by placement group (top 10, 11–20, etc.)

![image](https://github.com/user-attachments/assets/08295ae2-0c24-4ae2-8049-06e127d9afd9)

#### 📦 **Product Details**
- Product-level insights with placement history
- Price vs rank correlation
- Drillthrough to ASIN-level performance

![image](https://github.com/user-attachments/assets/69f09bc4-4a2f-4098-b504-c966016aba02)

---

## 📌 Features Implemented

| Feature             | Description |
|--------------------|-------------|
| ✅ Automation       | End-to-end scraping + data push to DB |
| ✅ Data Modeling    | Relationships between fact and dimension tables |
| ✅ DAX Measures     | Share %, Rank Index, Visual Calculation, Rank Buckets |
| ✅ Bookmarks        | Toggle views across sections |
| ✅ Drillthrough     | Product-level exploration |
| ✅ Visuals          | Scatterplots, KPIs, stacked bars, small multiples |
| ✅ Segmentation     | Generic vs Branded vs Competitor terms |

---

## 🧠 Key Insights

- **Yogabar** dominates share of search on branded keywords but lacks visibility in generic terms like *protein bar*, *oatmeal*.
- **Competitors like RiteBite** outperform on high-value placements for non-branded queries.
- **Sponsored listings** play a crucial role in ranking for high-intent keywords.
- Strong correlation found between **lower pricing and better placement** in some segments.

---

## 📈 Recommendations

- 💰 **Increase Sponsored Campaigns** for generic and competitive keywords with weak share.
- 🧠 **Improve SEO** metadata on Amazon listings to rank organically for broader terms.
- 🎯 **Monitor price vs rank weekly** to optimize product pricing for better placement.
- 🧪 **A/B test creatives** on Flipkart, where competition is less saturated but Yogabar trails.

---

## 🌐 Connect with Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/vikashm1996)  
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-4B0082?logo=internet-explorer)](https://vikashmishra.co.in/)

