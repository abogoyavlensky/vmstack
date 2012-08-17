class VagrantfileGenerator(object):
    """ This class create a Vagrantfile with
        users's configuration of virtual machine.
    """
    def __init__(self):
        """ Set default values properties of the class
            VagrantfileGenerator
        """
        self._name = 'my_virtual_machine'
        self._box_name = 'lucid32'
        self._gui = 'headless'
        self._memory = 384
        self._accelerate3d = 'off'
        #self._nic1 = 'nat'
        self._nictype1 = '82540EM'
        self._cableconnected1 = 'on'
        self._vram = 8
        self._ip = "10.11.12.13"
        self._hd_size = 10000
        self._set_cookbook = []

    @property
    def name(self):
        """ name - You can set name of your virtual machine.
            (Default = 'my_virtual_machine')
        """
        return self._name

    @name.setter
    def name(self,value):
        if type(value) == str:
            self._name = value


    @property
    def box_name(self):
        """ box_name - You can set name a box to build virtual machine.
            (Default = 'lucid32')
        """
        return self._box_name

    @box_name.setter
    def box_name(self,value):
        if type(value) == str:
            self._box_name = value


    @property
    def gui(self):
        """ gui - You can set boot with a GUI so you can see the screen.
            Possible value: true | false
            (Default = 'false')
        """
        return self._gui

    @gui.setter
    def gui(self,value):
        if value == 'true':
            self._gui = 'gui'


    @property
    def memory(self):
        """ memory - You can set number of RAM (in MB) on virtual machine.
            (Default = 384)
        """
        return self._memory

    @memory.setter
    def memory(self,value):
        if type(value) == int:
            self._memory = value


    @property
    def accelerate3d(self):
        """ accelerate3d - You can on hardware 3D acceleration.
            Possible value: on | off
            (Default = 'off')
        """
        return self._accelerate3d

    @accelerate3d.setter
    def accelerate3d(self,value):
        if value == 'on':
            self._accelerate3d = value


#    @property
#    def nic1(self):
#        """ nic1 -  You can set type of networking.
#            Possible value: none|null|nat|bridged|intnet|generic
#            (Default = 'nat')
#        """
#        return self._nic1
#
#    @nic1.setter
#    def nic1(self,value):
#        if type(value) == str:
#            self._nic1 = value


    @property
    def nictype1(self):
        """ nictype1 -  This allows you to specify which networking
                        hardware VirtualBox presents to the guest.
            Possible value: Am79C970A|Am79C973|82540EM|82543GC|82545EM|virtio
            (Default = '82540EM')
        """
        return self._nictype1

    @nictype1.setter
    def nictype1(self,value):
        if type(value) == str:
            self._nictype1 = value


    @property
    def cableconnected1(self):
        """ cableconnected1 - This allows you to temporarily disconnect
                              a virtual network interface, as if a network cable had been
                              pulled from a real network card.
            Possible value: on | off
            (Default = 'on')
        """
        return self._cableconnected1

    @cableconnected1.setter
    def cableconnected1(self,value):
        if value == 'on':
            self._cableconnected1 = value


    @property
    def vram(self):
        """ vram - You can set number of RAM (in MB) that the virtual
                   graphics card should have.
            (Default = 8)
        """
        return self._vram

    @vram.setter
    def vram(self,value):
        if type(value) == int:
            self._vram = value


    @property
    def ip(self):
        """ ip - This will configure a host only network on the virtual
                 machine that is assigned a static IP of.
            (Default = "10.11.12.13")
        """
        return self._ip

    @ip.setter
    def ip(self,value):
        self._ip = value


    @property
    def hd_size(self):
        """ hd_size - You can set number of hd size (in MB) on virtual machine.
            (Default = 10000)
        """
        return self._hd_size

    @hd_size.setter
    def hd_size(self,value):
        if type(value) == int:
            self._hd_size = value

    @property
    def set_cookbook(self):
        """ set_cookbook - You can set your cookbook.
            (Default = [])
        """
        return self._set_cookbook

    @set_cookbook.setter
    def set_cookbook(self,value):
        if type(value) == list:
            self._set_cookbook = value

    def generate_vagrantfile(self):
        lines_vf = []
        vm_attr_str = ''
        vm_attr_list = ['modifyvm',':id','--name',self.name,'--memory',self.memory,'--accelerate3d', self.accelerate3d,
                        '--nictype1',self.nictype1,'--cableconnected1',self.cableconnected1,'--vram',self.vram]
        len_vm_list = len(vm_attr_list)
    #create list of strigs for Vagrantfile
        lines_vf.append('# -*- mode: ruby -*-\n')
        lines_vf.append('# vi: set ft=ruby :\n')
        lines_vf.append('Vagrant::Config.run do |config|\n')
        lines_vf.append('  config.vm.box = "%s"\n' % self.box_name)
        lines_vf.append('  config.vm.boot_mode = :%s\n' % self.gui)
        for i in xrange(0,len_vm_list-1,2):
            vm_attr_str = vm_attr_str + '"%s", %s, ' % (vm_attr_list[i],vm_attr_list[i+1])
        vm_attr_str = vm_attr_str[:len(vm_attr_str)-2]
        lines_vf.append('  config.vm.customize [%s]\n' % vm_attr_str)
        lines_vf.append('  config.vm.network :hostonly, "%s"\n' % self.ip)
        lines_vf.append('  config.vm.customize ["modifyhd", :id, "--resize", %s]\n' % self.hd_size)
        lines_vf = lines_vf + self.set_cookbook

        lines_vf.append('end')

    #create Vagrantfile
        f = open('Vagrantfile','w')
        f.writelines(lines_vf)
        f.close()
        #return lines_vf



#VBoxManage createhd --filename "WinXP.vdi" --size 10000