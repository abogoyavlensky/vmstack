import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import VMtable

Base = declarative_base()

class DBserver():
    """virtual machines database class 
    """
    def __init__(self, detail = False):
        self.engine = sqlalchemy.create_engine('sqlite:///server.db', echo = detail)
        Base.metadata.create_all(self.engine)
        Session = sqlalchemy.orm.sessionmaker(bind = self.engine)
        self.session = Session()
        
    def check_name(self, name):
        """DB.check_name(S) -> bool
        
        Return True if S is contain in database table "VMs" column "name", False othewise
        """
        for names_in_DB in self.session.query(VMtable.VM).filter(VMtable.VM.name == name):
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
        if not self.check_name(name)[0]:
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

    def setStarted(self, name, ip):
        """Set row in table "VMs" as started (column "started" = True)
        row is a row whichcontain name in column "name"
        """
        set_vm = self.session.query(VMtable.VM).filter(VMtable.VM.name == name).one()
        set_vm.started = True
        set_vm.ip = ip
        self.session.commit()
        
    def setStoped(self,name):
        """Set row in table "VMs" as stoped (column "started" = False)
        row is a row which contain name in column "name"
        """
        set_vm = self.session.query(VMtable.VM).filter(VMtable.VM.name == name).one()
        set_vm.started = False
        set_vm.ip = '0.0.0.0'
        self.session.commit()
