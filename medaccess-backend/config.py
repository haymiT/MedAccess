import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:460K@r2000@localhost/medaccessdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'




# class Config:
#     SECRET_KEY = 'your_secret_key'
#     MYSQL_HOST = 'localhost'
#     MYSQL_USER = 'Esubalew'
#     MYSQL_PASSWORD = '350B@lew'
#     MYSQL_DB = 'medAccessDB'
#     MYSQL_CURSORCLASS = 'DictCursor'
