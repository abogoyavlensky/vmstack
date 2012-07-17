import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Boolean

base = declarative_base()

class VM(base):
    """This is "VM" table, which contain:
    
        virtual machine "id" [int] (is a primaty_key)
        virtual machine "name" [str] (shoud not be repeated)
        virtual machine "active" [bool] (started/stoped)
        cirtual machine "ip"[str]
    """
    __tablename__ = 'VMs'

    id = sqlalchemy.Column(Integer, primary_key = True)
    name = sqlalchemy.Column(String)
    started = sqlalchemy.Column(Boolean)
    ip = sqlalchemy.Column(String)

    def __init__(self, name, (active, ip)):
        """name [str] is virtual machine "name"
        active [bool] need for undertanding virtual machine started (active = True)
                                                          or stoped (active = False)
        ip [str] is ip address
        """
        self.name = name
        self.active = active
        self.ip = ip
        
    def __repr__(self):
        """need for creating a row
        """    
        return '<VM(%s,%s,%s)>' % (self.name, self.started, self.ip)

