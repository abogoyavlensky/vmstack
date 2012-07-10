import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import INTEGER, TEXT

Base = declarative_base()

class VM(Base):
    __tablename__ = 'VMs'

    id = sqlalchemy.Column(INTEGER, primary_key = True)
    name = sqlalchemy.Column(TEXT)
    started = sqlalchemy.Column(INTEGER)
    ip = sqlalchemy.Column(TEXT)

    def __init__(self, name, started, ip):
        self.name = name
        self.started = started
        self.ip = ip

    def __repr__(self):
        return '<VM(%s,%s,%s)>' % self.name, self.started, self.ip
    
class DBserver():
    def __init__(self):
        self.engine = sqlalchemy.create_engine('sqlite:///server.db', echo = True)
        self.Session = sqlalchemy.orm.sessionmaker(bind = self.engine)

    def add(self, name, started, ip):
        new_VM = VM(name, started, ip)
        self.session = self.Session()
        self.session.add(new_VM)
        self.session.flush(new_VM)
