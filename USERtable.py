import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Boolean

base = declarative_base()

class USER(base):
    """This is "USER" table, which contain:
    
        user "id" [int] (is a primaty_key)
        user "name" [str] (shoud not be repeated)
        user "active"[bool] (active/inactive)
        user "password"[str]
    """
    __tablename__ = 'USERs'

    id = sqlalchemy.Column(Integer, primary_key = True)
    name = sqlalchemy.Column(String)
    password = sqlalchemy.Column(String)


    def __init__(self, name, (password,)):
        """name [str] is user's' "name"
        password [str] is user's "password"
        active [bool] need for understanding user active loged in (active = True)
                                                     or loged out (active = False)
        """
        self.name = name
        self.password = password

    def __repr__(self):
        """need for creating a row
        """    
        return '<VM(%s,%s)>' % (self.name, self.password)

