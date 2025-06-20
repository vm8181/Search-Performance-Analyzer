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
## 1. What percentage of total results for a keyword are brand-owned products?
```sql
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
## 2. Among top 10 ranked items for each keyword, how many belong to the brand vs competitors?
```sql
SELECT 
    date,
    Keyword_type,
    keywords,
    COUNT(CASE WHEN brand_num = 1 THEN 1 END) AS brand_count_top_10,
    COUNT(CASE WHEN brand_num = 0 THEN 1 END) AS comp_count_top_10
FROM share_of_search
WHERE CAST(rank AS INT) <= 10 AND date >= DATEADD(DAY, -7, (SELECT MAX([date]) FROM share_of_search))
GROUP BY date, keywords, Keyword_type
ORDER BY Keyword_type ASC, date DESC;
```
## 3. How does this trend over time? (Brand Share in Top 10)
```sql
DECLARE @aggregation_level VARCHAR(10) = 'Monthly';
WITH Aggregated AS (
    SELECT 
        [date],
        CASE 
            WHEN @aggregation_level = 'Daily' THEN CAST([date] AS DATE)
            WHEN @aggregation_level = 'Weekly' THEN DATEADD(DAY, -DATEPART(WEEKDAY, [date]) + 1, CAST([date] AS DATE))
            WHEN @aggregation_level = 'Monthly' THEN DATEFROMPARTS(YEAR([date]), MONTH([date]), 1)
        END AS period,
        DATEPART(MONTH, [date]) AS month_num,
        DATEPART(WEEK, [date]) - DATEPART(WEEK, DATEFROMPARTS(YEAR([date]), MONTH([date]), 1)) + 1 AS week_in_month,
        brand_num,
        CAST(rank AS INT) AS rank
    FROM share_of_search
)
SELECT 
    CASE 
        WHEN @aggregation_level = 'Monthly' THEN FORMAT(period, 'MMM-yyyy')
        WHEN @aggregation_level = 'Weekly' THEN FORMAT(DATEFROMPARTS(YEAR(period), month_num, 1), 'MMM') + ', Week' + CAST(week_in_month AS VARCHAR(2))
        ELSE FORMAT(period, 'yyyy-MM-dd')
    END AS display_period,
    period AS original_period,
    CAST(COUNT(CASE WHEN brand_num = 1 AND rank <= 10 THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN rank <= 10 THEN 1 END), 0) AS DECIMAL(5,2)) AS top_10_brand_share_percent
FROM Aggregated
GROUP BY 
    CASE 
        WHEN @aggregation_level = 'Monthly' THEN FORMAT(period, 'MMM-yyyy')
        WHEN @aggregation_level = 'Weekly' THEN FORMAT(DATEFROMPARTS(YEAR(period), month_num, 1), 'MMM') + ', Week' + CAST(week_in_month AS VARCHAR(2))
        ELSE FORMAT(period, 'yyyy-MM-dd')
    END,
    period
ORDER BY period;
```
## 4. Products Avg Rank in different keyword Types in last 30 days

```sql
SELECT 
    pname,
    ISNULL([Brand],0) AS Brand_Keyword_Rank,
    ISNULL([Competitor],0) AS Competitor_Keyword_Rank,
    ISNULL([Generic],0) AS Generic_Keyword_Rank
FROM (
    SELECT 
        Keyword_type, 
        pname, 
        CAST(rank AS INT) AS rank
    FROM share_of_search
    WHERE brand_num = 1
      AND date >= DATEADD(DAY, -30, (SELECT MAX([date]) FROM share_of_search))
) AS SourceTable
PIVOT (
    AVG(rank)
    FOR Keyword_type IN ([Brand], [Competitor], [Generic])
) AS PivotTable
ORDER BY pname;
```

## 5. Platform and keyword type wise Brand share for Last 30 Days
```sql
SELECT 
    platform,
    ISNULL([Brand], 0) AS Brand_Keyword_Share,
    ISNULL([Competitor], 0) AS Competitor_Keyword_Share,
    ISNULL([Generic], 0) AS Generic_Keyword_Share
