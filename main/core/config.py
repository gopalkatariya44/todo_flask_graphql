from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str

    # Database
    SQLALCHEMY_DATABASE_URI: str
    DATABASE_NAME: str

    # KEYCLOAK
    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_SECRET: str

    # STRIPE
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLIC_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
