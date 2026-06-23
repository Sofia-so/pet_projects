import os


class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
