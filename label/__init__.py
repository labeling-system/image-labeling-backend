import os
from flask import Flask
# from database import db
import config

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    with app.app_context():
        from .models import user
        app.register_blueprint(user.user_bp)

        from .models import image
        app.register_blueprint(image.image_bp)

        from .models import selection
        app.register_blueprint(selection.selection_bp)

        from .models import label
        app.register_blueprint(label.label_bp)
        
        return app