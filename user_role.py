from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3 as sql
from sqlite3 import Error
app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/')
def list():
    conn = sql.connect("users.db")
    # print("Database opened succesfully")
    cursor = conn.execute("SELECT * FROM USER")
    return render_template("list_user.html", rows = cursor)
    # print("Operation done successfully")
    conn.close()

@app.route('/<int:id>',methods = ['POST', 'GET'])
def save(id):
    # error message
    # msg = ''
    # check if "role" POST request is exist (admin submitted form to update role)
    if request.method == 'POST':
        role = request.form['role']
        roles = ['admin', 'labeller', 'editor']
        # check if role is admin/labeller/editor
        if (role in roles):
            try:
                conn = sql.connect("users.db")
                cur = conn.cursor()
                cur.execute("UPDATE USER SET ROLE=? WHERE ID=?;", (role, id))

                print("Total", cur.rowcount, "records updated")
                conn.commit()
                cur.close()

            except Error as e:
                print(e)
            finally:
                if conn:
                    conn.close()
        else:
            return("Invalid input. ROLE = [admin, editor, labeller]")
    
    return redirect(url_for('list'))

if __name__ == '__main__':
   app.run(debug = True)