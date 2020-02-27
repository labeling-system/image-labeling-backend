from flask import Blueprint, flash, redirect, render_template, request, abort, url_for
from flask import current_app as app
import flask_login
from sqlite3 import Error
from label.database import db

user_bp = Blueprint('user_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    try:
        result = False

        cur = db.conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            if username == row[1]:
                result = True

        cur.close()

    except Error as e:
        print(e)

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
        result = False

        cur = db.conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            db_user = row[1]
            db_pass = row[3]
            if db_user == username and db_pass == password:
                result = True

        cur.close()

    except Error as e:
        print(e)

    user = User()
    if result == False:
        return
    else:
        user.id = username
        user.is_authenticated = True

    return user

@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    # error message
    msg = ''
    if request.method == 'GET':
        return render_template('login.html', msg=msg)

    else:
        username = request.form['username']
        password = request.form['password']
        try:
            result = False

            cur = db.conn.cursor()
            cur.execute("SELECT * FROM users")
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

        if result == True:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return user_role(db_role)
        else:
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)

@user_bp.route('/register/', methods=['GET', 'POST'])
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
            cur = db.conn.cursor()
            cur.execute("INSERT INTO users (name, role, password) VALUES (?, ?, ?);", (username, role, password))
            # call commit on the connection...
            print("Total", cur.rowcount, "Records inserted successfully into user table")
            db.conn.commit()
            cur.close()

            flash("Successfully registered")
            
        except Error as e:
            print(e)

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)

@user_bp.route('/home/<user>')
@flask_login.login_required
def user_role(user):
    if user == 'admin':
        return redirect(url_for('user_bp.admin'))
    elif user == 'labeller':
        return redirect(url_for('user_bp.labeller'))
    else:
        return redirect(url_for('user_bp.editor'))

@user_bp.route('/home/admin')
@flask_login.login_required
def admin():
    msg = "You are in admin site"
    return render_template('home.html', msg=msg)

@user_bp.route('/home/labeller')
@flask_login.login_required
def labeller():
    msg =  "You are in labeller site"
    return render_template('home.html', msg=msg)

@user_bp.route('/home/editor')
@flask_login.login_required
def editor():
    msg =  "You are in editor site"
    return render_template('home.html', msg=msg)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@user_bp.route("/logout")
def logout():
    flask_login.logout_user()
    return login()
