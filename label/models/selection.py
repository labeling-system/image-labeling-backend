from flask import Blueprint, jsonify, request, Response
from sqlite3 import Error
from label.database import db
from label.utils import const
from xml.etree import ElementTree
from xml.dom.minidom import parseString

selection_bp = Blueprint('selection_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
is_initiated = False
a = 1
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

# Fetch all labeled image    
@selection_bp.route("/others", methods=['GET'])
def get_all_labeled():
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM images JOIN selections USING(id_image) WHERE images.status = 'labeled'")
        rows = cur.fetchall()
        cur.close()

    except Error as e:
        return jsonify({"error": "can't fetch user's data"}), 500
    
    return jsonify({
        "labeled": rows
    }), 200

def genXML(filename):
    images = {
        'image1' : {
            'name' : 'A',
            'xmin' : 10,
            'ymin' : 10,
            'size' : 20
        },
        'image2' : {
            'name' : 'B',
            'xmin' : 15,
            'ymin' : 15,
            'size' : 20
        }
    }

    for x, y in images.items():
        print(y['name'])

    tree = ElementTree.ElementTree() 
    node_root = ElementTree.Element('annotation')
    
    node_folder = ElementTree.Element('folder')
    node_folder.text = 'GTSDB'
    node_root.append(node_folder)
    
    node_filename = ElementTree.Element('filename')
    node_filename.text = '000001.jpg'
    node_root.append(node_filename)
    
    node_size = ElementTree.Element('size')
    node_width = ElementTree.Element('width')
    node_width.text = '500'
    node_size.append(node_width)
    
    node_height = ElementTree.Element('height')
    node_height.text = '375'
    node_size.append(node_height)
    
    node_depth = ElementTree.Element('depth')
    node_depth.text = '3'
    node_size.append(node_depth)

    node_root.append(node_size)

    for x, y in images.items() :
        node_object = ElementTree.Element('object')
        node_name = ElementTree.Element('name')
        node_name.text = y['name']
        node_object.append(node_name)
        
        node_difficult = ElementTree.Element('difficult')
        node_difficult.text = '0'
        node_object.append(node_difficult)

        node_bndbox = ElementTree.Element('bndbox')
        node_xmin = ElementTree.Element('xmin')
        node_xmin.text = str(y['xmin'])
        node_bndbox.append(node_xmin)
        node_ymin = ElementTree.Element('ymin')
        node_ymin.text = str(y['ymin'])
        node_bndbox.append(node_ymin)
        node_xmax = ElementTree.Element('xmax')
        node_xmax.text = str(y['xmin'] + y['size'])
        node_bndbox.append(node_xmax)
        node_ymax = ElementTree.Element('ymax')
        node_ymax.text = str(y['xmin'] + y['size'])
        node_bndbox.append(node_ymax)
        node_object.append(node_bndbox)
        node_root.append(node_object)

    tree._setroot(node_root)
    tree.write("../templates/" + filename + ".xml")