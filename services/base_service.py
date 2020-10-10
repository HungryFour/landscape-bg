from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from errors.error_handler import InvalidUsageException
import config
from tools.request_tools import RequestTools


class BaseService(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = None
        self.Session = None
        self.init_session()
        self.request_tools = RequestTools()

    def init_session(self):
        cf = config.get_db_config()
        connect_string = 'mysql+pymysql://%s:%s@%s:%s/%s' % (
            cf['user'], cf['password'], cf['host'], cf['port'],
            cf['db'])
        print("connect_string:", connect_string)
        self.engine = create_engine(connect_string)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
        except InvalidUsageException as error:
            session.rollback()
            raise error
        except Exception as error:
            session.rollback()
            raise error
        finally:
            session.close()

    def return_error(self, err_code, error_msg=None, status_code=400):
        self.request_tools.return_error(err_code, error_msg, status_code)
