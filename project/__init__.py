from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Inicializamos SQLAlchemy de tal forma que podemos usar en nuestros modelos
db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='dev'
    app.config['SQLALCHEMY_DATABASE_URI']="mariadb+mariadbconnector://root:123456@127.0.0.1:3306/auth_app_db"
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

     # blueprint para rutas auth routes en nuestro app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint para rutas no-auth routes en nuestro app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()
    return app
