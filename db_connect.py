import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


config = configparser.ConfigParser()
config.read("config.ini")


db_name = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMAIN")
port = config.get("DB", "PORT")
user = config.get("DB", "USER")
password = config.get("DB", "PASSWORD")


url = f"postgresql://{user}:{password}@{domain}:{port}/{db_name}"


engine = create_engine(url, echo=False, pool_size=5, max_overflow=0)
engine.connect()
DBSession = sessionmaker(bind=engine)
session = DBSession()
