import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


env = "segmentation"
ENV = os.environ['env']

CONFIG_PATH = os.path.relpath(
    os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ), 'conf/dbs.ini')
)

if not os.path.exists(CONFIG_PATH):
    CONFIG_PATH = "/code/cong/dbs.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)


Base = declarative_base()


def get_session(db_name, env=ENV):
    db_config = config[db_name + '-' + env]
    user = db_config["user"].replace('"', '')
    pswd = db_config["pass"].replace('"', '')
    host = db_config["host"].replace('"', '')
    name = db_config["name"].replace('"', '')
    port = db_config.get("port", '').replace('"', '')

    if not port:
        port = 5432

    database_url = f"postgresql://{user}:{pswd}@{host}:{port}/{name}"

    engine = create_engine(database_url, pool_pre_ping=True, echo_pool=True, pool_size=100)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session
