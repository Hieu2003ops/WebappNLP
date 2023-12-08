/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [Tên sp]
      ,[Comments]
      ,[Time rating]
      ,[Mô tả sản phẩm]
      ,[Chất lượng sản phẩm]
      ,[Chất lượng vận chuyển]
  FROM [Group6].[dbo].[Shopee]


SELECT DISTINCT [Tên sp]
FROM [Shopee]
--kiểm tra Comments
SELECT DISTINCT [Comments]
FROM [Shopee]
-- xác nhận có null , lọc null 
DELETE FROM [Shopee]
WHERE [Comments] IS NULL

--kiểm tra cột Mô tả Sản phẩm 
SELECT DISTINCT [Mô tả sản phẩm]
FROM [Shopee]
-- xác nhận có null của cột Mô tả sản phẩm
DELETE FROM [Shopee]
WHERE [Mô tả sản phẩm] IS NULL

-- kiểm tra cột Chất lượng sản phẩm
SELECT DISTINCT [Chất lượng sản phẩm]
FROM [Shopee]
--xác nhận có null cột Chất lượng sản phẩm 
DELETE FROM [Shopee]
WHERE [Chất lượng sản phẩm] IS NULL

-- kiểm tra cột Chất lượng vận chuyển 
SELECT DISTINCT [Chất lượng vận chuyển]
FROM [Shopee]
-- xác nhận có null cột Chất lượng vận chuyển 
DELETE FROM [Shopee]
WHERE [Chất lượng vận chuyển] IS NULL

-- lọc các từ thừa , lấy mỗi tên sản phẩm 
UPDATE [Shopee]
SET [Tên sp] = LTRIM(SUBSTRING([Tên sp], CHARINDEX('Yêu thích', [Tên sp]) + LEN('Yêu thích'), LEN([Tên sp])))
WHERE CHARINDEX('Yêu thích', [Tên sp]) = 1

-- chuyển các giá trị cảm xúc Negative , Neutral, Positive với Negative mang giá trị 0 , Neutral mang giá trị 1 , Positive mang giá trị 2 
UPDATE [Shopee]
SET [Mô tả sản phẩm] = CASE
    WHEN [Mô tả sản phẩm] = 'Negative' THEN '0'
    WHEN [Mô tả sản phẩm] = 'Neutral' THEN '1'
    WHEN [Mô tả sản phẩm] = 'Positive' THEN '2'
    ELSE [Mô tả sản phẩm]
END,
[Chất lượng sản phẩm] = CASE
    WHEN [Chất lượng sản phẩm] = 'Negative' THEN '0'
    WHEN [Chất lượng sản phẩm] = 'Neutral' THEN '1'
    WHEN [Chất lượng sản phẩm] = 'Positive' THEN '2'
    ELSE [Chất lượng sản phẩm]
END,
[Chất lượng vận chuyển] = CASE
    WHEN [Chất lượng vận chuyển] = 'Negative' THEN '0'
    WHEN [Chất lượng vận chuyển] = 'Neutral' THEN '1'
    WHEN [Chất lượng vận chuyển] = 'Positive' THEN '2'
    ELSE [Chất lượng vận chuyển]
END
-- kiểm tra lại 
select * from [Group6].[dbo].[Shopee]