from authlib.integrations.flask_client import OAuth

from app import app
from main.core.config import settings

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
