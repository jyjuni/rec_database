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
WHERE retailer_id='{}';
"""
# Query item details for retailer + 
QUERY_ITEMS_INFO = """
WITH a AS(
SELECT i.item_id, item_name, price, brand FROM item i WHERE retailer_id='{}'
),
b AS(
SELECT it.item_id, rated_score as item_rating
FROM rating r, order_detail o, item it
WHERE o.order_id = r.order_id AND
o.item_id = it.item_id
AND it.retailer_id= '{}'
),
c AS(
SELECT quantity, i.item_id 
FROM order_detail o, item i
WHERE i.retailer_id='{}' AND i.item_id=o.item_id
)
SELECT a.item_id, item_name, price, brand, TRUNC(AVG(item_rating),1) item_rating, COALESCE(SUM(quantity),0) item_total_sale
FROM a
LEFT OUTER JOIN b
ON a.item_id = b.item_id
LEFT OUTER JOIN c
ON a.item_id = c.item_id
GROUP BY a.item_id, item_name, price, brand;
"""

# Query ad details for retailer
QUERY_AD_INFO = """
SELECT ad_id, a1.item_id, item_name, ad_title, MAX(end_date) valid_until, SUM(amount) as ad_price
FROM ad a1
JOIN ad_payment a2
ON a1.ad_payment_id=a2.ad_payment_id
JOIN item i
ON i.item_id=a1.item_id
WHERE i.item_id IN (SELECT item_id FROM item WHERE retailer_id = '{}')
GROUP BY ad_id, a1.item_id, item_name, ad_title
"""

def query_retailer_info(retailer_id):
    return QUERY_RETAILER_INFO.format(retailer_id)

def query_items_info(retailer_id):
    return QUERY_ITEMS_INFO.format(retailer_id, retailer_id, retailer_id)

def query_ads_info(retailer_id):
    return QUERY_AD_INFO.format(retailer_id)

    
