import os


class Config:
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = os.getenv("TEST_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI")
