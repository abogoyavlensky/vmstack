import commands
import DBserver

class VMserver():
    """VirtualBox-Server connector class   
    """
    def __init__(self):
        """Constructor of VMserver:
        VMserver.Status_output [turple] is contain result of commands.getstatusoutput([str]) (status [int], output [str])
        VMserver.IN [str] is a string for execution
        VMserver.DB [DBserver.DBserver] is a database of virtual machines
        """
        self.Status_output = (0, 'ready to work')
        self.IN = 'echo'
        self.DB = DBserver.DBserver()
        
    def create_vm(self, name_vm, ostype_vm = 'Ubuntu'):
        """VMserver.create_vm(name_vm, ostype_vm = 'Ubuntu') -> bool
        
        Create a virtual machine with name "name_vm" and ostype "ostype_vm"
        
        Return True if it is sucsesful, False otherwise
        """
        self.IN = 'VBoxManage createvm "' + name_vm + '" --ostype ' + ostype_vm + ' --register'

        if self.execute(self.IN)[0] != 0:
            print 'error in create_vm:\n' + self.Status_output[1]
            return False

        self.DB.add(name_vm, False, '0.0.0.0')
        return True
            
    def start_vm(self, name_vm):
        """VMserver.start_vm(name_vm) -> bool
        
        Start a virtual machine with name "name_vm"
        
        Return True if it is sucsesful, False otherwise
        """
        self.IN = 'VBoxManage startvm "' + name_vm + '"'
        if self.execute(self.IN)[0] != 0:
            return False

        self.DB.setStarted(name_vm)
        return True

        
    def list(self, what, detailed = True):
        """Execute a 'VBoxManage list "what"'
        If detailed is True it set detail output
        """
        if detailed:
            self.IN = 'VBoxManage list --long ' 
        else:
            self.IN = 'VBoxManage list '
        self.IN = self.IN + what
        self.execute(self.IN)
        
    def clone_vm(self, name_parent_vm, name_child_vm):
        """VMserver.start_vm(name_parent_vm, name_child_vm = name_parent_vm + '_cloned') -> bool

        Clone a virtual machine "name_parent_vm" with name "name_child_vm" 
        
        Return True if it is sucsesful, False otherwise
        """
        self.IN = 'VBoxManage clonevm "' + name_parent_vm + '" --name "' + name_child_vm + '" --register'

        if self.execute(self.IN)[0] != 0:
            print 'error in clone_vm:\n' + self.Status_output[1]
            return False
            
        self.DB.add(name_child_vm, False, '0.0.0.0')
        return True
        
    def control_vm(self, name_vm, what_to_do):
        """If type in cmd command 'VBoxManage controlvm "naem_vm" "what_to_do"' it will be the same 
        """
        self.IN = 'VBoxManage controlvm "' + name_vm + '"' + what_to_do
        self.execute()
        
    def stop_vm(self, name_vm, safely = False):
        """VMserver.stop_vm(name_vm, safe = False) -> bool

        Stop a virtual machine with name "name_vm" [str]
        If safely is True do it safely (save current state,
           after "start_vm()" virtual machine will have its state)
        
        Return True if it is sucsesful, False otherwise
        """
        if safely:
            self.IN = 'VBoxManage controlvm "' + name_vm + '"' + ' savestate'
        else:
            self.IN = 'VBoxManage controlvm "' + name_vm + '"' + ' poweroff'
        if self.execute(self.IN)[0] !=0:
            return False
        self.DB.setStoped(name_vm)
        return True
        
    def delete_vm(self, name_vm):
        """VMserver.create_vm(name_vm) -> bool

        Delete a virtual machine with name "name_vm"
        
        Return True if it is sucsesful, False otherwise
        """
        self.IN = 'VBoxManage unregistervm "' + name_vm + '" --delete'
        if self.execute(self.IN)[0] != 0:
            return False
        self.DB.delete(name_vm)
        return True

    def execute(self, IN):
        """VMserver.execute(IN = self.IN) -> turple([int],[str])

        Execute cmd string contain in "IN".

        If VMserver.execute()[0] equal 0 then operation was seccussful.
        """
        self.Status_output = commands.getstatusoutput(IN)
        return self.Status_output
        
    def get_statusoutput(self):
        """VMserver.get_statusoutput() -> turple([int],[str])

        If VMserver.get_statusoutput()[0] equal 0 then last operation was seccussful.
        """
        return self.Status_output