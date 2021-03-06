from flask import Blueprint, jsonify, request, Response
from sqlite3 import Error
from label.database import db
from label.utils import const
import time

image_bp = Blueprint('image_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

ID = 0
STATUS = 1
FILENAME = 2
LAST_UPDATE = 3

REQ_FILENAME = 0
REQ_WIDTH = 1
REQ_HEIGHT = 2
REQ_URI = 3

COUNT_PAGE = 25

# in minutes
INTERVAL = 1

# Fetch all image
@image_bp.route('/image/all/<page>', methods=['GET'])
def get_all_image(page):
    offset = (int(page) - 1) * COUNT_PAGE
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM images LIMIT ? OFFSET ?", (COUNT_PAGE, offset))
        rows = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM images")
        count = cur.fetchone()
        cur.close()

    except Error as e:
        return jsonify({"error": "can't fetch image"}), 500
    
    return jsonify({
        "images": rows,
        "count": count
    }), 200

# Delete all image
@image_bp.route('/image/all', methods=['DELETE'])
def delete_all_image():
    try:
        cur = db.conn.cursor()
        cur.execute("DELETE FROM selections")
        cur.execute("DELETE FROM images")
        count = cur.rowcount
        cur.close()

    except Error as e:
        print(e)
        return jsonify({"error": "can't delete image"}), 500
    
    return jsonify({
        "count": count
    }), 200


@image_bp.route('/image/update/<id>', methods=['POST'])
def update_inactive_editing_by_id(id):
    print("wakgeng msk")
    try:
        cur = db.conn.cursor()

        cur.execute("UPDATE images SET status= CASE WHEN (SELECT COUNT(*) FROM selections WHERE id_image=:id_image) > 0 THEN :status_labaled ELSE :status_unlabaled END WHERE id_image=:id_image", {
            "status_labaled": const.LABELED, 
            "status_unlabaled": const.UNLABELED, 
            "id_image": id
        })
        
        db.conn.commit()
        cur.close()

    except Error as e:
        print(e)
        return jsonify({"error": "can't update status image by id"}), 500

    return Response(status=200)

# Ping image id
@image_bp.route('/image/ping/<id>', methods=['POST'])
def ping_image(id):
    try:
        cur = db.conn.cursor()
        cur.execute("UPDATE images SET last_update=:time WHERE id_image=:id", {"time": time.time(), "id": id})
        db.conn.commit()
        cur.close()

    except Error as e:
        print(e)
        return jsonify({"error": "can't update last_update in ping image"}), 500

    return jsonify({
        "id": id
    }), 200

# Fetch an image from given id
@image_bp.route('/image/<id>', methods=['GET'])
def get_image(id):
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM images WHERE id_image=:id", {"id": id})
        row = cur.fetchone()
        cur.close()

    except Error as e:
        print(e)
        return jsonify({"error": "can't fetch one image"}), 500
    
    if row == None:
        return jsonify({"error": "id for image not found"}), 404

    return jsonify({
        "filename": row[FILENAME],
        "status": row[STATUS],
        "last_update": row[LAST_UPDATE]
    }), 200

# Save image to database as unlabeled
@image_bp.route('/image', methods=['POST'])
def post_image():
    req = request.get_json()
    try:
        cur = db.conn.cursor()
        for file in req['files']:
            cur.execute("INSERT INTO images (status, filename, width, height, uri) VALUES (:status, :filename, :width, :height, :uri);", 
                {
                    "status": const.UNLABELED, 
                    "filename": file[REQ_FILENAME],
                    "width": file[REQ_WIDTH],
                    "height": file[REQ_HEIGHT],
                    "uri": file[REQ_URI]
                })
        db.conn.commit()
        cur.close()
    except Error as e:
        print(e)
        return jsonify({"error": "can't post image"}), 500

    return Response(status=200)
    

# For debugging, delete this when unused
@image_bp.route('/image/update', methods=['POST'])
def update_inactive_editing():
    try:
        cur = db.conn.cursor()
        timed = time.time() - INTERVAL * 60
        print(timed)

        # Get all id image of expired image
        cur.execute("SELECT id_image FROM images WHERE status=:old_status AND last_update <= :time", {
            "old_status": const.EDITING, 
            "time": time.time() - INTERVAL * 60
        })
        rows = cur.fetchall()

        for row in rows:
            cur.execute("UPDATE images SET status= CASE WHEN (SELECT COUNT(*) FROM selections WHERE id_image=:id_image) > 0 THEN :status_labaled ELSE :status_unlabaled END WHERE id_image=:id_image", {
                "status_labaled": const.LABELED, 
                "status_unlabaled": const.UNLABELED, 
                "id_image": row[ID]
            })
        
        db.conn.commit()
        cur.close()

    except Error as e:
        print(e)
        return jsonify({"error": "can't update status image"}), 500

    return Response(status=200)

