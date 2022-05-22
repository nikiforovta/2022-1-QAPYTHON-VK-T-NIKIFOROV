import os
import shutil
import sys

from utils.db.client import MysqlClient


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir

    mysql_client = MysqlClient(user='root', password='1111', db_name='vkeducation')
    mysql_client.connect()
    config.mysql_client = mysql_client
