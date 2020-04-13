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
from datetime import date

selection_bp = Blueprint('selection_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
is_initiated = False
ID_IMAGE = 0
STATUS = 1
FILENAME = 2
WIDTH = 4
HEIGHT = 5

@selection_bp.route('/selection', methods=['GET', 'POST'])
def working_image():
    try:
        image_id, filename, width, height = get_working_image()
        if (image_id != const.ERROR and filename != const.ERROR):
            update_image_status(const.EDITING, image_id)  
            return jsonify({
                "image_id": image_id,
                "filename": filename,
                "width": width,
                "height": height
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
            if row[WIDTH] != None and row[HEIGHT] != None:
                width = row[WIDTH]
                height = row[HEIGHT]
                return (image_id, filename, width, height)
            else:
                return(const.ERROR, const.ERROR, const.ERROR, const.ERROR)
        else:
            return(const.ERROR, const.ERROR, const.ERROR, const.ERROR)

    except Error as e:
        print(e)
        return jsonify({"error": "can't get image from database"})
 

@selection_bp.route('/selection/<image_id>', methods=['GET'])
def get_selection_properties(image_id):
    try:
        cur = db.conn.cursor()
        print(image_id)
        cur.execute("SELECT x,y,length,width,label FROM selections WHERE id_image=:id", {"id": image_id})
        rows = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM selections WHERE id_image=:id", {"id": image_id})
        count = cur.fetchone()
        cur.close()

    except Error as e:
        print(e)
        return jsonify({"error": "can't get selection from database"}), 500
    
    if rows == None:
        return jsonify({"error": "id for image not found"}), 404

    return jsonify({
        "selections": rows,
        "count" : count
    }), 200


#akan diimplementasikan dan digabungkan dengan kode lukas
def get_raw_selection_properties(image_id, selection):
    height = selection['height']
    width = selection['width']
    x = float(selection['x']) 
    y = float(selection['y'])
    label = selection['label']
    print(height, width, x, y, label)
    return height, width, x, y, label

def get_label_counter(label):
    if (label != ""):
        return

@selection_bp.route('/selection/next/<image_id>', methods=['GET', 'POST'])

def save_image(image_id):
    req = request.get_json()
    print("size of selections:", len(req['selections']))
    for selection in req['selections']:
        print(selection)
        height, width, x, y, label = get_raw_selection_properties(image_id, selection)
        print(height, width, x, y, label)
        #height, width, x, y, label = get_raw_selection_properties(image_id, selection)
        #print(height, width, x, y, label)

        try:
            print("SYUHU")
            cur = db.conn.cursor()
            cur.execute("INSERT INTO selections (id_image, length, width, x, y, label) VALUES (?, ?, ?, ?, ?, ?);", (image_id, height, width, x, y, label))
            db.conn.commit()
            cur.close()
            print("SYUHU2")
            
        except Error as e:
            return jsonify({"error": "can't fetch image"})
            
    update_image_status(const.LABELED, image_id)

    image_id, filename, width, height = get_working_image()
    if (image_id != const.ERROR and filename != const.ERROR and width != const.ERROR and height != const.ERROR):
        update_image_status(const.EDITING, image_id)  
        return jsonify({
            "image_id": image_id,
            "filename": filename,
            "width": width,
            "height": height
        }), 200
    else:
        return jsonify({"error": "error occured. can't get image from database"}) 
    return jsonify({"error": "null"})
    # try:
    # except Error as e:
    #     return jsonify({"error": "can't fetch image"})



def update_image_status(status, id_image):
    try:
        cur = db.conn.cursor()
        cur.execute("UPDATE images SET status=? WHERE id_image=?;", (status, id_image))
        db.conn.commit()
        cur.close()
        return Response(status=200)
    except Error as e:
        return jsonify({"error": "can't fetch image"}), 500

# fetch all labeled image    
def get_all_labeled():
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT * FROM (select * from images JOIN selections USING(id_image) WHERE images.status = 'labeled' ORDER BY filename) as labeled JOIN label WHERE labeled.label == label.name")
        rows = cur.fetchall()
        cur.close()

    except Error as e:
        print(e)
    
    return rows

# function to get zip file of all json/xml generated file
def zipping(directory):
    with ZipFile(directory + '.zip', 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)

# functions to generate all xml file for all labeled images
def get_image_info_xml(data):
    node_root = ET.Element('annotation')
    node_folder = ET.Element('folder')
    node_folder.text = 'public/images'
    node_root.append(node_folder)
    node_filename = ET.Element('filename')
    node_filename.text = data[2]
    node_root.append(node_filename)
    node_size = ET.Element('size')
    node_width = ET.Element('width')
    node_width.text = str(float(data[4]))
    node_size.append(node_width)
    node_height = ET.Element('height')
    node_height.text = str(float(data[5]))
    node_size.append(node_height)
    node_root.append(node_size)

    return node_root

def get_objects_xml(filename, data):
    node_object = ET.Element('object')
    for d in data:
        if (d[2].split('.')[0] == filename):
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
            node_xmax.text = str(float(d[9]) + float(d[7]))
            node_bndbox.append(node_xmax)
            node_ymax = ET.Element('ymax')
            node_ymax.text = str(float(d[10]) + float(d[8]))
            node_bndbox.append(node_ymax)
            node_object.append(node_bndbox)
    
    return node_object

def generate_new_xml(filename, data, all_data):
    tree = ET.ElementTree()
    node_root = get_image_info_xml(data)
    node_object = get_objects_xml(filename, all_data)
    node_root.append(node_object)
    tree._setroot(node_root)

    xmlstr = minidom.parseString(ET.tostring(node_root)).toprettyxml(indent='   ')
    with open('./temp/xml/' + filename + '.xml', 'w') as f:
        f.write(xmlstr)

def generate_all_xml():
    try:
        data = get_all_labeled()
        curr_filename = data[0][2].split('.')[0]
        for d in data:
            filename = d[2].split('.')[0]
            if (d == data[0] or filename != curr_filename):
                curr_filename = filename
                generate_new_xml(filename, d, data)

    except Error as e:
        print(e)
        return jsonify({"error": "can't generate xml file"}), 500

@selection_bp.route("/downloadxml", methods=['GET'])
def downloadxml():
    try:
        print("downloadxml")
        generate_all_xml()
        zipping('./temp/xml')
        response = send_file('../temp/xml.zip', attachment_filename='label.zip', as_attachment=True)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": "can't send zip file"}), 500

# functions to generate all json file for all labeled images
def get_all_labelname():
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT id_label, name FROM  label")
        rows = cur.fetchall()
        cur.close()

    except Error as e:
        print(e)
    
    return rows

def get_info_json():
    today_date = date.today()
    info = {
        "year": 2020,
        "version": "1.0",
        "description": "Global image dataset",
        "contributor": "ppl-label-02-bounding_box",
        "url": "tbd",
        "date_created": str(today_date)
    }
    return info


def get_categories_json():
    labels = get_all_labelname()
    list_label = []
    for label in labels:
        id = label[0]
        name = label[1]
        tmp = {"id": id, "name": name}
        list_label.append(tmp)
    return list_label

def get_image_json(data):
    tmp = {
        "id": data[0],
        "width": data[4],
        "height": data[5],
        "filename": data[2]
    }
    return tmp

def get_annotations(filename, data):
    selections = []
    for d in data:
        if (d[2].split('.')[0] == filename):
            tmp = {
                "segmentation": [d[9], d[10], d[9] + float(d[7]), d[10] + float(d[8])],
                "area": float(d[7]) * float(d[8]),
                "image_id": d[0],
                "bbox": [d[9], d[10], float(d[7]), float(d[8])],
                "category_id": d[12],
                "id": d[6]
            }
            selections.append(tmp)
    return selections

def generate_new_json(filename, all_data, data):
    object_dict = {
        "info": get_info_json(),
        "categories": get_categories_json(),
        "image": get_image_json(data),
        "annotations": get_annotations(filename, all_data)
    }

    json_object = json.dumps(object_dict, indent=4, sort_keys=False)
    with open('./temp/json/' + filename + '.json', 'w') as outfile:
                outfile.write(json_object)

def generate_all_json():
    try:
        data = get_all_labeled()
        curr_filename = data[0][2].split('.')[0]
        for d in data:
            filename = d[2].split('.')[0]
            if (d == data[0] or filename!=curr_filename):
                curr_filename = filename
                generate_new_json(filename, data, d)            

    except Exception as e:
        print(e)

@selection_bp.route("/downloadjson", methods=['GET'])
def downloadjson():
    try:
        print("downloadjson")
        generate_all_json()
        zipping('./temp/json')
        response = send_file('../temp/json.zip', attachment_filename='label.zip', as_attachment=True)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": "can't send zip file"}), 500