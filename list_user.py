from flask import Flask, redirect, url_for, request, render_template
import sqlite3 as sql
app = Flask(__name__)

@app.route('/list')
def list():
    conn = sql.connect("test.db")
    # print("Database opened succesfully")
    cursor = conn.execute('''SELECT ID, NAME, ROLE FROM USER''')
    return render_template("list.html", rows = cursor)
    # print("Operation done successfully")
    conn.close()

@app.route('/list/<user>')
def user_role(user):
    if user == 'admin':
        return redirect(url_for('user_bp.admin'))
    elif user == 'labeller':
        return redirect(url_for('user_bp.labeller'))
    else:
        return redirect(url_for('user_bp.editor'))

@app.route('/list/admin')
def admin():
    return "You are in admin site"

@app.route('/list/labeller')
def labeller():
    return "You are in labeller site"

@app.route('/list/editor')
def editor():
    return "You are in editor site"

if __name__ == '__main__':
   app.run(debug = True)