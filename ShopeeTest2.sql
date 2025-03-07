SELECT 
    buyerid, 
    DATE_FORMAT(order_time, '%Y-%m') AS order_month, 
    COUNT(orderid) AS total_orders
FROM order_tab
GROUP BY buyerid, order_month
HAVING COUNT(orderid) > 1;