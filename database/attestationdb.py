import pymysql.cursors
from configparser import ConfigParser
import sys

class AttestationDB:

    def __init__(self):
        Config = ConfigParser()
        Config.read('db.ini')

        self.db = pymysql.connect(host='localhost',
                    user=Config.get('MYSQL', 'DBUSER'),
                    password=Config.get('MYSQL', 'DBPWD'),
                    db=Config.get('MYSQL', 'DBNAME'),
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
        
    def __del__(self):
        self.db.close()
    
    def query(self, sql_query, sql_args=None):
        cursor = self.db.cursor()

        if not cursor.connection:
            print('DB connection failed!')
            return None
        
        try:
            print(cursor.mogrify(sql_query, sql_args))
            cursor.execute(sql_query, sql_args)
            
            self.db.commit()
            return cursor
        except:
            print("Query ["+cursor._last_executed+"] failed:", sys.exc_info()[0])

        return None
    
    def closeDB():
        self.db.close()