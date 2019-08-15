# test test
import sys
sys.path.insert(0, '/home/acharya/Desktop/work/cars24_hackthon2/live_auction_web_server')
from db import event_db
from db import transactional_db_operation as tran_db
import time
import json
import auction_events
from datetime import datetime,timedelta


def get_all_unsold_items():
	all_live_items = tran_db.get_all_unsold_items()
	return all_live_items

def get_all_live_items():
	all_live_items = get_all_unsold_items()
	all_items_price_dict = dict()
	for items in all_live_items:
		item_id = int(items["ITEM_ID"])
		item_price_dtl = tran_db.get_latest_price_of_item(int(item_id))
		if str(item_id) not in all_items_price_dict:
			all_items_price_dict.update({str(item_id):item_price_dtl})
	return all_items_price_dict

def publish_item_price(item_id,user_price_list):
	for user_price in user_price_list:
		auction_events.generate_change_bid_price_events(item_id,str(user_price["USER_ID"]),str(user_price["CURRENT_PRICE"]))

def publish_current_max_price():
	all_live_items = get_all_unsold_items()
	for items in all_live_items:
		item_id = int(items["ITEM_ID"])
		max_price_detail = tran_db.get_item_current_max_price_details(item_id)
		if max_price_detail:
			user_id = max_price_detail["USER_ID"]
			current_price = max_price_detail["CURRENT_PRICE"]
			user_name = str(max_price_detail["USER_NAME"])
			auction_events.generate_item_current_max_price_events(str(item_id),str(user_id),str(current_price),str(user_name))

def main():
	while True:		
		all_items_price_dict = get_all_live_items()
		##pulish current price in respective rooms
		for item_id in all_items_price_dict:
			publish_item_price(item_id,all_items_price_dict[item_id])
		publish_current_max_price()
		time.sleep(20)

if __name__ == '__main__':
	main()

