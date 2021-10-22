from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask import Flask

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b24f82f8ec842ee5e4d0742ddf0101241c154d0a2c4d308ec43010649b10f196'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:arcmedic@localhost:5432/celerdev"
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=15)

    db.init_app(app)
    
    # Modifica as views que estão elegiveis ao login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_usuario'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_porteiro(id):
        return Usuario.query.get(id)

    from .auth import auth
    from .views import views
    from .changes import changes

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(changes, url_prefix='/')

    from .models import Usuario

    return app