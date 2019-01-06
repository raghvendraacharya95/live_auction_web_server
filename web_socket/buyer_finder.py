import sys
sys.path.insert(0, '/home/acharya/Desktop/work/cars24_hackthon2/live_auction_web_server')
from db import event_db
from db import transactional_db_operation as tran_db
import time
import json
import auction_events
from datetime import datetime,timedelta

auction_window = 61

def get_date():
	return datetime.now().utcnow() +timedelta(hours=5,minutes=45)

def get_buyer_and_publish(all_live_items):
	print all_live_items
	for items in all_live_items:
		item_id = int(items["ITEM_ID"])
		max_price_detail = tran_db.get_item_current_max_price_details(item_id)
		if max_price_detail:
			user_id = max_price_detail["USER_ID"]
			current_price = max_price_detail["CURRENT_PRICE"]
			str_bid_time = max_price_detail["LAST_BID_TIME"]
			order_id = int(max_price_detail["ORDER_ID"])
			user_name = str(max_price_detail["USER_NAME"])
			bid_time = datetime.strptime(str_bid_time,"%Y-%m-%d %H:%M:%S")
			current_time = get_date()
			print  bid_time+timedelta(minutes = auction_window) , current_time
			if bid_time+timedelta(minutes = auction_window) < current_time:
				##update buyer found
				print "Updating item buyer with order id"
				print item_id,order_id
				update_flag = tran_db.update_buyer(str(item_id),str(order_id))
				print update_flag,"update_flag"
				if update_flag:
					##publish this event
					auction_events.generate_buyer_found_event(item_id,user_id,current_price,user_name)

def main():
	pass
	while True:
		all_live_items = tran_db.get_all_unsold_items()
		get_buyer_and_publish(all_live_items)
		time.sleep(10)


if __name__ == '__main__':
	main()