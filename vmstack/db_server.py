import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


class DBserver():
    """database class:
    support: VMtable, USERtable
    """
    def __init__(self, db_name, tables_base, detail = False):
        self.engine = sqlalchemy.create_engine('sqlite:///' + db_name, echo = detail)
        for table_base in tables_base:
            table_base.metadata.create_all(self.engine)
        Session = sqlalchemy.orm.sessionmaker(bind = self.engine)
        self.session = Session()
        
    def check_name(self, table, name, owner = None):
        """DB.check_name(T, S1, S2 = None) -> bool
        
        Return True if "S1" is contain in database table "T" column "name"
             and if "S2" is contain in database table "T" column "owner"
             or if S2 not a None, False othewise
        """
        if owner == None:
            for note_in_DB in self.session.query(table).filter(table.name == name):
                return (True, note_in_DB)
        else:
            for note_in_DB in self.session.query(table).filter(table.name == name,
                                                           table.owner == owner):
                return (True, note_in_DB)
        return (False, None)

    def add(self, table, name, parameters, ownership = False):
        """DB.add(T, S, P, O) -> bool

        T [str] is a table name for addition
        S [str] will be added in column "name"
        P [turple] will be added in all other column 
        onwership [bool] should be used when you want to check belonging to it's' onwer
        
        Return True if note hasn't already been added, False otherwise 
        """
        new_note = table(name, parameters)
        if ownership:
            if self.check_name(table, new_note.name, new_note.owner)[0]:
                return False
        else:
            if self.check_name(table, new_note.name)[0]:
                return False

        self.session.add(new_note)
        self.session.commit()
        return True

    def delete(self, table, name, owner = None):
        """DB.delete(name) -> bool
        
        name [str] is a existed note column "name"
        owner [str] is a existed note column "owner"

        Return True if name is contained in database table "T" and was deleted successfuly,
               False if name isn't contained in database table "T",
               None if deletion was unsuccessful
        """
        delete_note = self.check_name(table, name, owner)
        if not delete_note[0]:
            return False
        self.session.delete(delete_note[1])
        self.session.commit()
        return True

    def check_user(self, table, name, password):
        """Check "row" in table "table" is contained 
        "row" is a row which contain name in column "name"
                         and password in column "password" 
        """
        check_note = self.check_name(table, name)
        if not check_note[0]:
            return None
            
        return check_note[1].password == password 
            
    def set_active(self, table, name, active, owner):
        """Set "active" in "row" in table with "table" like active
        row is a row which contain name in column "name"
                             and owner in column "owner" 

        """
        set_note = self.check_name(table, name, owner) 
        if not set_note[0]:
            return None
            
        set_note[1].active = active
        self.session.commit()
        
    def set_ip(self, table, name, ip, owner):
        """Set "ip"" in "row" in table with "table" like ip
        row is a row which contain name in column "name"
                             and owner in column "owner" 
        """
        set_note = self.check_name(table, name, owner) 
        if not set_note[0]:
            return None
            
        set_note[1].ip = ip
        self.session.commit()
        
    def check_uuid(self, table, uuid_note):
        """DB.check_uuid(T, S) -> bool
        
        Return True if "S" is contain in database table "T" column "name", False othewise
        """
        for note_in_DB in self.session.query(table).filter(table.uuid_note == uuid_note):
            return (True, note_in_DB)
        return (False, None)

    def get_uuid(self, table, name, owner):
        """Get "uuid" from "row" in table with name "table"
        row is a row which contain name in column "name"
                             and owner in column "owner"         
        """
        get_note = self.check_name(table, name, owner)
        if get_note[0]:
            return (True, get_note[1].uuid_note)
        return (False, None)

    def get_stuff(self, table, owner):
        """Get rows from table with name"table"
        rows are containing owner in column "owner"         
        """
        owners_stuff = []
        for note_in_DB in self.session.query(table).filter(table.owner == owner):
            owners_stuff.append(note_in_DB.name)
        return owners_stuff