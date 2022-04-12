from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RBMModel(Base):
    __tablename__ = 'method'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Request: method={self.method}, count={self.count}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(273), nullable=False)
    count = Column(Integer, nullable=False)


class Top10Model(Base):
    __tablename__ = '10'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Request: endpoint={self.endpoint}, count={self.count}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    endpoint = Column(String(500), nullable=False)
    count = Column(Integer, nullable=False)


class Top54xxModel(Base):
    __tablename__ = '4xx'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Request: url={self.url}, status_code={self.status_code}, byte_size={self.headers_byte_size}, ip={self.ip}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(425), nullable=False)
    status_code = Column(Integer, nullable=False)
    headers_byte_size = Column(String(50), nullable=False)
    ip = Column(String(15), nullable=False)


class Top55xxModel(Base):
    __tablename__ = '5xx'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Request: ip={self.ip}, count={self.count}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    count = Column(Integer, nullable=False)
