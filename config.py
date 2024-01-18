import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-key-is-not-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or None
