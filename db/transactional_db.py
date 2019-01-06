##Author R@ghvendra

from sqlalchemy import create_engine
engines={}
import pymysql
import os
import ConfigParser

CONFIG_FILE = "sql.ini"
DEFAULT_DB_POOL_SIZE = 2

def get_mysql_db_engine(server_name,refresh=False):
	config = ConfigParser.ConfigParser()
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)),CONFIG_FILE)
	config.read(path)
	section_name = server_name
	if section_name not in config.sections():
		raise Exception("No section % " % server_name)
	server = config.get(section_name,"host")
	db_name = config.get(section_name,"db_name")
	user = config.get(section_name,"user")
	password = config.get(section_name,"password")
	engine_key = server+db_name+user+password	
	if not engine_key in engines or refresh==True:
		db_url="mysql+pymysql://"+user+":"+password+"@"+server+"/"+db_name+"?charset=utf8"
		print "creating engine "+str(db_url)
		engines[engine_key]=create_engine(db_url,pool_size=DEFAULT_DB_POOL_SIZE,max_overflow=0)
	return engines[engine_key]


class DB(object):
	def __init__(self,server_name):
		self.engine = get_mysql_db_engine(server_name)
		self.server_name = server_name
		
	def execute_query(self,str_query,params=None,commit=False,return_result=True,execute_query=False,return_id=False):
		result=None		
		conn=self.engine.raw_connection()
		try:
			if execute_query:
				# print str_query,params
				with conn.cursor(pymysql.cursors.DictCursor) as cursor:
					cursor.execute(str_query,params)					
			else:
				with conn.cursor() as cursor:
					cursor.callproc(str_query,params)
			if return_result:
				result=cursor.fetchall()
				# print cursor,
				# print cursor.fetchall()
				# print result,"result"
				conn.commit()
				conn.close()
				return result
			if return_id:
				result = cursor.lastrowid
			if commit==True:
				conn.commit()
		finally:
			conn.close()
		return result

if __name__=="__main__":
	server_name = "localhost"
	db=DB(server_name)
	q = """
		INSERT INTO users(user_name,email_id,mobile)
		VALUES('Raghvendra','test@gmail.com','9999999999');
	"""
	print db.execute_query(q,execute_query=True,commit=True)