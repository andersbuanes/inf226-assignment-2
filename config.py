class Config:
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///content.db'
    DEBUG=True
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE="Strict"
    SESSION_COOKIE_SECUre=True
