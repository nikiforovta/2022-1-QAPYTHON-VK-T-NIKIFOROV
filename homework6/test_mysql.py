import pytest

from builder import MysqlBuilder
from client import MysqlClient
from models import RBMModel, Top10Model, Top54xxModel, Top55xxModel


class MyTest:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.mysql)

    def get_top_logs(self, top_type='method', **filters):
        self.mysql.session.commit()
        model = None
        if top_type == 'method':
            model = RBMModel
        elif top_type == '10':
            model = Top10Model
        elif top_type == '4xx':
            model = Top54xxModel
        elif top_type == '5xx':
            model = Top55xxModel
        res = self.mysql.session.query(model).filter_by(**filters)
        return res.all()


class TestMySql(MyTest):

    @pytest.mark.parametrize('top_type, expected_count', [
        ('method', 5),
        ('10', 10),
        ('4xx', 5),
        ('5xx', 5)])
    def test_logs(self, top_type, expected_count):
        self.mysql.create_table_log(top_type)
        self.builder.create_logs(top_type)
        count = self.get_top_logs(top_type=top_type)
        assert len(count) == expected_count
