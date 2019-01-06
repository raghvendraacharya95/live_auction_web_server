import sys
sys.path.insert(0, '/home/acharya/Desktop/work/cars24_hackthon2/live_auction_web_server')
from db import event_db
from db import transactional_db_operation as tran_db
import time
import json
import auction_events
import web_socket_server
from datetime import datetime,timedelta


def get_last_order_id():
	last_order_id = tran_db.get_last_order_id()
	if last_order_id:
		return last_order_id
	else:
		return 0

# def set_last_order_id(new_last_order_id):
# 	objEventDB=event_db.EventDB()	
# 	redis_key = objEventDB.get_redis_key("latest_order")
# 	order_id = objEventDB.redis_client.get(redis_key)
	
# 	if order_id:
# 		if int(order_id)>new_last_order_id:
# 			new_last_order_id=int(order_id)
# 	if new_last_order_id:
		# objEventDB.redis_client.set(redis_key,str(new_last_order_id))

def set_all_live_items(all_live_items):
	objEventDB=event_db.EventDB()	
	redis_key = objEventDB.get_redis_key("live_items")
	if all_live_items:
		objEventDB.redis_client.sadd(redis_key,all_live_items)

def process_new_orders(result):
	objEventDB=event_db.EventDB()
	dict_order_details={}
	live_orders=[]	
	new_last_order_id=get_last_order_id()
	all_auction_dict = {}
	orders=set()
	all_live_items = set()
	for item in result:
		# item = json.load(json.dumps(item))
		order_id = int(item["ORDER_ID"])
		orders.add(order_id)
		auction_id="_".join(["o",str(order_id)])
		user_id = int(item["USER_ID"])
		status=item["status"]
		item_id = int(item["ITEM_ID"])
		
		order_redis_key=objEventDB.get_redis_key("order",[auction_id])
		str_item = objEventDB.redis_client.get(order_redis_key)
		final_item = dict()
		final_item.update(item)			
		dict_order_details[auction_id]=json.dumps(final_item)
		
		if status !='S':
			live_orders.append(auction_id)
			all_live_items.add(item_id)

	#objEventDB.redis_client.mset(dict_order_details)
	if 0 in orders:
		orders.remove(0)
	# set_last_order_id(new_last_order_id)
	# set_all_live_items((all_live_items))
	with objEventDB.redis_client.pipeline() as pipe:
		for auction_id,str_item in dict_order_details.iteritems():
			redis_key=objEventDB.get_redis_key("orders",[str(auction_id)])
			pipe.set(redis_key,str_item)
		pipe.execute()				
	key_live_orders=objEventDB.get_redis_key("live_orders")
	
	if not "live_auction" in all_auction_dict:
		all_auction_dict["live_auction"]=[]
	all_auction_dict["live_auction"].append((str(auction_id),user_id,status,item_id))

	if len(live_orders)>0:
		objEventDB.redis_client.sadd(key_live_orders,*live_orders)
	return all_auction_dict

def get_list_live_user_items(all_auction_dict):
	user_items_list = []
	user_item_dict = {}
	for item in all_auction_dict["live_auction"]:
		auction_id,user_id,status,item_id=item
		# users_item= str(user_id)+"|"+str(item_id)
		if str(item_id) not in user_item_dict:
			user_item_dict.update({str(item_id):[user_id]})
		else:
			user_item_dict[str(item_id)].append(user_id)
		# user_items_list.append(users_item)
	return user_item_dict

def main():
	while True:
		# try:
		all_user_ids = []
		last_order_id = get_last_order_id()
		if last_order_id:
			result = tran_db.get_order_detail(last_order_id)
		if result:
			all_auction_dict = process_new_orders(result)
			# all_user_ids = get_list_live_user_items(all_auction_dict)
			user_item_dict = get_list_live_user_items(all_auction_dict)
		auction_events.generate_new_orders_events(user_item_dict)
		# except Exception as e:
			# raise e
		time.sleep(10)

if __name__ == '__main__':
	main()