import user_table
import db_server
import vm_table

class USERserver():
    """USERdatabase-Server connetor class
    """
    def __init__(self):
        self.database = db_server.DBserver('server.db', (user_table.base,))

    def create_user(self, name_user, password):
        """USERserver.create_user(name_user) -> bool
        
        Create a user note  with name "name_user"
        
        Return True if it is sucsesful, False otherwise
        """
        return self.database.add(user_table.USER, name_user, (password,))

    def delete_user(self, name_user):
        """USERserver.delete_user(name_user) -> bool

        Delete a user with name "name_user"
        
        Return True if it is sucsesful, False otherwise
        """
        return self.database.delete(user_table.USER, name_user)

    def check_user(self, name_user, password):
        """Check user's password
        """
        return self.database.check_user(user_table.USER, name_user, password)
        
    def get_stuff(self, name_user):
        """Return user's virtual machines names list
        """
        return self.database.get_stuff(vm_table.VM, name_user)