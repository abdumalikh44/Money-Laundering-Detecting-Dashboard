SELECT o.buyerid, u.country, SUM(o.gmv) AS total_gmv
FROM order_tab o
JOIN user_tab u ON o.buyerid = u.buyerid
WHERE u.country IN ('ID', 'SG')
GROUP BY o.buyerid, u.country
ORDER BY total_gmv DESC
LIMIT 10;