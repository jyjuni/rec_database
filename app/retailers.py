# Select all info except password, with total items, total sell count and total average rating and sell count
QUERY_RETAILER_INFO = """
SELECT retailer_id, retailer_name as username, created_time, industry,
(SELECT TRUNC(AVG(rated_score),1) as average_rating
FROM rating ra WHERE order_id IN (
	SELECT o.order_id 
	FROM order_detail o, item i
	WHERE o.item_id = i.item_id AND i.retailer_id = r.retailer_id
)),
(SELECT SUM(t.total_sale_quantity * t.price) total_sale_amount
FROM (
SELECT i.item_id, price, SUM(quantity) total_sale_quantity
FROM item i
JOIN order_detail o
ON i.item_id = o.item_id
WHERE i.retailer_id = r.retailer_id
GROUP BY i.item_id, price
) t
)
FROM retailer r
WHERE retailer_id=:retailer_id;
"""
# Query item details for retailer + 
QUERY_ITEMS_INFO = """
WITH a AS(
SELECT i.item_id, item_name, price, brand, color FROM item i WHERE retailer_id=:retailer_id
),
b AS(
SELECT it.item_id, rated_score as item_rating
FROM rating r, order_detail o, item it
WHERE o.order_id = r.order_id AND
o.item_id = it.item_id
AND it.retailer_id= :retailer_id
),
c AS(
SELECT quantity, i.item_id 
FROM order_detail o, item i
WHERE i.retailer_id=:retailer_id AND i.item_id=o.item_id
)
SELECT a.item_id, item_name, price, brand, color, TRUNC(AVG(item_rating),1) item_rating, COALESCE(SUM(quantity),0) item_total_sale
FROM a
LEFT OUTER JOIN b
ON a.item_id = b.item_id
LEFT OUTER JOIN c
ON a.item_id = c.item_id
GROUP BY a.item_id, item_name, price, brand, color
ORDER BY a.item_id;
"""

# Delete Item
DELETE_ITEM = """
DELETE FROM item
WHERE item_id=:item_id;
"""

# Query ad details for retailer
QUERY_AD_INFO = """
SELECT ad_id, a1.item_id, item_name, ad_title, MAX(end_date) valid_until, SUM(amount) as ad_price
FROM ad a1
JOIN ad_payment a2
ON a1.ad_payment_id=a2.ad_payment_id
JOIN item i
ON i.item_id=a1.item_id
WHERE i.item_id IN (SELECT item_id FROM item WHERE retailer_id = :retailer_id)
GROUP BY ad_id, a1.item_id, item_name, ad_title
ORDER BY ad_id DESC;
"""

# Insert new retailer
INSERT_RETAILER = """
INSERT INTO retailer(retailer_id, retailer_name, password, created_time) 
VALUES(:retailer_id, :retailer_name, :password, NOW())
"""


INSERT_AD = """
INSERT INTO ad(ad_id, item_id, ad_title, start_date, end_date, ad_payment_id)
VALUES(:ad_id, :item_id, :ad_title, TO_DATE(:start_date,'YYYY-MM-DD'), TO_DATE(:end_date,'YYYY-MM-DD'), :ad_payment_id);
"""

def query_insert_newretailer(user_id, user_name, password):
    return INSERT_RETAILER.format(user_id, user_name, password)

def query_retailer_info(retailer_id):
    return QUERY_RETAILER_INFO.format(retailer_id)

def query_items_info(retailer_id):
    return QUERY_ITEMS_INFO.format(retailer_id, retailer_id, retailer_id)

def change_items_info(item_id, item_name, price, brand, description, color):
    set_query = []
    if item_name:
        set_query.append(f"item_name='{item_name}'") 
    if price:
        set_query.append(f"price={price}")
    if brand:
        set_query.append(f"brand='{brand}'")
    if description:
        set_query.append(f"description='{description}'")
    if color:
        set_query.append(f"color='{color}'")
    if not set_query: # no field changed
        return None
    change_items_query =  "UPDATE item SET " + ",".join(set_query) + f" WHERE item_id={item_id} RETURNING *;" 

def query_ads_info(retailer_id):
    return QUERY_AD_INFO.format(retailer_id)
