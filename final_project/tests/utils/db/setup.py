from sqlalchemy.exc import IntegrityError

from builder import MysqlBuilder
from client import MysqlClient


def prepare():
    mysql_client = MysqlClient(user='root', password='1111', db_name='vkeducation')
    mysql_client.connect()
    mysql_client.create_table_users()
    try:
        MysqlBuilder(mysql_client).add_test_user()
    except IntegrityError:
        print("Test user already exists")
    mysql_client.connection.close()


if __name__ == '__main__':
    prepare()
