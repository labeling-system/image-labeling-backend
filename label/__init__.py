import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config/config.cfg')
    app.secret_key = app.config['SECRET_KEY']

    with app.app_context():
        from .models import user
        
        app.register_blueprint(user.user_bp)

        return app