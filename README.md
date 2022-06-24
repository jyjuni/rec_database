# Online Shopping Platform Database

## Account Information    
The PostgreSQL account:yj2682
URL: http://34.139.146.205:8111/

## Project Description: 

This web front project seeks to simulate the online transactions between the users and the retailers. At the same time, we also included the functionality of the admin to monitor the overall transaction done on the platform and retrieve key information for analysis. 



## Pages and Sections

### Aligning with Part 1.1
All features laid out in the original proposal, except ad payment system, in part 1 have been implemented. For the Ads payment syste, since we do not have the technical ability to implement a real transaction system, we choose to set our ads price to 100 USD/day and insert a new record with ad_payment_id, calculated price and corresponding ad_id directly into `ad_payment` table.


### User 

We first let the user enter the username and the password to log into his or her account. Just like any other website, we locate the ‘Sign Up’ near the bottom of the login page to let first-time users sign up easily. We implement the signing up feature using insertion operation.

Suppose a first-time user signs up on the website (e.g user_name: jg4329 and password: wdvhui), the website will direct the user to the webpage containing the account details, order history, and advertisements. This page is of course empty and the user can start placing orders. 

When an existing user signs up to the system (e.g ​​username: Montana, password: fgsfah1255), in addition to placing orders, the user should be able to see his or her account details, as well as the order history on the website. At the same time, some advertisements are being shown to the users (the product name and some basic specifications) to influence their purchase decisions. The advertisements being shown are the latest 3 advertisements that are scheduled for today. 

When placing an order, the user might be interested to search the order based on different features. Hence, we allow the user to search the order by item_id, item name, retailer, color, and brand. The user can use this query function to search for the list of available products, complete with the item name, retailer, price, brand, color, and description. Subsequently, the user can place the order with its associated quantity, and the system will update the order database accordingly. 

In addition, after an order has been placed, the user can also give a rating to the product using the order id. This rating system will be used to give a rating to every item, and the retailers will know how its items are doing. 


### Retailer: 

Similar to the user, a retailer can first sign up on the website and update his or her basic information (e.g username: yj2682, password: 1122334455). This page is going to be blank at first but allows the retailer to start updating the product offerings and the advertisements on those products. 

When an existing retailer logs into the system (e.g retailer_name: choco, password: ilovesweets), the retailer will find a summary of average rating of all items, and the total revenue so far. Detailed implementation of this SQL query can be found below. The retailer also gets a summary of the product (including the system-generated item_id) and advertisements it has on the platform (how much is paid and the period in which the advertisement will be shown). The retailer then has choices to update the products and advertisements accordingly.

The retailer can also purchase advertisements using the purchase advertisement function. Advertisement prices are functionally dependent on the duration of the advertisement (in days) and the system automatically charges 100 per day for the advertisement. These advertisement prices will then be shown on the screen for the retailer to see after the purchase. 


### Admin

As the admin, we will want to have an overall view of the entire website. For example, we might want to know what are some of the transactions made by a certain user. Since all the details in the database are linked by the user_id, retailer_id, item_id, and order_id, we will be querying the database using these fields as well. For example, if we want to check user id 14 (who is Montana) we can simply search by user_id 14, and we will get the information from the results table. 
An admin also has the choice to delete any user, retailer, item or order. If the admin presses the delete button, he or she will be redirected to a confirmation page which shows the item info once again. Upon confirmation, an item will be deleted from the SQL database, and the admin will be redirected to the admin page.


## Interesting Queries
The two most interesting query function we implemented are: 

1. Query all info of the retailer (except password), with total items and total average rating and sell count
```
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
```

2. Query item details for retailer and compute average item raing, sum of sales quantity
```
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
```
