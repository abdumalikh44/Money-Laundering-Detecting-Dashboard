SELECT 
    buyer_id, 
    shop_id, 
    MIN(order_date) AS first_order_date, 
    MAX(order_date) AS latest_order_date
FROM orders
GROUP BY buyer_id, shop_id;
