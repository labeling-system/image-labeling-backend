from flask import Flask
from flask import Flask, flash, redirect, render_template, request, abort, url_for
import os
from sqlite3 import Error
import sqlite3 as sql

app = Flask(__name__)


@app.route('/home/<user>')
def user_role(user):
    if user == 'admin':
        return redirect(url_for('admin'))
    elif user == 'labeller':
        return redirect(url_for('labeller'))
    else:
        return redirect(url_for('editor'))

@app.route('/home/admin')
def admin():
    return "You are in admin site"

@app.route('/home/labeller')
def labeller():
    return "You are in labeller site"

@app.route('/home/editor')
def editor():
    return "You are in editor site"


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # error message
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Check user on database
        try:
            conn = sql.connect("users.db")
            result = False

            cur = conn.cursor()
            cur.execute("SELECT * FROM USER")
            rows = cur.fetchall()
            for row in rows:
                db_user = row[1]
                db_pass = row[3]
                if db_user == username and db_pass == password:
                    db_role = row[2]
                    result = True

            cur.close()

        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

        if result:
            # Redirect to home page
            return user_role(db_role)

        else:
            # jika akun tidak ada
            msg = 'Incorrect username/password!'
            
    # menampilkan error message jika ada
    return render_template('login.html', msg=msg)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    # error message
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        try:
            conn = sql.connect("users.db")

            cur = conn.cursor()
            cur.execute("INSERT INTO USER (NAME, ROLE, PASSWORD) VALUES (?, ?, ?);", (username, role, password))
            # call commit on the connection...
            print("Total", cur.rowcount, "Records inserted successfully into USER table")
            conn.commit()
            cur.close()
            
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)

if __name__ == '__main__':
   app.run(debug = True)