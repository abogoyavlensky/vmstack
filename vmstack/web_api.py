import os
import uuid
import base64

import vm_server
import user_server
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

tornado.options.define("port", default=8000,
                       help="run on the given port", type = int)


class BaseHandler(tornado.web.RequestHandler):
    """Base Hanldler class for authenticating user
    """
    def get_current_user(self):
        return self.get_secure_cookie("user_name", max_age_days = 1)

class RegisterHandler(BaseHandler):
    """Hanldler class for register user and creating user's cokkie
    """
    def get(self):
        self.render('register.html')

    def post(self):
        user_name = self.get_argument("user_name")
        user_pass = self.get_argument("user_password_1")
        if user_pass != self.get_argument("user_password_2"):
            return self.write("passwords mast be equal")

        user_db_api = user_server.USERserver()
        user_db_api.create_user(user_name, user_pass)
        
        self.set_secure_cookie("user_name", user_name, expires_days = 1)
        self.redirect(r"/")

class LoginHandler(BaseHandler):
    """Handler for creating user's cookie
    """
    def get(self):
        self.render('login.html')

    def post(self):
        user_name = self.get_argument("user_name")
        user_pass = self.get_argument("user_password")
        user_db_api = user_server.USERserver()
        if not user_db_api.check_user(user_name, user_pass):
            return self.write("Wrong user or wrong password")

        self.set_secure_cookie("user_name", user_name, expires_days = 1)
        self.redirect(r"/")

class GreetHandler(BaseHandler):
    """Handler for Greeting, when someone come on "main page"
    """
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user_name = self.current_user)

class VMsListHandler(BaseHandler):
    """Handler for showing users virtual machines name list
    """
    @tornado.web.authenticated
    def get(self):
        self.render('stuff_button.html')
        
    def post(self):
        user_db_api = user_server.USERserver()
        self.render('stuff.html', user_name = self.current_user,
                    vm_list = user_db_api.get_stuff(self.current_user))

        
class VMInfoHandler(BaseHandler):
    """Handler for good reaction on showing information about virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('info.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        vm_cmd_api = vm_server.VMserver(self.current_user)
        vm_cmd_api.vm_info(name_vm)
        self.render('info_out.html', name = name_vm,
                    out_info = vm_cmd_api.get_statusoutput()[1].split('\n'))
        
class CloneVMHandler(BaseHandler):
    """Handler for good reaction on cloning virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('clone.html')

    @tornado.web.asynchronous
    def post(self):
        name_parent_vm = self.get_argument('parent_vm')
        name_child_vm = self.get_argument('child_vm')
        vm_cmd_api = vm_server.VMserver(self.current_user)
        vm_cmd_api.clone_vm(name_parent_vm, name_child_vm)
        if vm_cmd_api.get_statusoutput()[0] == 0:
            self.write("All OK. I clone what you want.\n")
        else:
            self.write("Not OK. I don't clone what you want.\n")
#        result = yield tornado.gen.Task(clone, name_parent_vm, name_child_vm)
        self.finish()
            
class StartVMHandler(BaseHandler):
    """Handler for good reaction on starting virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('start.html')

    @tornado.web.asynchronous
    def post(self):
        name_vm = self.get_argument('name_vm')
        start_type = self.get_argument('start_type')
        vm_cmd_api = vm_server.VMserver(self.current_user)
        if not vm_cmd_api.start_vm(name_vm, start_type):
            self.write("I can't start you virtual machine " + name_vm)
#        result = yield tornado.gen.Task(vm_cmd_api.start_vm, name_vm, start_type)
        self.write('To know your virtual machine ip check /get_ip.')
        self.finish()

class StopVMHandler(BaseHandler):
    """Handler for good reaction on stoping virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('stop.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        safely = self.get_argument('safely')
        vm_cmd_api = vm_server.VMserver(self.current_user)
        vm_cmd_api.stop_vm(name_vm, bool(safely))
        self.write(vm_cmd_api.get_statusoutput()[1])

class DeleteVMHandler(BaseHandler):
    """Handler for good reaction on deleting virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('delete.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        vm_cmd_api = vm_server.VMserver(self.current_user)
        vm_cmd_api.delete_vm(name_vm)
        self.write(vm_cmd_api.get_statusoutput()[1])

class GetVMIpHandler(BaseHandler):
    """Handler for good reaction on starting virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('get_ip.html')
        
    def post(self):
        name_vm = self.get_argument('name_vm')
        vm_cmd_api = vm_server.VMserver(self.current_user)
        ip = vm_cmd_api.get_vm_ip(name_vm)
        self.write('Your virtual machine ip is ' + ip +'.')

class ConfigHandler(BaseHandler):
    """Handler for change some virtual machine hardware
    """
    @tornado.web.authenticated
    def get(self):
        self.render('configs.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        ram = self.get_argument('ram')
        vram = self.get_argument('vram')
        accelerate3d = self.get_argument('accelerate3d')
        vm_cmd_api = vm_server.VMserver(self.current_user)
        vm_cmd_api.config_hardware_vm(name_vm, ram, vram, accelerate3d)
        self.write(vm_cmd_api.get_statusoutput()[1])
        
class LogoutHandler(BaseHandler):
    """Handler for clearing user's cookie
    """
    def get(self):
        self.write(str(self.current_user) + " loged out")
        self.clear_cookie('user_name')

def main():
    """Main function, run if module is a main module
    Create a Tornado Web api and put Hendlers
    """
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "vQyvZtIcSxa94ls6zub7EHQkXQF4Z0QGt+0xIAQlcmo=",
        "login_url": "/login"
    }
    application = tornado.web.Application(
        [(r"/", GreetHandler),
         (r"/info", VMInfoHandler),
         (r"/start", StartVMHandler),
         (r"/stop", StopVMHandler),
         (r"/delete", DeleteVMHandler),
         (r"/get_ip", GetVMIpHandler),
         (r"/login", LoginHandler),
         (r"/logout", LogoutHandler),
         (r"/register", RegisterHandler),
         (r"/clone", CloneVMHandler),
         (r"/configs", ConfigHandler),
         (r"/list", VMsListHandler)
     ], **settings)
    
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':        
    main()