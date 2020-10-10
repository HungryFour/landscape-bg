import json
import os
import pymysql

from sqlalchemy import create_engine


class ConfigManager(object):
    def __init__(self, *args, **kwargs):
        super(ConfigManager, self).__init__(*args, **kwargs)

    def load_db_config(self, config):
        self.config = config

    def connect_db(self):
        self.connection = pymysql.connect(host=self.config["host"],
                                          user=self.config["user"],
                                          password=self.config["password"],
                                          db=self.config["db"],
                                          charset='utf8mb4',
                                          port="1433",
                                          cursorclass=pymysql.cursors.DictCursor)

    def get_engine(self) -> object:
        self.engine = create_engine(self.get_connect_string())

    def get_connect_string(self):
        connection_string = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' % (
            self.config['user'], self.config['password'], self.config['host'], self.config['port'],
            self.config['db'])
        return connection_string


def get_config_content(name):
    with open(get_config_path(), 'r') as f:
        try:
            content = json.load(f)[name]
            return content
        except Exception as err:
            print(str(err))
            return None


def get_config_path():
    path = str(os.path.abspath(os.path.dirname(os.path.realpath(__file__)))) + "/config.json"
    return path


def get_db_config():
    with open(get_config_path(), 'r') as f:

        if get_config_content("env") == "pro":
            conf = json.load(f)["mysql"]["mysql_pd"]
        else:
            conf = json.load(f)["mysql"]["mysql_dev"]
    return conf


def get_redis_config():
    with open(get_config_path(), 'r') as f:

        if get_config_content("env") == "pro":
            conf = json.load(f)["redis"]["redis_pd"]
        else:
            conf = json.load(f)["redis"]["redis_dev"]
    return conf


def get_bases_conf():
    with open(get_config_path(), 'r') as f:
        conf = json.load(f)['bases']
    return conf
