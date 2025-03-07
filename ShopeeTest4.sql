SELECT 
    b.country, 
    COUNT(DISTINCT CASE WHEN MOD(a.itemid, 2) = 0 THEN a.buyerid END) AS even_item_buyers,
    COUNT(DISTINCT CASE WHEN MOD(a.itemid, 2) = 1 THEN a.buyerid END) AS odd_item_buyers
FROM order_tab a
JOIN user_tab b ON a.buyerid = b.buyerid
GROUP BY b.country;