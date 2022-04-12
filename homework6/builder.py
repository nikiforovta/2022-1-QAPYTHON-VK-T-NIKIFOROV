import log_parse
from models import RBMModel, Top10Model, Top55xxModel, Top54xxModel


class MysqlBuilder:
    def __init__(self, client):
        self.client = client

    def create_logs(self, top_type='method'):
        logs = log_parse.log_parse(top_type)
        for log in logs:
            if top_type == 'method':
                self.client.session.add(RBMModel(method=log, count=logs[log]))
                self.client.session.commit()
            elif top_type == '10':
                self.client.session.add(Top10Model(endpoint=log[0], count=log[1]))
                self.client.session.commit()
            elif top_type == '4xx':
                self.client.session.add(Top54xxModel(url=log['url'], status_code=log['status_code'],
                                                     headers_byte_size=log['headers_byte_size'], ip=log['ip']))
                self.client.session.commit()
            elif top_type == '5xx':
                self.client.session.add(Top55xxModel(ip=log[0], count=log[1]))
                self.client.session.commit()
        return
