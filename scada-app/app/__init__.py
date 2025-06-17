import logging

from sqlalchemy import URL, Engine, create_engine

from .db.models import Base
from .jobs.icmp import JobIcmp
from .jobs.mbus import JobMbus

logger = logging.getLogger(__name__)

__version__ = '0.0.1'


def init_db(use_sqlite: bool = False) -> Engine:
    if use_sqlite:
        # init engine (turn on echo for debug on need)
        engine = create_engine(f'sqlite:///:memory:', echo=False)
    else:
        # init engine (turn on echo for debug on need)
        url = URL.create(drivername='mysql+pymysql', username='sup_rst', password='p@ssword',
                         host='localhost', database='sup_rst',)
        engine = create_engine(url, echo=False)

    # create all tables in the database (if they don't exist)
    Base.metadata.create_all(engine)

    return engine


def init_logging(debug: bool = False) -> None:
    logging.basicConfig(format='%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s',
                        level=logging.DEBUG if debug else logging.INFO)


def run_icmp(debug: bool = False) -> None:
    # some initializations
    init_logging(debug=debug)
    engine = init_db(use_sqlite=False)

    # run job
    logger.info(f'start icmp job (version {__version__})')
    JobIcmp(engine).run()


def run_mbus(debug: bool = False) -> None:
    # some initializations
    init_logging(debug=debug)
    engine = init_db(use_sqlite=False)

    # run job
    logger.info(f'start mbus job (version {__version__})')
    JobMbus(engine).run()
