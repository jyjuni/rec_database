# TOP N RETAILER IN RATING
QUERY_TOP_N_SALE="""
SELECT t.retailer_id, retailer_name, SUM(t.total_sale_quantity * t.price) total_sale_amount
FROM (
SELECT retailer_id, i.item_id, price, SUM(quantity) total_sale_quantity
FROM item i
JOIN order_detail o
ON i.item_id = o.item_id
GROUP BY i.item_id, retailer_id, price
) t
JOIN retailer r
ON r.retailer_id = t.retailer_id
GROUP BY t.retailer_id, retailer_name
ORDER BY total_sale_amount DESC
LIMIT {};"""

# TOP N RETAILER IN RATING
QUERY_TOP_N_RATING="""
SELECT t.retailer_id, retailer_name, TRUNC(retailer_rating, 1) retailer_rating
FROM (
SELECT retailer_id, AVG(rated_score) retailer_rating
FROM order_detail o, rating r, item i
WHERE o.order_id = r.order_id AND i.item_id = o.item_id
GROUP BY retailer_id
) t
JOIN retailer r1
ON r1.retailer_id = t.retailer_id
ORDER BY retailer_rating DESC
LIMIT {};"""


def query_full_info(search_by, key):
    QUERY = ""
    if search_by=="1":
        QUERY = "SELECT * FROM users WHERE user_id = '{}'"
    elif search_by=="2":
        QUERY = "SELECT * FROM retailer WHERE retailer_id = '{}'"
    elif search_by=="3":
        QUERY = "SELECT * FROM item WHERE item_id = '{}'"
    else:
        QUERY = "SELECT * FROM order_detail WHERE order_id = '{}'"
    return QUERY.format(key)



def query_top_n_amount(n=10):
    return QUERY_TOPN5_SALE.format(n)


def query_top_n_rating(n=10):
    return QUERY_TOP_N_RATING.format(n)