FROM (
    SELECT 
        platform,
        Keyword_type,
        STR(COUNT(CASE WHEN brand_num = 1 THEN 1 END) * 100.0 / COUNT(date),6,2) AS brand_share_percent
    FROM share_of_search
    WHERE date >= DATEADD(DAY, -30, (SELECT MAX([date]) FROM share_of_search))
    GROUP BY platform, Keyword_type
) AS SourceTable
PIVOT (
    MAX(brand_share_percent)
    FOR Keyword_type IN ([Brand], [Competitor], [Generic])
) AS PivotTable
ORDER BY platform;
```

## 6. Keywords share on different platforms
```sql
SELECT 
    Keyword_type,
    Keywords,
    ISNULL([Amazon], 0) AS Amazon_Share,
    ISNULL([Flipkart], 0) AS Flipkart_Share
FROM (
    SELECT 
        Keyword_type,
        keywords,
        platform,
        STR(COUNT(CASE WHEN brand_num = 1 THEN 1 END) * 100.0 / COUNT(date),6,2) AS brand_share_percent
    FROM share_of_search
    WHERE date >= DATEADD(DAY, -30, (SELECT MAX([date]) FROM share_of_search))
    GROUP BY platform, keywords, Keyword_type
) AS SourceTable
PIVOT (
    MAX(brand_share_percent)
    FOR platform IN ([Amazon], [Flipkart])
) AS PivotTable
ORDER BY keyword_type;
```

## 7. Products Frequncy under TOP3, Top5 and TOP10 ranking Last week
```sql
SELECT 
    platform,
    keywords,
    SUM(CASE WHEN CAST(rank AS INT) <= 3 THEN 1 ELSE 0 END) AS top_3_count,
    SUM(CASE WHEN CAST(rank AS INT) <= 5 THEN 1 ELSE 0 END) AS top_5_count,
    SUM(CASE WHEN CAST(rank AS INT) <= 10 THEN 1 ELSE 0 END) AS top_10_count
FROM share_of_search
WHERE brand_num = 1
  AND date >= DATEADD(DAY, -7, (SELECT MAX([date]) FROM share_of_search))
GROUP BY platform, keywords
HAVING 
    SUM(CASE WHEN CAST(rank AS INT) <= 3 THEN 1 ELSE 0 END) > 0 OR
    SUM(CASE WHEN CAST(rank AS INT) <= 5 THEN 1 ELSE 0 END) > 0 OR
    SUM(CASE WHEN CAST(rank AS INT) <= 10 THEN 1 ELSE 0 END) > 0;
```

## 8. TOP 10 Brand are ranked #1 most frequently in last 30 days?
```sql
WITH cte AS (
    SELECT 
        brands,
        COUNT(*) AS rank_1_count
    FROM share_of_search
    WHERE CAST(rank AS INT) = 1 
      AND date >= DATEADD(DAY, -30, (SELECT MAX([date]) FROM share_of_search))
    GROUP BY brands
),
_rank AS (
SELECT 
    brands,
    rank_1_count,
    DENSE_RANK() OVER(ORDER BY rank_1_count DESC) AS brand_rank
FROM cte)
SELECT brands, rank_1_count FROM _rank
WHERE bra
nd_rank <= 10;
```
## 9. Average Rank and Frequency of Brand's Product in last 7 days
```sql
SELECT 
    platform,
    pname,
    AVG(CAST(rank AS INT)) AS avg_rank,
    SUM(CASE WHEN brand_num = 1 THEN 1 END) AS [frequency]
