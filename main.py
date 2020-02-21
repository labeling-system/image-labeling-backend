from flask import Flask, flash, redirect, render_template, request, abort, url_for
import flask_login
import os
from sqlite3 import Error
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'secretlogin' 
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    try:
        conn = sql.connect("users.db")
        result = False

        cur = conn.cursor()
        cur.execute("SELECT * FROM USER")
        rows = cur.fetchall()
        for row in rows:
            if username == row[1]:
                result = True

        cur.close()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    if result == False:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    password = request.form.get('password')

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
                result = True

        cur.close()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    if result == False:
        return
    else:
        user = User()
        user.id = username
        user.is_authenticated = True

    return user

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # error message
    msg = ''
    if request.method == 'GET':
        return render_template('login.html', msg=msg)

    else:
        username = request.form['username']
        password = request.form['password']
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
        if result == True:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return user_role(db_role)
        else:
            msg = 'Incorrect username/password!'
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

            flash("Successfully registered")
            
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)

@app.route('/home/<user>')
@flask_login.login_required
def user_role(user):
    if user == 'admin':
        return redirect(url_for('admin'))
    elif user == 'labeller':
        return redirect(url_for('labeller'))
    else:
        return redirect(url_for('editor'))

@app.route('/home/admin')
@flask_login.login_required
def admin():
    # msg = "You are in admin site"
    # return render_template('home.html', msg=msg)
    conn = sql.connect("users.db")
    # print("Database opened succesfully")
    cursor = conn.execute("SELECT * FROM USER")
    return render_template("list_user.html", rows = cursor)
    # print("Operation done successfully")
    conn.close()

@app.route('/home/admin/<int:id>',methods = ['POST', 'GET'])
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
    
    return redirect(url_for('admin'))

@app.route('/home/labeller')
@flask_login.login_required
def labeller():
    msg =  "You are in labeller site"
    return render_template('home.html', msg=msg)

@app.route('/home/editor')
@flask_login.login_required
def editor():
    msg =  "You are in editor site"
    return render_template('home.html', msg=msg)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return login()

if __name__ == '__main__':
    app.run(debug = True)