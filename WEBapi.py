import os
import VMserver
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

tornado.options.define("port", default=8000, help="run on the given port", type = int)

vm_cmd_api = VMserver.VMserver()

class GreetHandler(tornado.web.RequestHandler):
    """Handler for Greeting, when someone come on "main page"
    """
    def get(self):
        self.write("Hello, my master!\nI'm greeting to you!\n")

class VMInfoHandler(tornado.web.RequestHandler):
    """Handler for good reaction on showing information about virtual machine
    """
    def get(self):
        self.render('info.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        vm_cmd_api.vm_info(name_vm)
        self.render('info_out.html', name = name_vm,
                    out_info = vm_cmd_api.get_statusoutput()[1].split('\n'))
        
class CloneVMHandler(tornado.web.RequestHandler):
    """Handler for good reaction on cloning virtual machine
    """
    def get(self):
        self.render('clone.html')
    
    def post(self):
        name_parent_vm = self.get_argument('parent_vm')
        name_child_vm = self.get_argument('child_vm')
        if vm_cmd_api.clone_vm(name_parent_vm, name_child_vm):
            if vm_cmd_api.get_statusoutput()[0] == 0:
                print("All OK. I clone what you want.\n")
            else:
                print("Not OK. I don't clone what you want.\n")

class StartVMHandler(tornado.web.RequestHandler):
    """Handler for good reaction on starting virtual machine
    """
    def get(self):
        self.render('start.html')
        
    def post(self):
        name_vm = self.get_argument('name_vm')
        vm_cmd_api.start_vm(name_vm)
        self.write('To know your virtual machine ip check /get_ip.')

class StopVMHandler(tornado.web.RequestHandler):
    """Handler for good reaction on stoping virtual machine
    """
    def get(self):
        self.render('stop.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        safely = self.get_argument('safely')
        print(safely)
        vm_cmd_api.stop_vm(name_vm, safely)
        self.write(vm_cmd_api.get_statusoutput()[1])

class DeleteVMHandler(tornado.web.RequestHandler):
    """Handler for good reaction on deleting virtual machine
    """
    def get(self):
        self.render('delete.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        vm_cmd_api.delete_vm(name_vm)
        self.write(vm_cmd_api.get_statusoutput()[1])

class GetVMIpHandler(tornado.web.RequestHandler):
    """Handler for good reaction on starting virtual machine
    """
    def get(self):
        self.render('get_ip.html')
        
    def post(self):
        name_vm = self.get_argument('name_vm')
        ip = vm_cmd_api.get_vm_ip(name_vm)
        self.write('Your virtual machine ip is ' + ip +'.')


        
def main():
    """Main function, run if module is a main module
    Create a Tornado Web api and put Hendlers
    """
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [(r"/", GreetHandler),
                    (r"/info", VMInfoHandler),
                    (r"/start", StartVMHandler),
                    (r"/stop", StopVMHandler),
                    (r"/delete", DeleteVMHandler),
                    (r"/get_ip", GetVMIpHandler),
                    (r"/clone", CloneVMHandler)],
        template_path = os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()