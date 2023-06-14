import os

class DevelopmentConfig():
    DEBUG = True
    SQLITE_DATABASE_FILE = os.path.join('database', 'test.db')




config = {
    'development': DevelopmentConfig
}
