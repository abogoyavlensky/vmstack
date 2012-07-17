import USERtable
import DBserver

class USERserver():
    """USERdatabase-Server connetor class
    """
    def __init__(self):
        self.database = DBserver.DBserver('server.db', (USERtable.base,))

    def create_user(self, name_user, password):
        """USERserver.create_user(name_user) -> bool
        
        Create a user note  with name "name_user"
        
        Return True if it is sucsesful, False otherwise
        """
        return self.database.add(USERtable.USER, name_user, (password,))

    def delete_user(self, name_user):
        """USERserver.delete_user(name_user) -> bool

        Delete a user with name "name_user"
        
        Return True if it is sucsesful, False otherwise
        """
        return self.database.delete(USERtable.USER, name_user)

    def check_user(self, name_user, password):
        return self.database.check_user(USERtable.USER, name_user, password)
        
