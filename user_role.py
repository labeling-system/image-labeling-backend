from flask import Flask, request, render_template
from dropdown_role import dropdown
import sqlite3 as sql
app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/')
def list():
    form = dropdown()
    
    conn = sql.connect("test.db")
    # print("Database opened succesfully")
    cursor = conn.execute('''SELECT ID, NAME, ROLE FROM USER''')
    return render_template("list_user.html", rows = cursor, form = form)
    # print("Operation done successfully")

    conn.close()

if __name__ == '__main__':
   app.run(debug = True)