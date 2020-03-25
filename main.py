from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
from label import create_app
from label.database import db
from sqlite3 import Error
from label.utils import const
import atexit
import config
import time

# must check new status based on selection
def update_inactive_editing():
    print("update")
    try:
        cur = db.conn.cursor()
        # check last update
        cur.execute("UPDATE images SET status=:new_status WHERE status=:old_status", {"new_status": const.UNLABELED, "old_status": const.EDITING})
        db.conn.commit()
        cur.close()

    except Error as e:
        print(e)

if __name__ == '__main__':
    app = create_app()   
    CORS(app) 
    db.create_connection(config.DATABASE_NAME)

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_inactive_editing, trigger="interval", seconds=60)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    
    app.run(debug = True)
    db.close_connection()
