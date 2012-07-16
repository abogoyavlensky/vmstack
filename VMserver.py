import commands
import re
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
        self.status_output = (0, 'ready to work')
        self._input = 'echo'
        self.database = DBserver.DBserver()
        self.vm_ip = ''
        self.vm_mac = ''
        
    def create_vm(self, name_vm):
        """VMserver.create_vm(name_vm, ostype_vm = 'Ubuntu') -> bool
        
        Create a virtual machine with name "name_vm"
        
        Return True if it is sucsesful, False otherwise
        """
        self._input = 'VBoxManage createvm "' + name_vm + ' --register'

        if self.execute(self._input)[0] != 0:
            print 'error in create_vm:\n' + self.status_output[1]
            return False

        self.database.add(name_vm, False, '0.0.0.0')
        return True
            
    def start_vm(self, name_vm):
        """VMserver.start_vm(name_vm) -> bool
        
        Start a virtual machine with name "name_vm"
        
        Return True if it is sucsesful, False otherwise
        """
        if not self.database.check_name(name_vm)[0]:
            return False

        self.config_bridge_vm(name_vm)

        self._input = 'VBoxManage startvm "' + name_vm + '"'
        if self.execute(self._input)[0] != 0:
            return 

        print(self.status_output[1])
        self.database.set_started(name_vm)        
        return True

        
    def list(self, what, detailed = True):
        """Execute a 'VBoxManage list "what"'
        If detailed is True it set detail output
        """
        if detailed:
            self._input = 'VBoxManage list --long ' 
        else:
            self._input = 'VBoxManage list '
        self._input = self._input + what
        self.execute(self._input)

    def vm_info(self, name_vm):
        """Execute operation which initialaize self.status_output[1]
        like string contained info of virtual machine
        """
        self._input = 'VBoxManage showvminfo "' + name_vm + '"'
        self.execute(self._input)
        
    def clone_vm(self, name_parent_vm, name_child_vm):
        """VMserver.start_vm(name_parent_vm, name_child_vm = name_parent_vm + '_cloned') -> bool

        Clone a virtual machine "name_parent_vm" with name "name_child_vm" 
        
        Return True if it is sucsesful, False otherwise
        """
        self._input = 'VBoxManage clonevm "' + name_parent_vm + '" --name "' + name_child_vm + '" --register'

        if self.execute(self._input)[0] != 0:
            print 'error in clone_vm:\n' + self.status_output[1]
            return False
            
        self.database.add(name_child_vm, False, '0.0.0.0')
        self.config_bridge_vm(name_child_vm)
        return True
        
    def control_vm(self, name_vm, what_to_do):
        """If type in cmd command 'VBoxManage controlvm "naem_vm" "what_to_do"' it will be the same 
        """
        self._input = 'VBoxManage controlvm "' + name_vm + '"' + what_to_do
        self.execute(self._input)
        
    def stop_vm(self, name_vm, safely = False):
        """VMserver.stop_vm(name_vm, safe = False) -> bool

        Stop a virtual machine with name "name_vm" [str]
        If safely is True do it safely (save current state,
           after "start_vm()" virtual machine will have its state)
        
        Return True if it is sucsesful, False otherwise
        """
        if safely:
            self._input = 'VBoxManage controlvm "' + name_vm + '"' + ' acpipowerbutton'
        else:
            self._input = 'VBoxManage controlvm "' + name_vm + '"' + ' poweroff'
        if self.execute(self._input)[0] !=0:
            return False
        self.database.set_stoped(name_vm)
        return True
        
    def delete_vm(self, name_vm):
        """VMserver.create_vm(name_vm) -> bool

        Delete a virtual machine with name "name_vm"
        
        Return True if it is sucsesful, False otherwise
        """
        if self.database.check_name(name_vm)[0]:
            self._input = 'VBoxManage unregistervm "' + name_vm + '" --delete'
            if self.execute(self._input)[0] != 0:
                return False
            self.database.delete(name_vm)
            return True
        else:
            print('You did not create this virtual machine')

    def execute(self, input_command):
        """VMserver.execute(IN = self.IN) -> turple([int],[str])

        Execute cmd string contain in "IN".

        If VMserver.execute()[0] equal 0 then operation was seccussful.
        """
        self.status_output = commands.getstatusoutput(input_command)
        return self.status_output
        
    def get_statusoutput(self):
        """VMserver.get_statusoutput() -> turple([int],[str])

        If VMserver.get_statusoutput()[0] equal 0 then last operation was seccussful.
        """
        return self.status_output

    def check_running_vms(self, name_vm):
        """VMserver.check_running_vms(name_vm) -> [bool]

        Return True if find virtual machine whit name "name_vm", False otherwise
        """
        self._input = "VBoxManage list runningvms"
        self.execute(self._input)
        check_name_vm = '"' + name_vm + '"'
        if check_name_vm in self.status_output[1]:
            return True

        return False

    def config_bridge_vm(self, name_vm):
        """name_vm is a virtual machine name

        Make a config for internet connection:
            connection = bridge
            bridgeadapter = en1
            connection type = Intel PRO/1000 MT Desktop (see manual for VirtualBox)
            cableconnection is on
        
        Nota bene: for bridgeadapter need type ifcondig on host, "en1" exemple
        """
        self._input = 'VBoxManage modifyvm "' + name_vm + '" --bridgeadapter1 "en1:  Ethernet (en1)"'
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm "' + name_vm + '" --nic1 bridged'
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm "' + name_vm + '" --nictype1 82540EM'
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm "' + name_vm + '" --cableconnected1 on'
        self.execute(self._input)
                

    def config_hardware_vm(self, name_vm, memory_vm = "2048", vram_vm = "32", accelerate3d_vm = "on"):
        """name_vm is a virtual machine "name"

        Configurate a new registered virtual machine with next:
        RAM: memory_vm in MB
        VRAM: vram_vm in MB
        if accelarate3d is True
        """    
        self._input = 'VBoxManage modifyvm "' + name_vm + '" --memory ' + memory_vm + ' --vram ' + vram_vm + ' --accelerate3d ' + accelerate3d_vm
        self. execute(self._input)

    def get_vm_mac(self, name_vm):
        """VMserver.get_vm_mac(name_vm) -> [str]

        Return MAC addres of started virtual machine with name "name_vm" [str]

        """
        self._input = 'VBoxManage showvminfo "' + name_vm + '"'
        self.execute(self._input)
        mac_address_vm = re.search("\sNIC (\d):           MAC: (\w+)", self.status_output[1]).group(2).lower()
        self.vm_mac = ''
        for i in range(6):
            if mac_address_vm[i*2] == '0':
                self.vm_mac = self.vm_mac + mac_address_vm[i*2+1] + ':'
            else:
                self.vm_mac = self.vm_mac + mac_address_vm[i*2 : i*2+2] + ':'
        self.vm_mac = self.vm_mac[:-1]
        print(self.vm_mac)
        return self.vm_mac

    def get_vm_ip(self, name_vm):
        """VMserver.get_vm_ip(name_vm) -> [str]

        Return IP addres of started virtual machine with name "name_vm" [str]
        """
        self._input = "arp -a | grep " + self.get_vm_mac(name_vm)
        self.execute(self._input)
        self.vm_ip = re.search('[(](\d+)[.](\d+)[.](\d+)[.](\d+)[)]', self.status_output[1])
        self.vm_ip = self.vm_ip.group(0)[1:-1]
        self.database.set_ip(name_vm, self.vm_ip)
        return self.vm_ip

    def set_boot_order(self, name_vm,
                       boot1 = 'net', boot2 = 'disk',
                       boot3 = 'none', boot4 = 'none'):
        """Set a boot order like:
        1.boot1
        2.boot2
        3.boot3
        4.boot4
        
        All of them shold be uniqe (except "none" ):
                none, floppy, dvd, disk, net
        """
        self._input = 'VBoxManage modifyvm "' + name_vm + '" --boot1 ' + boot1
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm "' + name_vm + '" --boot2 ' + boot2
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm "' + name_vm + '" --boot3 ' + boot3
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm "' + name_vm + '" --boot4 ' + boot4
        self.execute(self._input)
