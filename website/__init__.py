from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "findmynanny"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '@Antony1237'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://fmn_dev:fmn_dev_pwd@localhost/' + DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models.family import Family
    from .models.nanny import Nanny
    from .models.booking import Booking

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        family = Family.query.get(str(id))
        if family:
            print(f"Loaded user as family (ID: {id}): {family}")
            return family
        else:
            nanny = Nanny.query.get(str(id))
            print(f"Loaded user as nanny (ID: {id}): {nanny}")
        return nanny

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
