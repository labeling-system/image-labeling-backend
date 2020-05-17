from sqlite3 import Error
import sqlite3 as sql

class Database:
    # ATTRIBUTES
    # 
    # conn, an sql connection

    def __init__(self):
        pass
    
    def create_connection(self, db_name):
        self.conn = sql.connect(db_name, check_same_thread=False)
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
            
db = Database()
