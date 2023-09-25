from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    DJANGO_SECRET_KEY: str = Field(validation_alias="DJANGO_SECRET_KEY")
    POSTGRESQL_USER: str = Field(validation_alias="POSTGRESQL_USER")
    POSTGRESQL_PASSWORD: str = Field(validation_alias="POSTGRESQL_PASSWORD")
    POSTGRESQL_PORT: int = Field(validation_alias="POSTGRESQL_PORT")
    POSTGRESQL_HOST: str = Field(validation_alias="POSTGRESQL_HOST")
    POSTGRESQL_DB_NAME: str = Field(validation_alias="POSTGRESQL_DB_NAME")


config_dict: dict = Config().model_dump()