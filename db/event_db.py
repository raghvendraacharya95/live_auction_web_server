import redis
REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_PASSWORD=""
REDIS_DB=0
DELIM=":"
NS="e"

_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)				
DEFAULT_DELIMETER=":"

class EventDB(object):
	"""docstring for EventDB"""
	def __init__(self,namespace=NS ,default_delimeter=DEFAULT_DELIMETER):
		super(EventDB, self).__init__()
		self._namespace=namespace
		self._default_delimeter=default_delimeter
		self.redis_client=_redis_client

	def get_redis_key(self,name,eVars=[]):
		return self._default_delimeter.join( (self._namespace, name) + tuple(eVars) )