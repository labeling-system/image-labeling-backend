from flask import Blueprint, jsonify
from sqlite3 import Error
from label.database import db

image_bp = Blueprint('image_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

ID = 0
STATUS = 1
FILENAME = 2

# Fetch image from given id
@image_bp.route('/image/<id>', methods=['GET'])
def get_image(id):
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM images WHERE id_image=?", id)
        print(id)
        row = cur.fetchone()
        cur.close()

    except Error as e:
        return jsonify({"error": "can't fetch image"}), 500
    
    return jsonify({
        "filename": row[FILENAME],
        "status": row[STATUS]
    }), 200
