from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    DJANGO_SECRET_KEY: str = Field(validation_alias="DJANGO_SECRET_KEY")
    POSTGRESQL_USER: str = Field(validation_alias="POSTGRES_USER")
    POSTGRESQL_PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    POSTGRESQL_PORT: int = Field(validation_alias="POSTGRES_PORT")
    POSTGRESQL_HOST: str = Field(validation_alias="POSTGRES_HOST")
    POSTGRESQL_DB_NAME: str = Field(validation_alias="POSTGRES_DB")
    ALLOWED_HOSTS: str = Field(validation_alias="ALLOWED_HOSTS")
    ACCESS_TOKEN_TTL: int = Field(validation_alias="ACCESS_TOKEN_TTL")
    REFRESH_TOKEN_TTL: int = Field(validation_alias="REFRESH_TOKEN_TTL")


config_dict: dict = Config().model_dump()