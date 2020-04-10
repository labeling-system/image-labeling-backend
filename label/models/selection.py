from flask import Blueprint, jsonify, request, Response, make_response, send_file
from sqlite3 import Error
from label.database import db
from label.utils import const
from xml.etree import ElementTree as ET
from xml.dom import minidom
from zipfile import ZipFile
import os
import http.client
import xmltodict
import json

selection_bp = Blueprint('selection_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
is_initiated = False
ID_IMAGE = 0
STATUS = 1
FILENAME = 2

@selection_bp.route('/selection', methods=['GET', 'POST'])
def working_image():
    try:
        image_id, filename = get_working_image()
        if (image_id != const.ERROR and filename != const.ERROR):
            update_image_status(const.EDITING, image_id)  
            return jsonify({
                "image_id": image_id,
                "filename": filename
            }), 200
        else:
            return jsonify({"error": "error occured. can't get image from database"}) 
    except Error as e:
        print(e)
        return jsonify({"error": "can't get image from database"})


def get_working_image():
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM images WHERE status=?", [const.UNLABELED])
        row = cur.fetchone()
        cur.close()
        if (row != None):
            image_id = row[ID_IMAGE]
            filename = row[FILENAME]
            print("abc", image_id, filename)
            return (image_id, filename)
        else:
            return(const.ERROR, const.ERROR)

    except Error as e:
        print(e)
        return jsonify({"error": "can't get image from database"})
 

# Fetch an image from given id, buat rika
# akan menerima id, return nama file, status, last_update
@selection_bp.route('/selection/<id>', methods=['GET', 'POST'])
def get_working_image_from_id(id):
    try:
        cur = db.conn.cursor()
        print(id)
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


#akan diimplementasikan dan digabungkan dengan kode lukas
def get_selection_properties(image_id):
    length = "60px"
    width = "30px"
    x = 2 
    y = 4
    label = "human"
    return length, width, x, y, label



@selection_bp.route('/selection/next/<image_id>', methods=['GET', 'POST'])
def save_image(image_id):
    #req = request.get_json()
    #print(req)
    #image_id = req[0]
    #req = request.get_json()
    length, width, x, y, label = get_selection_properties(image_id)

    try:
        cur = db.conn.cursor()
        cur.execute("INSERT INTO selections (id_image, length, width, x, y, label) VALUES (?, ?, ?, ?, ?, ?);", (image_id, length, width, x, y, label))
        db.conn.commit()
        cur.close()
        
        update_image_status(const.LABELED, image_id)

        image_id, filename = get_working_image()
        if (image_id != const.ERROR and filename != const.ERROR):
            update_image_status(const.EDITING, image_id)  
            return jsonify({
                "image_id": image_id,
                "filename": filename
            }), 200
        else:
            return jsonify({"error": "error occured. can't get image from database"}) 
    except Error as e:
        return jsonify({"error": "can't fetch image"})



def update_image_status(status, id_image):
    try:
        cur = db.conn.cursor()
        cur.execute("UPDATE images SET status=? WHERE id_image=?;", (status, id_image))
        db.conn.commit()
        cur.close()
        return Response(status=200)
    except Error as e:
        return jsonify({"error": "can't fetch image"}), 500

# Fetch all labeled image    
def get_all_labeled():
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM images JOIN selections USING(id_image) WHERE images.status = 'labeled'")
        rows = cur.fetchall()
        cur.close()

    except Error as e:
        print(e)
    
    return rows

def zipping(directory):
    with ZipFile(directory + '.zip', 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)

def generateXML():
    try:
        data = get_all_labeled()
        # print(data)

        for d in data:
            print(d[2].split('.'))
            filename = d[2].split('.')[0]
            print(filename)
            tree = ET.ElementTree()
            node_root = ET.Element('annotation')
            node_folder = ET.Element('folder')
            node_folder.text = 'upload'
            node_root.append(node_folder)
            node_filename = ET.Element('filename')
            node_filename.text = d[2]
            node_root.append(node_filename)
            node_size = ET.Element('size')
            node_width = ET.Element('width')
            node_width.text = str(d[4])
            node_size.append(node_width)
            node_height = ET.Element('height')
            node_height.text = str(d[5])
            node_size.append(node_height)
            node_root.append(node_size)
            node_object = ET.Element('object')
            node_name = ET.Element('name')
            node_name.text = d[11]
            node_object.append(node_name)
            node_bndbox = ET.Element('bndbox')
            node_xmin = ET.Element('xmin')
            node_xmin.text = str(d[9])
            node_bndbox.append(node_xmin)
            node_ymin = ET.Element('ymin')
            node_ymin.text = str(d[10])
            node_bndbox.append(node_ymin)
            node_xmax = ET.Element('xmax')
            node_xmax.text = str(int(d[9]) + int(d[7]))
            node_bndbox.append(node_xmax)
            node_ymax = ET.Element('ymax')
            node_ymax.text = str(int(d[10]) + int(d[8]))
            node_bndbox.append(node_ymax)
            node_object.append(node_bndbox)
            node_root.append(node_object)
            tree._setroot(node_root)

            xmlstr = minidom.parseString(ET.tostring(node_root)).toprettyxml(indent='    ')
            with open('./temp/xml/' + filename + '.xml', 'w') as f:
                f.write(xmlstr)

    except Error as e:
        print(e)
        return jsonify({"error": "can't generate xml file"}), 500

@selection_bp.route("/downloadxml", methods=['GET'])
def downloadxml():
    try:
        print("downloadxml")
        generateXML()
        zipping('./temp/xml')
        return send_file('../temp/xml.zip', attachment_filename='label.zip', as_attachment=True)
    except Exception as e:
        print(e)
        return jsonify({"error": "can't send zip file"}), 500

def generateJSON():
    try:
        data = get_all_labeled()
        print(data)
        for d in data:
            filename = d[2].split('.')[0]
            print(filename)

            dictionary = {
                "halo" : d[0],
                "hola" : d[1],
                "ahoy" : d[2]
            }

            print(dictionary)

            json_object = json.dumps(dictionary, indent= 4)
            with open('./temp/json/' + filename + '.json', 'w') as outfile:
                outfile.write(json_object)

    except Exception as e:
        print(e)

@selection_bp.route("/downloadjson", methods=['GET'])
def downloadjson():
    try:
        print("here")
        generateJSON()
        print("generate json file")
        zipping('./temp/json')
        print("zipping json file")
        return send_file('../temp/json.zip', attachment_filename='label.zip', as_attachment=True)
        print("send json file")
    except Exception as e:
        print(e)
        return jsonify({"error": "can't send zip file"}), 500