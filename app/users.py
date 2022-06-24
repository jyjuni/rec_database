
QUERY_ORDER_HISTORY = """
SELECT order_id, item_name, retailer_name, brand, quantity, order_time 
FROM order_detail o, users u, item i, retailer r
WHERE u.user_id={}
AND u.user_id=o.user_id
AND i.item_id=o.item_id 
AND r.retailer_id=i.retailer_id
ORDER BY order_time DESC;
"""

SHOW_AD = """
SELECT item_name, ad_title FROM ad a, item i where i.item_id=a.item_id ORDER BY end_date desc LIMIT 3;
"""

INSERT_USER = """
INSERT INTO users(user_id, user_name, password, created_time) 
VALUES({}, '{}', '{}', NOW())
"""

INSERT_RATING = """
INSERT INTO rating(order_id, rated_time, rated_score) VALUES({}, NOW(), {})
"""

INSERT_ORDER = """
INSERT INTO order_detail(order_id, item_id, user_id, quantity, order_time) VALUES({}, {},{},{},NOW())
"""

def query_order_history(user_id):
    return QUERY_ORDER_HISTORY.format(user_id)

def query_insert_newuser(user_id, user_name, password):
    return INSERT_USER.format(user_id, user_name, password)

def query_ads():
    return SHOW_AD

def query_items(search_by, key):
    # search_by = SelectField('Search by', choices=[(1, 'item_id'), (2, 'item_name'), (3,'retailer'), (4, 'color'), (5,'brand')])
    QUERY = "select item_id, item_name, retailer_name, price, brand, color, description from item i, retailer r WHERE i.retailer_id=r.retailer_id "
    if search_by=="1":
        QUERY += f"AND item_id = {key}"
    elif search_by=="2":
        QUERY += f"AND item_name LIKE '%%{key}%%'"
    elif search_by=="3":
        QUERY += f"AND retailer_name LIKE '%%{key}%%'"
    elif search_by=="4":
        QUERY += f"AND color LIKE '%%{key}%%'"
    else:
        QUERY += f"AND brand LIKE '%%{key}%%'"
    return QUERY
