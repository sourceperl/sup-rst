from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .db.models import Base


def init_db() -> None:
    # init engine (turn on echo for debug on need)
    engine = create_engine(f'sqlite:////tmp/srst_test_mydatabase.db', echo=False)
    # init engine (turn on echo for debug on need)
    # engine = create_engine(url='mysql+pymysql://user:password@localhost:3306/mytestdb', echo=False)

    # create all tables in the database (if they don't exist)
    Base.metadata.create_all(engine)


def run() -> None:
    init_db()