import os
import re

import pytest

from client import MysqlClient


def pytest_configure(config):
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)

    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def parse_logs():
    pattern = re.compile(
        r"((\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})"
        r" - (\w*)- \[(\d{1,2}\/\w+\/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] "
        r"(\"(.+) (https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)?"
        r"([-a-zA-Z0-9()!@:%_\+,;.~#;?$|\*\[\]\{\}\'\\&\/=]*) HTTP\/1.[10]\") (\d{3}) ([\d\-]+)\s?"
        r"(\"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)?"
        r"([-a-zA-Z0-9()!@:%_\+,;.~#;?$|\*\[\]\{\}\'&\/=]*)\")?\s?((\".+\")\s?)+")
    res = []
    with open(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'access.log')) as logs:
        for log in logs:
            res.append(pattern.match(log))
    return res


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()
