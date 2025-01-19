import os
from dotenv import load_dotenv

# Load environment variables from .env.local file
load_dotenv('.env.local')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

    database_url = os.environ.get('SQLALCHEMY_DATABASE_URI')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = database_url
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:pEm8Y9yaYu1n1UDEV04K@autoapplier.cohuqar8xvwd.us-west-2.rds.amazonaws.com:5432/postgres"

class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI for production DB