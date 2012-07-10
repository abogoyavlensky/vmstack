import commands

class VMserver():
    def __init__(self):
        self.Status_output = (0, 'ready to work')
        self.IN = 'echo'
        
    def create_vm(self, name_vm, ostype_vm = 'Ubuntu'):
        self.IN = 'VBoxManage createvm "' + name_vm + '" --ostype ' + ostype_vm + ' --register'

    def start_vm(self, name_vm):
        self.IN = 'VBoxManage startvm "' + name_vm + '"'

    def list(self, what, detailed = True):
        if detailed:
            self.IN = 'VBoxManage list --long ' 
        else:
            self.IN = 'VBoxManage list '
        self.IN = self.IN + what

    def clone_vm(self, name_parent_vm, name_child_vm):
        self.IN = 'VBoxManage clonevm "' + name_parent_vm + '" --name "' + name_child_vm + '" --register'

    def control_vm(self, name_vm, what_to_do):
        self.IN = 'VBoxManage controlvm "' + name_vm + '"' + what_to_do

    def delete_vm(self, name_vm):
        self.IN = 'VBoxManage unregistervm "' + name_vm + '" --delete'

    def execute(self):
        self.Status_output = commands.getstatusoutput(self.IN)
    
    def get_statusoutput(self):
        return self.Status_output