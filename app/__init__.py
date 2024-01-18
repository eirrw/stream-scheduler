import os
from flask import Flask, render_template
from config import Config
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ''

from app import models

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    if app.config['SQLALCHEMY_DATABASE_URI'] is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'streams.sqlite')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    register_blueprints(app)

    @app.route('/')
    def index():
        return render_template('index.html', title='Home')

    return app


def register_blueprints(app: Flask):
    from . import auth
    app.register_blueprint(auth.bp)

    from . import stream
    app.register_blueprint(stream.bp)
