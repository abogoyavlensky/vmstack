import xml.dom
import xml.dom.minidom

class ChangerPref():
    def __init__(self, filename):
        self.document = xml.dom.minidom.parse(filename)
        self.filename = filename
        
    def change_memory(self, memory_size):
        memory = self.document.getElementsByTagName('Memory')
        memory.item(0).setAttribute('RAMSize', memory_size)

    def change_mac(self, nic_index, mac_address):
        nics = self.document.getElementsByTagName('Adapter')
        for i in range(nics.length):
            if nics.item(i).getAttridute('slot') == nic_index:
                nics.item(0).setAttribute('MACAddress', mac_address)

    def push(self):
        new_file = open(self.filename, 'w')
        data = self.document.toxml('utf_8')
        new_file.write(data)
        new_file.close()