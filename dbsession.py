# import sqlalchemy
# import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
# from sqlalchemy import event

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

SQLURINAME = "database.sqlite"
# engine = create_engine("mysql+pymysql://root:kihatap1l1@104.199.5.32/pymatrix-backend")
def make_session():
    engine = create_engine("sqlite:///{}".format(SQLURINAME), echo=False)

    # @event.listens_for(engine, "before_cursor_execute")
    # def before_cursor_execute(conn, cursor, statement,
    #                         parameters, context, executemany):
    #     conn.info.setdefault('query_start_time', []).append(time.time())
    #     logger.debug("Start Query: %s", statement)
    #
    # @event.listens_for(engine, "after_cursor_execute")
    # def after_cursor_execute(conn, cursor, statement,
    #                         parameters, context, executemany):
    #     total = time.time() - conn.info['query_start_time'].pop(-1)
    #     logger.debug("Query Complete!")
    #     logger.debug("Total Time: %f", total)


    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()
