import os
import uuid
import base64

import VMserver
import USERserver
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

tornado.options.define("port", default=8000, help="run on the given port", type = int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        """Base Hanldler class for authenticating user
        """
        return (self.get_secure_cookie("user_name", max_age_days = 1),
                self.get_secure_cookie("user_password", max_age_days = 1))

class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        user_name = self.get_argument("user_name")
        user_pass = self.get_argument("user_password_1")
        if user_pass != self.get_argument("user_password_2"):
            return write("passwords mast be equal")

        user_db_api = USERserver.USERserver()
        user_db_api.create_user(user_name, user_pass)
        
        self.set_secure_cookie("user_name",
                               user_name, expires_days = 1)
        
        self.set_secure_cookie("user_password",
                               user_pass, expires_days = 1)
        self.redirect(r"/")

class LoginHandler(BaseHandler):
    """Handler for creating user's cookie
    """
    def get(self):
        self.render('login.html')

    def post(self):
        user_name = self.get_argument("user_name")
        user_pass = self.get_argument("user_password")
        user_db_api = USERserver.USERserver()
        if not user_db_api.check_user(user_name, user_pass):
            return

        self.set_secure_cookie("user_name",
                               user_name, expires_days = 1)
        self.set_secure_cookie("user_password",
                               user_pass, expires_days = 1)
        self.redirect(r"/")

class GreetHandler(BaseHandler):
    """Handler for Greeting, when someone come on "main page"
    """
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user_name = self.current_user[0])

class VMInfoHandler(BaseHandler):
    """Handler for good reaction on showing information about virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('info.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        vm_cmd_api = VMserver.VMserver()
        vm_cmd_api.vm_info(name_vm)
        self.render('info_out.html', name = name_vm,
                    out_info = vm_cmd_api.get_statusoutput()[1].split('\n'))
        
class CloneVMHandler(BaseHandler):
    """Handler for good reaction on cloning virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('clone.html')
    
    def post(self):
        name_parent_vm = self.get_argument('parent_vm')
        name_child_vm = self.get_argument('child_vm')
        vm_cmd_api = VMserver.VMserver()
        if vm_cmd_api.clone_vm(name_parent_vm, name_child_vm):
            if vm_cmd_api.get_statusoutput()[0] == 0:
                print("All OK. I clone what you want.\n")
            else:
                print("Not OK. I don't clone what you want.\n")

class StartVMHandler(BaseHandler):
    """Handler for good reaction on starting virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('start.html')
        
    def post(self):
        name_vm = self.get_argument('name_vm')
        start_type = self.get_argument('start_type')
        vm_cmd_api = VMserver.VMserver()
        vm_cmd_api.start_vm(name_vm, start_type)
        self.write('To know your virtual machine ip check /get_ip.')

class StopVMHandler(BaseHandler):
    """Handler for good reaction on stoping virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('stop.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        safely = self.get_argument('safely')
        print(safely)
        vm_cmd_api = VMserver.VMserver()
        vm_cmd_api.stop_vm(name_vm, safely)
        self.write(vm_cmd_api.get_statusoutput()[1])

class DeleteVMHandler(BaseHandler):
    """Handler for good reaction on deleting virtual machine
    """
    @tornado.web.authenticated
    def get(self):
        self.render('delete.html')

    def post(self):
        name_vm = self.get_argument('name_vm')
        vm_cmd_api = VMserver.VMserver()
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
        vm_cmd_api = VMserver.VMserver()
        ip = vm_cmd_api.get_vm_ip(name_vm)
        self.write('Your virtual machine ip is ' + ip +'.')

class LogoutHandler(BaseHandler):
    """Handler for clearing user's cookie
    """
    def get(self):
        self.write(str(self.current_user[0]) + " loged out")
        self.clear_cookie('user_name')
        self.clear_cookie('user_password')

def main():
    """Main function, run if module is a main module
    Create a Tornado Web api and put Hendlers
    """
    tornado.options.parse_command_line()

#    secure_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), "templates"),
        'cookie_secret': "1342502742|92c61b1d3a7cd3434cba04e0375229b99f7573aa",
        "xsrf_cokkies": True,
        'login_url': "/login"
    }

    application = tornado.web.Application(
        handlers = [(r"/", GreetHandler),
                    (r"/info", VMInfoHandler),
                    (r"/start", StartVMHandler),
                    (r"/stop", StopVMHandler),
                    (r"/delete", DeleteVMHandler),
                    (r"/get_ip", GetVMIpHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    (r"/register", RegisterHandler),
                    (r"/clone", CloneVMHandler)],
        **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()