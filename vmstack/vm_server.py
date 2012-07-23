import commands
import re
import db_server
import vm_table
import uuid

class VMserver():
    """VirtualBox-Server connector class   
    """
    def __init__(self, owner):
        """Constructor of VMserver:
            VMserver.status_output [turple] is contain result of commands.getstatusoutput([str]) (status [int], output [str])
            VMserver._input [str] is a string for execution
            VMserver.database [DBserver.DBserver] is a database of virtual machines
            VMserver.owner [str] is a owner name
        """
        self.owner = owner
        self.status_output = (0, 'ready to work')
        self._input = 'echo'
        self.database = db_server.DBserver('server.db', (vm_table.base,))
        self.vm_ip = ''
        self.vm_mac = ''
        
    def create_vm(self, name_vm):
        """VMserver.create_vm(name_vm) -> bool
        
        Create a virtual machine with name "name_vm"
        
        Return True if it is sucsesful, False otherwise
        """
        uuid_vm = str(uuid.uuid4())
        if self.database.check_uuid(vm_table.VM, uuid_vm)[0]:
            return False
            
        self._input = 'VBoxManage createvm "%s" --uuid {%s} --basefolder "%s"--register' %\
                      (name_vm, uuid_vm[1], 'users/%s' % self.owner)
        
        if self.execute(self._input)[0] != 0:
            return False
            
        return self.database.add(vm_table.VM,
                                 name_vm, (False, '0.0.0.0', self.owner, uuid_vm),
                                 ownership = True)
        return True
            
    def start_vm(self, name_vm, start_type):
        """VMserver.start_vm(name_vm, start_type) -> bool
        
        Start a virtual machine with name "name_vm"
        Start a virtual machine with gui type "start_type":
              -gui run virtual machine with gui on host
              -headless run virtual machine without gui on host
        
        Return True if it is sucsesful, False otherwise
        """
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        self.config_bridge_vm(uuid_vm[1])

        self._input = 'VBoxManage startvm {%s} --type %s' % (uuid_vm[1], start_type)
        if self.execute(self._input)[0] != 0:
            return False

        self.database.set_active(vm_table.VM, name_vm, True, self.owner)        
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
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        self._input = 'VBoxManage showvminfo {%s}' % uuid_vm[1]
        self.execute(self._input)
        return True
        
    def clone_vm(self, name_parent_vm, name_child_vm):
        """VMserver.start_vm(name_parent_vm, name_child_vm = name_parent_vm + '_cloned') -> bool

        Clone a virtual machine "name_parent_vm" with name "name_child_vm" 
        
        Return True if it is sucsesful, False otherwise
        """
        uuid_vm = str(uuid.uuid4())
        if self.database.check_uuid(vm_table.VM, uuid_vm)[0]:
            return False
        
        self._input = 'VBoxManage clonevm "%s" --name "%s" --uuid {%s} --basefolder "%s" --register' %\
                      (name_parent_vm, name_child_vm, uuid_vm, 'users/%s' % self.owner) 

        if self.execute(self._input)[0] != 0:
            return False
            
        self.database.add(vm_table.VM,
                          name_child_vm, (False, '0.0.0.0', self.owner, uuid_vm),
                          ownership = True)
        return True
        
    def control_vm(self, name_vm, what_to_do):
        """If type in cmd command 'VBoxManage controlvm "naem_vm" "what_to_do"' it will be the same 
        """
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        self._input = 'VBoxManage controlvm {%s} %s'% (uuid_vm[1], what_to_do)
        self.execute(self._input)
        
    def stop_vm(self, name_vm, safely = False):
        """VMserver.stop_vm(name_vm, safe = False) -> bool

        Stop a virtual machine with name "name_vm" [str]
        If safely is True do it safely (save current state,
           after "start_vm()" virtual machine will have its state)
        
        Return True if it is sucsesful, False otherwise
        """
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        if safely:
            self._input = 'VBoxManage controlvm {%s} acpipowerbutton' % uuid_vm[1] 
        else:
            self._input = 'VBoxManage controlvm {%s} poweroff' % uuid_vm[1]
        if self.execute(self._input)[0] !=0:
            return False
            
        self.database.set_active(vm_table.VM, name_vm, False, self.owner)
        return True
        
    def delete_vm(self, name_vm):
        """VMserver.delete_vm(name_vm) -> bool

        Delete a virtual machine with name "name_vm"
        
        Return True if it is sucsesful, False otherwise
        """
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        self._input = 'VBoxManage unregistervm {%s} --delete' % uuid_vm[1]
        if self.execute(self._input)[0] != 0:
            return False
        self.database.delete(vm_table.VM, name_vm, self.owner)
        return True

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
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        self._input = "VBoxManage list runningvms"
        self.execute(self._input)
        check_uuid_vm = '{%s}' % uuid_vm[1] 
        if check_uuid_vm in self.status_output[1]:
            self.database.set_active(vm_table.VM, name_vm, True, self.owner)
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
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        self._input = 'VBoxManage controlvm {%s} --natpf1 "guist_ssh, tcp, ,%s, ,%s"' % uuid_vm[1]
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm {%s} --nic1 nat' % uuid_vm[1]
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm {%s} --nictype1 82540EM' % uuid_vm[1]
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm {%s} --cableconnected1 on' % uuid_vm[1]
        self.execute(self._input)
                

    def config_hardware_vm(self, name_vm, memory_vm = "2048", vram_vm = "32", accelerate3d_vm = "on"):
        """name_vm is a virtual machine "name"

        Configurate a new registered virtual machine with next:
        RAM: memory_vm in MB
        VRAM: vram_vm in MB
        accelarate3d: accelarate3d_vm "on"/"off"
        """
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        self._input = 'VBoxManage modifyvm {%s} --memory %s --vram %s --accelerate3d %s' %\
                      (uuid_vm[1], memory_vm, vram_vm, accelerate3d_vm)
        self. execute(self._input)

    def get_vm_mac(self, name_vm):
        """VMserver.get_vm_mac(name_vm) -> [str]

        Return MAC addres of started virtual machine with name "name_vm" [str]

        """
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        self._input = 'VBoxManage showvminfo {%s}' % uuid_vm[1]
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
        self._input = "arp -a | grep %s" % self.get_vm_mac(name_vm)
        self.execute(self._input)
        self.vm_ip = re.search('[(](\d+)[.](\d+)[.](\d+)[.](\d+)[)]', self.status_output[1])
        if self.vm_ip == None:
            return None
        self.vm_ip = self.vm_ip.group(0)[1:-1]
        self.database.set_ip(vm_table.VM, name_vm, self.vm_ip, self.owner)
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
        uuid_vm = self.database.get_uuid(vm_table.VM, name_vm, self.owner)
        if not uuid_vm[0]:
            return False

        self._input = 'VBoxManage modifyvm "%s" --boot1 %s' % uuid_vm[1], boot1
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm "%s" --boot2 %s' % uuid_vm[1], boot2
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm "%s" --boot3 %s' % uuid_vm[1], boot3
        self.execute(self._input)
        self._input = 'VBoxManage modifyvm "%s" --boot4 %s' % uuid_vm[1], boot4
        self.execute(self._input)
