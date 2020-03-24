from flask import Blueprint, flash, redirect, render_template, jsonify, request, Response, abort, url_for
from flask import current_app as app
import flask_login
from sqlite3 import Error
from label.database import db

user_bp = Blueprint('user_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@user_bp.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    res = False

    try:
        username = req['username']
        password = req['password']
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        for row in rows:
            db_user = row[1]
            db_pass = row[3]
            if db_user == username and db_pass == password:
                db_role = row[2]
                res = True

        cur.close()

        if res:
            return jsonify({
                "role": db_role
            }), 200
        else:
            return jsonify({
                "status": "Username/Password Not Match"
            }), 404

    except Error as e:
        return jsonify({"error": e}), 500

@user_bp.route('/register', methods=['POST'])
def register():
    req = request.get_json()

    try:
        username = req['username']
        password = req['password']
        role = "labeler"
        cur = db.conn.cursor()
        cur.execute("INSERT INTO users (name, role, password) VALUES (?, ?, ?);", (username, role, password))
        # call commit on the connection...
        # print("Total", cur.rowcount, "Records inserted successfully into user table")
        db.conn.commit()
        cur.close()

        return Response(status=200)
        
    except Error as e:
        return jsonify({"error": e}), 500

@user_bp.route("/userrole", methods=['GET'])
def get_all_users():
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        cur.close()

    except Error as e:
        return jsonify({"error": "can't fetch user's data"}), 500
    
    return jsonify({
        "users": rows
    }), 200

#update user's role
@user_bp.route("/userrole", methods=['POST'])
def update_user():
    req = request.get_json()
    print(req['id'])
    print(req['role'])

    try:
        cur = db.conn.cursor()
        cur.execute("UPDATE users SET role='" + req['role'] + "' WHERE id_user='" + str(req['id']) + "'")
        db.conn.commit()
        cur.close()
    except Error as e:
        return jsonify({"error": "can't update user"}), 500
    
    return Response(status=200)
