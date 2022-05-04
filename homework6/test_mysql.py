import pytest

from builder import MysqlBuilder
from client import MysqlClient
from models import TopMethodModel, TopFrequentModel, Top4xxModel, Top5xxModel


class MyTest:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.mysql)

    def get_top_logs(self, top_type='method', **filters):
        self.mysql.session.commit()
        model = None
        if top_type == 'method':
            model = TopMethodModel
        elif top_type == 'frequency':
            model = TopFrequentModel
        elif top_type == '4xx':
            model = Top4xxModel
        elif top_type == '5xx':
            model = Top5xxModel
        res = self.mysql.session.query(model).filter_by(**filters)
        return res.all()


class TestMySql(MyTest):

    @pytest.mark.parametrize('top_type, expected_count', [
        ('method', 4),
        ('frequency', 15),
        ('4xx', 10),
        ('5xx', 5)])
    def test_logs(self, top_type, expected_count, parse_logs):
        self.mysql.create_table_log(top_type)
        self.builder.create_logs(parse_logs, top_type, quantity=expected_count)
        count = self.get_top_logs(top_type=top_type)
        assert len(count) == expected_count

    @pytest.mark.parametrize('top_type', ['method', 'frequency', '4xx', '5xx'])
    def test_order(self, top_type, parse_logs):
        self.mysql.create_table_log(top_type)
        self.builder.create_logs(parse_logs, top_type)
        top_logs = self.get_top_logs(top_type=top_type)
        if top_type != '4xx':
            for i in range(2, len(top_logs)):
                assert top_logs[i - 1].count >= top_logs[i].count
        else:
            for i in range(2, len(top_logs)):
                assert top_logs[i - 1].headers_byte_size >= top_logs[i].headers_byte_size
