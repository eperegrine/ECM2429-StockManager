SELECT SI.location, P.name, SI.quantity, P.target_level
FROM StockItems SI LEFT JOIN Products P on P.id = SI.product_id;

SELECT P.name, SUM(SI.quantity) AS "stock_level", P.target_level
FROM StockItems SI LEFT JOIN Products P on P.id = SI.product_id
GROUP BY P.name;