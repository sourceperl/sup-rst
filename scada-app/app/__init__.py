from sqlalchemy import URL, create_engine, Engine
from sqlalchemy.orm import sessionmaker

from .db.models import Base
from .jobs.icmp import JobICMP


def init_db() -> Engine:
    # init engine (turn on echo for debug on need)
    # engine = create_engine(f'sqlite:////tmp/srst_test_mydatabase.db', echo=False)
    # init engine (turn on echo for debug on need)
    url = URL.create(drivername='mysql+pymysql', username='sup_rst', password='p@ssword', 
                     host='localhost', database='sup_rst',)
    engine = create_engine(url, echo=False)

    # create all tables in the database (if they don't exist)
    Base.metadata.create_all(engine)

    return engine


def run() -> None:
    engine = init_db()
    # run icmp job
    job_icmp = JobICMP(engine)
    job_icmp.run()
