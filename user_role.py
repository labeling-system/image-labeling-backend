from flask import Flask, request, render_template, redirect, url_for
import sqlite3 as sql
from sqlite3 import Error
app = Flask(__name__)
app.secret_key = 'development key'

def update_data(db_file, id, role):
    conn = None
    try:
        conn = sql.connect(db_file)
      #   print("Database opened succesfully")
        cursor = conn.execute("UPDATE USER SET ROLE='" + role + "' WHERE ID='" + str(id) + "'")
        return("update sukses")
    except Error as e:
        return(e)
    finally:
        if conn:
            conn.close()

@app.route('/')
def list():
    conn = sql.connect("test.db")
    # print("Database opened succesfully")
    cursor = conn.execute("SELECT ID, NAME, ROLE FROM USER")
    return render_template("list_user.html", rows = cursor)
    # print("Operation done successfully")
    conn.close()

@app.route('/<int:id>',methods = ['POST', 'GET'])
def save(id):
   if request.method == 'POST':
      role = request.form['role']
      roles = ['admin', 'labeller', 'editor']
      if (role in roles):
         # conn = sql.connect("test.db")
         # cursor = conn.execute("UPDATE USER SET ROLE = '" + role + "' WHERE ID = '" + str(id) + "'")
         # conn.close()
         update_data(r"test.db", id, role)
         return redirect(url_for('list'))
      else :
         return ("Invalid input role. Role = [admin, labeller, editor]")
      # return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)