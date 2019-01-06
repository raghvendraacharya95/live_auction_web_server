ROOM_NAME="ROOM-AUCTION"

from db import event_db

def get_room_name(item_id):
	return "=".join([ROOM_NAME+"-ITEM",item_id])

def generate_change_bid_price_events(item_id,user_id,current_price):
	objEventDB=event_db.EventDB()
	event="|".join(["price_change"]+[user_id,item_id,current_price])
	room_name = get_room_name(item_id)
	print room_name,"room_name to publish"
	objEventDB.redis_client.publish(room_name,event)	
	print event
	print "published!!!!!"


def pubish_new_orders_item_wise(item_id,users):
	objEventDB=event_db.EventDB()
	room_name = get_room_name(item_id)
	print room_name,"room_name to publish"
	for user_id in users:
		user_item = str(user_id)+"|"+str(item_id)
		event="|".join(("new_bid_init",str(user_item)))
		objEventDB.redis_client.publish(room_name,event)	
		print event,"event"
		

def generate_new_orders_events(user_items_dict):
	objEventDB=event_db.EventDB()
	for item_id,users in user_items_dict.iteritems():
		pubish_new_orders_item_wise(item_id,users)		
		print "published!!!!"

def generate_buyer_found_event(item_id,user_id,price,user_name):
	objEventDB=event_db.EventDB()
	event="|".join(["buyer_found"]+[str(user_id),str(item_id),price,user_name])
	room_name = get_room_name(str(item_id))
	print room_name,"room_name to publish"
	objEventDB.redis_client.publish(room_name,event)	
	print event
	print "published!!!!!"
	##Close this room
	##ToDo

def generate_item_current_max_price_events(item_id,user_id,price,user_name):
	objEventDB=event_db.EventDB()
	event="|".join(["current_best_price"]+[str(user_id),str(item_id),price,user_name])
	room_name = get_room_name(str(item_id))
	print room_name,"room_name to publish"
	objEventDB.redis_client.publish(room_name,event)	
	print event
	print "published!!!!!"