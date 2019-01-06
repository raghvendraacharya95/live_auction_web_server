from transactional_db import DB
from db_queries import *

global_server = "localhost"

def get_last_order_id():
	db = DB(global_server)
	last_order_id = db.execute_query(GET_LAST_ORDER_ID,execute_query=True,commit=True,return_result=True,return_id=True)
	return last_order_id[0]["ORDER_ID"]

def get_order_detail(order_id):
	db = DB(global_server)
	details = db.execute_query(GET_ORDER_DETAILS,params=(order_id),execute_query=True,commit=True,return_result=True,return_id=True)
	return details

def get_latest_price_of_item(item_id):
	db = DB(global_server)
	user_wise_item_price = db.execute_query(GET_ITEM_LATEST_PRICE,params=(item_id),execute_query=True,commit=True,return_result=True,return_id=True)
	return user_wise_item_price

def get_all_unsold_items():
	db = DB(global_server)
	lits_unsold_items = db.execute_query(GET_ALL_UNSOLD_ITEMS,execute_query=True,commit=True,return_result=True,return_id=True)
	return lits_unsold_items

def get_item_current_max_price_details(item_id):
	db = DB(global_server)
	item_current_max_price = db.execute_query(GET_MAX_BID_PRICE_OF_ITEM_AND_USER,params=(item_id),execute_query=True,commit=True,return_result=True,return_id=True)
	print item_current_max_price
	if item_current_max_price:
		return item_current_max_price[0]

def get_last_bid_time(order_id):
	db = DB(global_server)
	last_bid_time_dtl = db.execute_query(GET_LAST_BID_TIME_BY_ORDER_ID,params=(order_id),execute_query=True,commit=True,return_result=True,return_id=True)
	if last_bid_time_dtl:
		return last_bid_time_dtl[0]

def update_buyer(item_id,order_id):
	db = DB(global_server)
	db.execute_query(UPDATE_ITEM_BUYER_FOUND,params=(order_id,"S",item_id),execute_query=True,commit=True,return_result=True,return_id=True)
	return True

