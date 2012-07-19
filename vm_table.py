import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Boolean

base = declarative_base()

class VM(base):
    """This is "VM" table, which contain:
    
        virtual machine "id" [int] (is a primaty_key)
        virtual machine "name" [str] (shoud not be repeated)
        virtual machine "active" [bool] (started/stoped)
        virtual machine "ip" [str]
        virtual machine "owner"[str]
        virtual machine uuid [str]
   """
    __tablename__ = 'VMs'

    id = sqlalchemy.Column(Integer, primary_key = True)
    name = sqlalchemy.Column(String)
    active = sqlalchemy.Column(Boolean)
    ip = sqlalchemy.Column(String)
    owner = sqlalchemy.Column(String)
    uuid_note = sqlalchemy.Column(String)

    def __init__(self, name, (active, ip, owner, uuid_note)):
        """name [str] is virtual machine "name"
        active [bool] need for undertanding virtual machine started (active = True)
                                                          or stoped (active = False)
        ip [str] is ip address
        owner [str] is owner name
        uuid [str] is virtual machine "uuid"
        """
        self.name = name
        self.active = active
        self.ip = ip
        self.owner = owner
        self.uuid_note = uuid_note
        
    def __repr__(self):
        """need for creating a row
        """    
        return '<VM(%s,%s,%s,%s,%s)>' % (self.name, self.active, self.ip, self.owner, self.uuid_note)
