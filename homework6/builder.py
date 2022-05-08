import log_parse
from models import TopMethodModel, TopFrequentModel, Top5xxModel, Top4xxModel


class MysqlBuilder:
    def __init__(self, client):
        self.client = client

    def create_logs(self, logs, top_type='method', quantity=10):
        logs = log_parse.get_top(logs, top_type, quantity)
        for log in logs:
            if top_type == 'method':
                self.client.session.add(TopMethodModel(method=log, count=logs[log]))
                self.client.session.commit()
            elif top_type == 'frequency':
                self.client.session.add(TopFrequentModel(endpoint=log[0], count=log[1]))
                self.client.session.commit()
            elif top_type == '4xx':
                self.client.session.add(Top4xxModel(url=log['url'], status_code=log['status_code'],
                                                    headers_byte_size=log['headers_byte_size'], ip=log['ip']))
                self.client.session.commit()
            elif top_type == '5xx':
                self.client.session.add(Top5xxModel(ip=log[0], count=log[1]))
                self.client.session.commit()
        return
