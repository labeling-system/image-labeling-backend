import sqlite3
from sqlite3 import Error
 
 
def create_database(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Database opened succesfully")
        conn.execute('''CREATE TABLE USER
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT NOT NULL,
                        ROLE TEXT NOT NULL,
                        PASSWORD TEXT NOT NULL);''')
        print("Table created successfully")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def insert_data(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Database opened succesfully")
        conn.execute('''INSERT INTO USER (NAME, ROLE, PASSWORD) \
            VALUES ('admin', 'admin', 'admin');''')
        conn.execute('''INSERT INTO USER (NAME, ROLE, PASSWORD) \
            VALUES ('labeller', 'labeller', '123456');''')
        conn.execute('''INSERT INTO USER (NAME, ROLE, PASSWORD) \
            VALUES ('editor', 'editor', '123456');''')
        conn.commit()
        print("Table created successfully")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def select_data(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Database opened succesfully")
        cursor = conn.execute('''SELECT ID, NAME, ROLE, PASSWORD FROM USER''')
        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("ROLE = ", row[2])
            print("PASSWORD = ", row[3], "\n")
        print("Operation done successfully")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
 
if __name__ == '__main__':
    select_data(r"users.db")