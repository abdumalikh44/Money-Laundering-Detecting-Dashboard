SELECT 
    p.shopid, 
    COUNT(o.orderid) AS total_orders, 
    p.item_views, 
    p.total_clicks, 
    p.impressions, 
    COUNT(o.orderid) / NULLIF(p.item_views, 0) AS order_to_views_ratio,
    p.total_clicks / NULLIF(p.impressions, 0) AS clicks_to_impressions_ratio
FROM performance_tab p
LEFT JOIN order_tab o ON p.shopid = o.shopid
GROUP BY p.shopid, p.item_views, p.total_clicks, p.impressions;