FROM share_of_search
WHERE date >= DATEADD(DAY, -7, (SELECT MAX([date]) FROM share_of_search)) and brand_num = 1
GROUP BY pname,platform
ORDER BY platform, avg_rank ASC;
```

## 10. Which products improved their position over time?
```sql
WITH RankHistory AS (
    SELECT 
        platform,
        keywords,
        code,
        pname,
        date,
        RANK() OVER (PARTITION BY code ORDER BY date) AS seq,
        CAST(rank AS INT) rank
    FROM share_of_search
    WHERE brand_num = 1
)
SELECT
    a.platform,
    a.keywords,
    a.code,
    a.pname,
    MIN(a.rank) AS start_rank,
    MAX(b.rank) AS end_rank,
    MIN(a.date) AS start_date,
    MAX(b.date) AS end_date,
    MIN(a.rank) - MAX(b.rank) AS rank_improvement
FROM RankHistory a
JOIN RankHistory b ON a.code = b.code AND a.seq = 1 AND b.seq = (
    SELECT MAX(seq) FROM RankHistory WHERE code = a.code
)
GROUP BY a.platform, a.code, a.pname, a.keywords;
```
## 11. What percentage of top-ranked brand products are sponsored vs organic?
```sql
SELECT 
    date,
    STR(
        STR(COUNT(CASE WHEN brand_num = 1 AND sponsered = 'Sponsored' AND CAST(rank AS INT) <= 10 THEN 1 END) * 100.0 /
        NULLIF(COUNT(CASE WHEN brand_num = 1 AND CAST(rank AS INT) <= 10 THEN 1 END), 0), 
    2),6,2) AS sponsored_percent_in_top10,
    
    STR(
        COUNT(CASE WHEN brand_num = 1 AND sponsered = 'Organic' AND CAST(rank AS INT) <= 10 THEN 1 END) * 100.0 /
        NULLIF(COUNT(CASE WHEN brand_num = 1 AND CAST(rank AS INT) <= 10 THEN 1 END), 0),6,2) AS organic_percent_in_top10
FROM share_of_search
WHERE date >= DATEADD(DAY, -30, (SELECT MAX([date]) FROM share_of_search))
GROUP BY date
ORDER BY date;
```
## 12. Which keywords are the most effective for sponsorship?
```sql
SELECT 
    keywords,
    COUNT(*) AS sponsored_appearances,
    AVG(CAST(rank AS INT)) AS avg_sponsored_rank
FROM share_of_search
WHERE brand_num = 1 AND sponsered = 'Sponsored'
GROUP BY keywords
HAVING COUNT(*) >= 3
ORDER BY avg_sponsored_rank ASC;
```

## 13. Which competitor products show up for brand keywords?
```sql
SELECT 
    date,
    keywords,
    pname,
    brands,
    CAST(rank AS INT) AS rank
FROM share_of_search
WHERE Keyword_type = 'Brand' 
  AND brand_num = 0
ORDER BY date, keywords, rank;
```
## 14. Are competitors bidding on the brand’s keywords and ranking high?
```sql
SELECT 
    date,
    platform,
    keywords,
    pname,
    brands,
    CAST(rank AS INT) AS rank
FROM share_of_search
WHERE Keyword_type = 'Brand'
  AND brand_num = 0
  AND sponsered = 'Sponsored'
  AND CAST(rank AS INT) <= 5
ORDER BY date, keywords, rank;
```

## 15. How often do competitors rank above brand products for a keyword?
```sql
SELECT DISTINCT pname, AVG(CAST(rank AS INT)) rank
FROM share_of_search
WHERE brand_num = 1
GROUP BY pname
EXCEPT
SELECT DISTINCT pname, AVG(CAST(rank AS INT)) rank
FROM share_of_search
WHERE brand_num = 1 AND CAST(rank AS INT) <= 10
GROUP BY pname
```

## 16. Which brand products have high rank (i.e., poor visibility) but no sponsorship?
```sql
SELECT 
    date,
    keywords,
    pname,
    CAST(rank AS INT) AS rank,
    sponsered
FROM share_of_search
WHERE brand_num = 1 
  AND CAST(rank AS INT) > 10 
  AND sponsered != 'Sponsored'
ORDER BY rank DESC;
```
