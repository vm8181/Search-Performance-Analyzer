USE [Yogabar]
GO

/****** Object:  View [dbo].[share_of_search]    Script Date: 12-03-2025 21:18:28 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



ALTER VIEW [dbo].[share_of_search] AS
WITH search_view AS
(SELECT a.[date], a.keywords, a.pname, a.[asin] [code], a.price, a.prod_img, a.[rank], a.sponsered, a.[url], 'Amazon' [platform], b.brands,
CASE WHEN b.brands LIKE '%yogabar%' OR b.brands LIKE '%yoga bar%' THEN 1 ELSE 0 END [brand_num] FROM Search a, 
brand_master b WHERE a.[asin] = b.platform_code
UNION ALL
SELECT fk.[date], fk.keywords, fk.pname, fk.code , fk.price, fk.prod_img, fk.[rank], fk.sponsered, fk.[url], 'Flipkart' [platform], b.brands,
CASE WHEN b.brands LIKE '%yogabar%' OR b.brands LIKE '%yoga bar%' THEN 1 ELSE 0 END [status_num] FROM fk_search fk,
fk_brand_master b WHERE fk.code = b.platform_code)
SELECT s.date, s.keywords, m.Keyword_type, s.pname, s.code, s.price, s.prod_img, s.rank, s.sponsered, s.url, s.platform, s.brands, 
s.brand_num FROM search_view s LEFT JOIN keyword_master m ON s.keywords = m.Keywords
GO

SELECT Search.keywords, keyword_master.Keywords FROM keyword_master RIGHT JOIN Search ON keyword_master.Keywords = Search.keywords

INSERT INTO keyword_master (Keywords, keyword_type)
SELECT DISTINCT Search.keywords, 'generic'
FROM Search
LEFT JOIN keyword_master ON keyword_master.Keywords = Search.keywords
WHERE keyword_master.Keywords IS NULL;

UPDATE keyword_master
SET Keyword_type = 'Generic'
Where Keyword_type = 'generic'


