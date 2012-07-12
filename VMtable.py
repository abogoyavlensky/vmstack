import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Boolean

Base = declarative_base()

class VM(Base):
    """This is "VM" table, which contain:
    
        virtual machine "id" [int] (is a primaty_key)
        virtual machine "name" [str] (shoud not be repeated)
        virtual machine status [bool] (started/stoped)
        cirtual machine "ip"[str]
    """
    __tablename__ = 'VMs'

    id = sqlalchemy.Column(Integer, primary_key = True)
    name = sqlalchemy.Column(String)
    started = sqlalchemy.Column(Boolean)
    ip = sqlalchemy.Column(String)

    def __init__(self, name, started, ip):
        """name [str] is virtual machine "name"
        started [bool] need for undertanding virtual machine started (started = False)
                                                          or stoped (started = False)
        ip [str] is ip address
        """
        self.name = name
        self.started = started
        self.ip = ip
        
    def __repr__(self):
        """need for creating a row
        """    
        return '<VM(%s,%s,%s)>' % (self.name, self.started, self.ip)

