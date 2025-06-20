### Brand Share & Rank Analysis Queries
- Dataset: share_of_search (E-commerce Keyword Performance)
- Description:
  This file includes SQL Server queries for analyzing brand vs competitor performance on keyword-based product listings across e-commerce platforms.
---
### Sections Included:
1. Brand Share % by Keyword and Date
2. Brand vs Competitor Count in Top 10
3. Brand Share Trend over Time (Daily/Weekly/Monthly)
4. Product Avg Rank by Keyword Type
5. Platform-wise Brand Share per Keyword Type
6. Platform-wise Keyword Performance
7. Product Frequency in Top 3, Top 5, Top 10 (Weekly)
---
### Usage:
- Edit the date range dynamically using DATEADD or replace with a fixed date.
- For temporal trend queries, set @aggregation_level to 'Daily', 'Weekly', or 'Monthly'.
- Use in conjunction with Power BI for visual analytics.
---
### Dependencies:
- Table: share_of_search
- Columns: date, keywords, platform, rank, sponsered, brand_num, Keyword_type, pname, brands
- Ensure proper CAST(rank AS INT) where applicable.
---
1. What percentage of total results for a keyword are brand-owned products?
```
sql
SELECT 
    date,
    keywords,
    STR(
        COUNT(CASE WHEN brand_num = 1 THEN 1 END) * 100.0 / COUNT(*), 
        6, 2
    ) AS brand_share_percent
FROM share_of_search
WHERE date >= DATEADD(DAY, -7, (SELECT MAX([date]) FROM share_of_search))
GROUP BY date, keywords
ORDER BY date DESC, keywords;
```
