QUERY_ORDER_HISTORY = """
SELECT order_id, item_name, retailer_name, brand, quantity, order_time 
FROM order_detail o, users u, item i, retailer r
WHERE u.user_id={}
AND u.user_id=o.user_id
AND i.item_id=o.item_id 
AND r.retailer_id=i.retailer_id
ORDER BY order_time DESC;
"""

def query_order_history(user_id):
    return QUERY_ORDER_HISTORY.format(user_id)

