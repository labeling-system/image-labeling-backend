from flask import Blueprint, jsonify, request, Response
from sqlite3 import Error
from label.database import db
from label.utils import const

image_bp = Blueprint('image_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

ID = 0
STATUS = 1
FILENAME = 2
COUNT_PAGE = 25

# Fetch an image from given id
@image_bp.route('/image/<id>', methods=['GET'])
def get_image(id):
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM images WHERE id_image=?", id)
        row = cur.fetchone()
        cur.close()

    except Error as e:
        return jsonify({"error": "can't fetch image"}), 500
    
    return jsonify({
        "filename": row[FILENAME],
        "status": row[STATUS]
    }), 200

# Save image to database as unlabeled
@image_bp.route('/image', methods=['POST'])
def post_image():
    req = request.get_json()
    
    try:
        cur = db.conn.cursor()
        for filename in req['filenames']:
            cur.execute("INSERT INTO images (status, filename) VALUES (?, ?);", (const.UNLABELED, filename))
        db.conn.commit()
        cur.close()
    except Error as e:
        return jsonify({"error": "can't fetch image"}), 500

    return Response(status=200)

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
