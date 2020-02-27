from label import create_app
from label.database import db
import config

if __name__ == '__main__':
    app = create_app()    
    db.create_connection(config.DATABASE_NAME)
    app.run(debug = True)
    db.close_connection()
