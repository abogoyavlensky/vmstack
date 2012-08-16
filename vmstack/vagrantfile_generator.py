class VagrantfileGenerator(object):
    """ This class create a Vagrantfile with
        users's configuration of virtual machine.
    """
    def __init__(self):
        """ Set default values properties of the class
            VagrantfileGenerator
        """
        self._box_name = 'lucid32'
        self._gui = 'headless'
        self.memory = 384

    @property
    def box_name(self):
        """ box_name - name a box to build virtual machine.
            (Default = 'lucid32')
        """
        return self._box_name

    @box_name.setter
    def box_name(self,value):
        self._box_name = value


    @property
    def gui(self):
        """ If property  gui = 'gui' - Boot with a GUI so you can see the screen.
            (Default = 'headless')
        """
        return self._gui

    @gui.setter
    def gui(self,value):
        if value == 'True':
            self._gui = 'gui'


    @property
    def memory(self):
        """ memory - number of RAM on virtual machine.
            (Default = 384)
        """
        return self._memory

    @memory.setter
    def memory(self,value):
        if type(value) == int:
            self._memory = value


    def generate_vagrantfile(self):
        lines_vf = []
        vm_attr_str = ''
        vm_attr_list = ['modifyvm',':id','--memory',self.memory]
        len_vm_list = len(vm_attr_list)

        lines_vf.append('# -*- mode: ruby -*-\n')
        lines_vf.append('# vi: set ft=ruby :\n')
        lines_vf.append('Vagrant::Config.run do |config|\n')
        lines_vf.append('  config.vm.box = "%s"\n' % self.box_name)
        lines_vf.append('  config.vm.boot_mode = :%s\n' % self.gui)

        for i in xrange(0,len_vm_list-1,2):
            vm_attr_str = vm_attr_str + '"%s", %s, ' % (vm_attr_list[i],vm_attr_list[i+1])
        vm_attr_str = vm_attr_str[:len(vm_attr_str)-2]

        lines_vf.append('  config.vm.customize [%s]\n' % vm_attr_str)
        lines_vf.append('end')

        f = open('Vagrantfile','w')
        f.writelines(lines_vf)
        f.close()
        #return lines_vf


#config.vm.customize ["modifyvm", :id, "--memory", 1024]