from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
from label import create_app
from label.database import db
from sqlite3 import Error
from label.utils import const
import atexit
import config
import time


ID = 0

# in minutes
INTERVAL = 1

# must check new status based on selection
def update_inactive_editing():
    print("update inactive")
    try:
        cur = db.conn.cursor()
        # Get all id image of expired image
        cur = db.conn.cursor()
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

if __name__ == '__main__':
    app = create_app()   
    CORS(app) 
    db.create_connection(config.DATABASE_NAME)

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_inactive_editing, trigger="interval", seconds=INTERVAL*60)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    
    app.run(debug = True, use_reloader=False, host= '0.0.0.0', port = 5000)
    db.close_connection()
