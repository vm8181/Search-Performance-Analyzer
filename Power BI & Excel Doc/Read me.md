# E-Commerce Brand Performance Dashboard - Excel Guide

## 📊 Overview:
This Excel dashboard compares Brand vs Competitor performance on Amazon and Flipkart platforms using metrics like share %, product ranks, and placements across months. It includes dynamic filters and slicers for easy navigation.

---

## 📁 SHEET STRUCTURE

### 1️⃣ `Share Trend by Keyword`
- Visualizes **monthly share%** (Jul23–Oct23) for each keyword
- Split by `Brand` and `Competitor`
- Color scale to show performance from low (red) to high (green)
- Controlled by slicers:
  - `Ad Type` (Organic, Sponsored)
  - `Type` (Brand, Competitor, Generic)
  - `Platform` (Amazon, Flipkart)
  - `Placement Bin` (e.g., 1-10, 11-20...)

![image](https://github.com/user-attachments/assets/14125a9c-d5e8-4107-a575-5d2910ef82a5)

---

### 2️⃣ `Brand-Wise Monthly Share`
- Pivot table showing **brand-level monthly share%** with Grand Total
- Color scale to highlight strongest brands overall
- Controlled by:
  - Slicers + Dropdown for:
    - `Keyword`
    - `Placement Bin`

![image](https://github.com/user-attachments/assets/be41ba47-1001-4c75-9eed-c544530efc89)

---

### 3️⃣ `Brand vs Competitor by Placement`
- Compare **Brand vs Competitor share%** by placement bins (1-10, 11-20, etc.)
- Month-wise comparison across Jul23–Oct23
- Use slicer:
  - `Keyword`
- Useful to understand **visibility by position**

![image](https://github.com/user-attachments/assets/9ecd2ec2-460c-496d-8944-59ed2303ed5e)

---

### 4️⃣ `Product Listing by Keyword/Date`
- Raw listing of products for a selected keyword and date
- Fields include:
  - ASIN/Code
  - Product Name
  - Ad Type (Organic/Sponsored)
  - Price
  - Product Rank (1 to 10)
- Controlled by:
  - `Keyword` (dropdown)
  - `Date` (calendar input or manual)
  - `Placement Bin` (1-10)

  ![image](https://github.com/user-attachments/assets/3abb1494-2bdc-4624-ba8d-134ee71f017d)


---

## 🧮 METRICS USED

| Metric             | Description                                         |
|--------------------|-----------------------------------------------------|
| Brand's Share %     | Share of keyword listings owned by the brand        |
| Product Rank        | Position in search results based on filters         |
| Placement Bin       | Groupings like 1-10, 11-20 based on search rank     |
| Grand Total %       | Average share across selected months                |

---

## 🎛️ INTERACTIVE FILTERS

| Filter Type  | Field         | Description                       |
|--------------|---------------|-----------------------------------|
| Slicer       | Ad Type       | Organic vs Sponsored              |
| Slicer       | Type          | Brand vs Competitor vs Generic    |
| Slicer       | Platform      | Amazon vs Flipkart                |
| Dropdown     | Placement Bin | 1-10, 11-20, etc.                 |
| Dropdown     | Keyword       | Specific keyword focus            |
| Date Input   | Date          | Product snapshot for a given day  |

---

## 🔧 TECHNICAL NOTES

- Pivot tables: "Autofit Column Width on Update" = **Disabled**
- Slicers: Set to **Don't move or size with cells**
- Conditional formatting: Applied to % fields for **heatmap coloring**
- Date field: Should be in Excel date format for dynamic filtering
- Placement bin logic is derived from product rank positions

---

## 🧭 HOW TO USE

1. Use slicers (top area) to narrow down to specific ad types, brand types, platforms.
2. Select keyword and placement bin for focused analysis.
3. View trends across months in **Sheet 1 & 2**.
4. Dive into product-level data using **Sheet 4** with date & keyword filter.
5. Compare placements and visibility in **Sheet 3**.

