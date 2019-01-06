import sys
sys.path.insert(0, '/home/acharya/Desktop/work/cars24_hackthon2/live_auction_web_server')
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect,Namespace,test_client

from flask_cors import CORS, cross_origin
# from live_auction_web_server import db
# from db.event_db import event_redis_db
from db import event_db
# import redis_db as event_db

import redis
import eventlet
import datetime
import time
import json

KEY_RT_UPDATE_ROOMS="rt-updates.rooms"
## Used to refresh emmitter
flag_refresh=False
room_no = None
## Monkey patch enables multithreading in eventlet server. 
eventlet.monkey_patch()

def run_emmitter():
    """
        Continously listen for events on mentioned channels(KEY_RT_UPDATE_ROOMS).
        To add new room, add room to KEY_RT_UPDATE_ROOMS set then refresh (set flag_refresh=True)
    """
    rooms=list(app.redis_client.sscan_iter(KEY_RT_UPDATE_ROOMS))
    print rooms
    sub_object = app.redis_client.pubsub()
    sub_object.subscribe(*rooms)            
    global flag_refresh
    for item in sub_object.listen():   
        channel=item["channel"]
        event_type= item['type']
        data=item["data"]
        
        socketio.send(json.dumps(item),room=channel,namespace="/sink_auction")        
        if flag_refresh==True:
            flag_refresh=False
            sub_object.unsubscribe()
            del sub_object
            break

def get_rooms():
    """
        Return subscribed rooms in current namespace
    """
    rooms=list(app.redis_client.sscan_iter(KEY_RT_UPDATE_ROOMS))
    if rooms:
        return rooms
    else:
        return []

def auth_for_rt_events(token):
    import hashlib
    import base64
    try:
        global MY_SECRET
        username,cipher = token.split("|")
        str_text="|".join(username,MY_SECRET)
        actual_cipher=base64.urlsafe_b64encode(username,hashlib.md5(str_text).digest())
        return actual_cipher==cipher
    except Exception, e:
        return False    

def get_clients(room=None):
    """
        Return connected clients in current namepsace and mentioned room.
        If room is None, it returns all clients in current namespace.
    """
    ns=request.namespace
    connected_clients=list(socketio.server.manager.get_participants(ns,room))
    return connected_clients

class Sink_Exchange(Namespace):
    def on_connect(self):
        pass
        #TODO
        

    def on_disconnect(self):
        pass
        #TODO

    def on_auth(self,token):
        pass
        return auth_for_rt_events(token)

    def on_join(self,join_request):
        """
            Join requested room.
            It checks authorization based on token provided during auth
            Only registered rooms are allowed to be connected. 
        """    
        room_no=join_request["room"]
        print room_no,"room_no!!!!!"
        print "join",join_request
        if app.redis_client.sismember(KEY_RT_UPDATE_ROOMS,room_no):
            join_room(str(room_no))
            return  True
        else:
            print "No such room!!! going to register."
            #create one
            add_room(room_no)
            print "Rester!! Succssfully!!!"
            return True

    def on_leave(self,join_request):
        room_no=join_request["room"]        
        leave_room(room_no)
        return True

    def on_msg(self,msg_request):
        """
            Broadcast msg to all clients in room
        """
        print "on message"
        room_no=msg_request["room_no"]
        ns=request.namespace        
        socketio.send(msg,room=room_no,namespace=ns)        

    def on_list_rooms(self):
        return get_rooms()
        
    def on_list_clients(self,room=None):
        return get_clients(room)
        
    def on_refresh_rooms(self):
        global flag_refresh
        flag_refresh=True

def add_room(room):
    app.redis_client.sadd(KEY_RT_UPDATE_ROOMS,room)
    flag_refresh = True

def init_emitter():        
    """
        Init redis instance
        Register default rooms
    """    
    # app.redis_client.sadd(KEY_RT_UPDATE_ROOMS,"ROOM-AUCTION")
    while True:
        time.sleep(1)
        run_emmitter()

async_mode = 'eventlet'
app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/*": {"origins": ["localhost:8000"]}})

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode) #message_queue="redis://:qazwsxEDC!@#321@127.0.0.1:6379/0" ## Not required

socketio.on_namespace(Sink_Exchange('/sink_auction'))


def main():    
    objEventDB=event_db.EventDB()
    #redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)                
    app.redis_client=objEventDB.redis_client
    socketio.start_background_task(init_emitter)    
    socketio.run(app,debug=True, host='0.0.0.0',port=8082)

if __name__ == '__main__':
    main()
