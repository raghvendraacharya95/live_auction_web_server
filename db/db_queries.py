GET_LAST_ORDER_ID = """
SELECT ORDER_ID FROM live_bidding ORDER BY ORDER_ID DESC limit 1
"""

GET_ORDER_DETAILS = """
SELECT lb.ORDER_ID,
USER_ID,
lb.ITEM_ID,
CAST(CURRENT_PRICE as CHAR) as 'Price',
CAST(LAST_BID_TIME AS CHAR) AS LAST_BID_TIME,
i.status
FROM live_bidding lb
left join items as i on i.item_id = lb.item_id
where lb.ORDER_ID = %s
"""

GET_ITEM_LATEST_PRICE = """
SELECT USER_ID,
CAST(CURRENT_PRICE AS CHAR) AS CURRENT_PRICE
,CAST(LAST_BID_TIME AS CHAR) AS LAST_BID_TIME
FROM live_bidding lb
where ITEM_ID = %s
"""

GET_ALL_UNSOLD_ITEMS = """
SELECT ITEM_ID
FROM items
where COALESCE(status,'') != 'S'
"""

GET_MAX_BID_PRICE_OF_ITEM_AND_USER = """
SELECT lb.ORDER_ID
,lb.USER_ID
,u.user_name as USER_NAME
,CAST(CURRENT_PRICE AS CHAR) AS CURRENT_PRICE
,CAST(LAST_BID_TIME AS CHAR) AS LAST_BID_TIME
FROM live_bidding lb
LEFT JOIN users u on u.user_id = lb.user_id
where ITEM_ID = %s
order by lb.CURRENT_PRICE desc
limit 1
"""

GET_LAST_BID_TIME_BY_ORDER_ID = """
SELECT
CAST(LAST_BID_TIME AS CHAR) AS LAST_BID_TIME
FROM live_bidding
where ORDER_ID = %s
"""

UPDATE_ITEM_BUYER_FOUND = """
UPDATE items SET order_id = %s,
STATUS = %s
where item_id = %s
"""

# GET_ITEM_CURRENT_MAX_PRICE= """
# SELECT CAST(CURRENT_PRICE AS CHAR) AS CURRENT_PRICE
# FROM live_bidding
# where ITEM_ID = %s
# order by lb.CURRENT_PRICE
# LIMIT 1
# """