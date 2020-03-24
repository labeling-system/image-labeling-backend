from flask import Blueprint, jsonify, request, Response
from sqlite3 import Error
from label.database import db
from label.utils import const

selection_bp = Blueprint('selection_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
is_initiated = False
#working image handling
@selection_bp.route('/selection/working', methods=['GET', 'POST'])
def working_image(is_initiated, image_id=1):
    if is_initiated:
        pass
    else:
        try:
            image_id, filename = get_working_image()
            is_initiated = True
        except Error as e:
            return jsonify({"error": "can't get image from database"}), 500

    update_image_status(const.EDITING, image_id)
    
    return jsonify({
        "image_id": image_id,
        "filename": filename
    }), 200

def get_working_image():
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM images WHERE status=?", const.UNLABELED)
        row = cur.fetchone()
        cur.close()
        image_id = row[ID_IMAGE]
        filename = row[FILENAME]
        return (image_id, filename), 200

    except Error as e:
        return jsonify({"error": "can't get image from database"}), 500

#akan diimplementasikan dan digabungkan dengan kode lukas
def get_selection_properties(image_id):
    length = "60px"
    width = "30px"
    x = 2 
    y = 4
    label = "human"
    return length, width, x, y, label



@selection_bp.route('/selection/next', methods=['GET', 'POST'])
def save_image(image_id):
    length, width, x, y, label = get_selection_properties(image_id)

    try:
        cur = db.conn.cursor()
        cur.execute("INSERT INTO selections (id_image, length, width, x, y, label) VALUES (?, ?, ?, ?, ?, ?);", (id_image, length, width, x, y, label))
        db.conn.commit()
        cur.close()
    except Error as e:
        return jsonify({"error": "can't fetch image"}), 500

    update_image_status(const.LABELED, image_id)

    image_id, filename = get_working_image()

    update_image_status(const.EDITING, image_id)

    return jsonify({
        "image_id": image_id,
        "filename": filename
    }), 200


def update_image_status(status, id_image):
    try:
        cur = db.conn.cursor()
        cur.execute("UPDATE images SET status=? WHERE id_image=?;", (status, image_id))
        db.conn.commit()
        cur.close()
        return Response(status=200)
    except Error as e:
        return jsonify({"error": "can't fetch image"}), 500
    


