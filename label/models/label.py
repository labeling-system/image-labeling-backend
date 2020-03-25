from flask import Blueprint, jsonify, request, Response
from sqlite3 import Error
from label.database import db
from label.utils import const

label_bp = Blueprint('label_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

#working image handling
@label_bp.route('/label', methods=['GET'])
def getMostUsedLabel():
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT name FROM label ORDER BY counter DESC LIMIT 10")
        rows = cur.fetchall()
        cur.close()

    except Error as e:
        print(e)
        return jsonify({"error": "can't fetch any label"}), 500
    
    return jsonify({
        "labelList": rows
    }), 200

    


