from vagrantfile_generator import VagrantfileGenerator

def main():
    obj = VagrantfileGenerator()
    obj.box_name = 'lucid32'
    obj.gui = 'true'
    obj.memory = 1024
    obj.accelerate3d = 'on'
    obj.nic1 = 'bridged'
    obj.nictype1 = 'Am79C973'
    obj.cableconnected1 = 'off'
    obj.vram = 12
    obj.generate_vagrantfile()


if __name__=='__main__':
    main()