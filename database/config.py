"""Configuration file """
from os import environ, path
import pyodbc


class Config(object):
    """Common configuration"""
    SESSION_PERMANENT = False
    SECRET_KEY= environ.get("FLASK_SECRET_KEY")
    EXPLAIN_TEMPLATE_LOADING = False


# class Development(Config):
    # """Development configuration"""
    # SESSION_TYPE = "filesystem"
    # BASEDIR = path.abspath(path.dirname(__file__))
    # print(BASEDIR)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASEDIR, environ.get("FLASK_SQLALCHEMY_DATABASE_NAME"))

class Production(Config):
    """Production configuration"""
    # Check Flor code if use redis or what method
    SESSION_TYPE = "filesystem"

    db_host = environ.get("MSSQLHOST")
    db_user = environ.get("MSSQLUSER")
    db_port = environ.get("MSSQLPORT")
    db_database = environ.get("MSSQLDATABASE")
    db_password = environ.get("MSSQLPASSWORD")

    # Remember change collation
    # SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_database}?sslmode=require"
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}?Driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection Timeout=30"
