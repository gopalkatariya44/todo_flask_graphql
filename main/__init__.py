from datetime import timedelta

from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from main.core.config import settings


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
# app.config.from_object(Config)

app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['UPLOAD_FOLDER'] = "main/static/user"
app.config['SQLALCHEMY_ECHO'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI + settings.DATABASE_NAME
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

db.init_app(app)

appConf = {
    "OAUTH2_CLIENT_ID": settings.KEYCLOAK_CLIENT_ID,
    "OAUTH2_CLIENT_SECRET": settings.KEYCLOAK_CLIENT_SECRET,
    "OAUTH2_ISSUER": "http://localhost:8080/realms/myrealm",
    "FLASK_SECRET": settings.SECRET_KEY,
    "FLASK_PORT": 5001
}

oauth = OAuth(app)

oauth.register(
    "myApp",
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret=settings.KEYCLOAK_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
        # 'code_challenge_method': 'S256'  # enable PKCE
    },
    server_metadata_url=f'{appConf.get("OAUTH2_ISSUER")}/.well-known/openid-configuration',
)
# Add GraphQL view
# app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
#     'graphql',
#     schema=schema,
#     graphiql=True  # Enable the GraphiQL interface
# ))

from main import features
