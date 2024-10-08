from flask import Flask
from authenticationflask.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.app_context().push()
    with app.app_context():
        db.create_all()

    from authenticationflask.main.routes import main
    from authenticationflask.users.routes import users
    from authenticationflask.logs.routes import logs

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(logs)

    
    return app