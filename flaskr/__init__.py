import os
from flask import Flask
from flask_login import LoginManager
import DB
from models import User
from flask_socketio import SocketIO, emit
import globals as globals


def create_app(test_config=None):
    globals.init()
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'secret!'
    login = LoginManager()
    login.init_app(app)
    globals.socketsio = SocketIO(app)
    # login.login_view = 'login'

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

        # a simple page that says hello

        # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    @login.user_loader
    def load_user(username):
        # u = flaskr.db.user_collection.find_one({"Name": username})
        u = DB.check_for_user(username)
        if not u:
            return None
        return User(username=u['username'])

    return app