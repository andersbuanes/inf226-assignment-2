SQLALCHEMY_DATABASE_URI = 'sqlite:///tiny.db'

SQLALCHEMY_BINDS = {
    'content': 'sqlite:///content.db',
    'auth': 'sqlite:///auth.db',
}
