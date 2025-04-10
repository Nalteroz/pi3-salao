import os
from dotenv import load_dotenv

from flask import Flask, redirect
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api

from sqlalchemy import Connection
from sqlalchemy import DDL
from sqlalchemy import event
from sqlalchemy import Table

from resources.data import system_db
from resources.models import UserModel

import resources.blueprints as bp

@event.listens_for(Table, "before_create")
def create_schema_if_not_exists(target: Table, connection: Connection, **_):
    connection.execute(
        DDL("CREATE SCHEMA IF NOT EXISTS %(schema)s", {"schema": target.schema})
    )

def create_app():
    #Flask initialization
    app = Flask(__name__)
    load_dotenv()

    #API Configuration
    app.config['API_TITLE'] = 'PI III Sistema de Agendamento Studio Hema '
    app.config['API_VERSION'] = 'v1.0'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    #OpenAPI Configuration
    app.config['OPENAPI_VERSION'] = '3.1.1'
    app.config['OPENAPI_URL_PREFIX'] = '/docs'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config['OPENAPI_REDOC_PATH'] = '/redoc'
    app.config['OPENAPI_REDOC_URL'] = 'https://cdn.jsdelivr.net/npm/redoc/dist/redoc.min.js'

    #database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('BI_DATABASE_URI', 'sqlite:///bi.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #JWT configuration
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/user/refreshtoken'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    #Set static folder
    app.static_folder = 'resources/templates/static'

    #Database initialization
    system_db.init_app(app)
    migrate = Migrate(app, system_db)

    #Smorest initialization
    api = Api(app)

    #JWT initialization
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return UserModel.query.filter_by(id=identity).one_or_none()
    
    @jwt.unauthorized_loader
    def custom_unauthorized_response(_err):
        return redirect('/login')

    # Blueprint registration
    api.register_blueprint(bp.IndexBlueprint)
    api.register_blueprint(bp.UserBlueprint)

    return app
