from vagrantfile_generator import VagrantfileGenerator

def main():
    obj = VagrantfileGenerator()
    obj.box_name = 'lucid32'
    obj.gui = 'False'
    obj.memory = 1024
    obj.generate_vagrantfile()


if __name__=='__main__':
    main()