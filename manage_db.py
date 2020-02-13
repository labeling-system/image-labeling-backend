import sqlite3
from sqlite3 import Error
 
 
def create_database(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Database opened succesfully")
        conn.execute('''CREATE TABLE USER
                        (ID INT PRIMARY KEY NOT NULL,
                        NAME TEXT NOT NULL,
                        ROLE TEXT NOT NULL);''')
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
        conn.execute('''INSERT INTO USER (ID, NAME, ROLE) \
            VALUES (1, 'Paul', 'admin');''')
        conn.execute('''INSERT INTO USER (ID, NAME, ROLE) \
            VALUES (2, 'Allen', 'labeller');''')
        conn.execute('''INSERT INTO USER (ID, NAME, ROLE) \
            VALUES (3, 'Teddy', 'editor');''')
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
        cursor = conn.execute('''SELECT ID, NAME, ROLE FROM USER''')
        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("ROLE = ", row[2], "\n")
        print("Operation done successfully")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
 
 
if __name__ == '__main__':
    # create_database(r"test.db")
    # insert_data(r"test.db")
    select_data(r"test.db")