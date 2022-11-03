class Config(object):
    SECRET_KEY = "asdads"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///content.db'
    SQLALCHEMY_BINDS = {
        'auth': 'sqlite:///auth.db',
        'content': 'sqlite:///content.db',
    }