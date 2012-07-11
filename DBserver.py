import sqlalchemy
from sqlalchemy import Integer, String, Boolean

class VM(sqlalchemy.ext.declarative.declarative_base()):
    """This is "VM" table, which contain:
    virtual machine "id" [int] (is a primaty_key)
    virtual machine "name" [str] (shoud not be repeated)
    virtual machine status [bool] (started/stoped)
    cirtual machine "ip"[str]"""
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

class DBserver():
    """virtual machines database class 
    """
    def __init__(self):
        self.engine = sqlalchemy.create_engine('sqlite:///server.db', echo = True)
        Base.metadata.create_all(self.engine)
        Session = sqlalchemy.orm.sessionmaker(bind = self.engine)
        self.session = Session()
        
    def check_name(self, name):
        """DB.check_name(S) -> bool
        
        Return True if S is contain in database table "VMs" column "name", False othewise
        """
        for names_in_DB in self.session.query(VM).filter(VM.name == name):
            return (True, names_in_DB)
        return (False, None)
        
    def add(self, name, started, ip):
        """DB.add(name, started, ip) -> bool
        
        name [str] is a created (cloned) virtual machine name
        started [bool] is a status of virtual machine (virtual machine started: True
                                                       virtual machine started: False)
        ip [str] is a virtual machine ip

        Return True if virtual machine has been already created, False otherwise 
        """
        if not self.check_name(name):
            return False
        new_vm = VM(name, started, ip)
        self.session.add(new_vm)
        self.session.commit()
        return True

    def delete(self, name):
        """DB.delete(name) -> bool
        
        name [str] is a existed virtual machine name

        Return True if name is contained in DB table "VMs", False otherwise
        """
        delete_vm = self.check_name(name)
        if not delete_vm[0]:
            return False
        self.session.delete(delete_vm[1])
        self.session.commit()
        return True

    def setStarted(self, name):
        """Set row in table "VMs" as started (column "started" = True)
        row is a row whichcontain name in column "name"
        """
        set_vm = self.session.query(VM).filter(VM.name == name).one()
        set_vm.started = True
        self.session.commit()
        
    def setStoped(self,name):
        """Set row in table "VMs" as stoped (column "started" = False)
        row is a row which contain name in column "name"
        """
        set_vm = self.session.query(VM).filter(VM.name == name).one()
        set_vm.started = False
        self.session.commit()
