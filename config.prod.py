import os

# Config if application were to be released to production environment
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_PROD")
    DEBUG=False
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE="Strict"
    SESSION_COOKIE_SECUre=True
    