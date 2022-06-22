# USER PAGE

## LOG IN/ SIGN UP:(select + if / insert)
username, password

# USER_DETAIL PAGE
DISPLAY:
user_id, username, date of birth, gender
order history FROM order_detail

## (RECOMMEND ITEM)
DISPLAY: 
RECOMMEND TOP 3 ITEMS: item names and brand, average rating


# RETAILER PAGE
## LOG IN/ SIGN UP:(select + if / insert)
username, password

# RETAILER_DETAIL PAGE
DISPLAY:
retailer_id, retailer_name, created_time, industry
all items FROM item

## ADD ITEM
name, price, (brand, description, color)

## SEARCH BY ITEM->ITEM_DETAIL PAGE:

# ITEM_DETAIL PAGE
name, price, brand, description, color

## VIEW ADVERTISEMENT->AD_DETAIL PAGE

# AD_DETAIL PAGE
## VIEW ADVERTISEMENT:
display all advertisement's ad_title, item_name
(+add new advertisement: insert title, item)

## SEARCH BY ADVERTISEMENT:
display advertisement detail: add_title, item_name, start_date, end_date, 
amount, transaction_time FROM ad_payment


# ADMIN PAGE

## LOOKUP 

LOOKUP BY USER:
user_id FROM users
LOOKUP BY RETAILER:
retailer_id FROM retailers
LOOKUP BY ITEM:
item_id FROM item
LOOKUP BY AD:
ad_id FROM ad

## DELETE
DELETE USER
