import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


class DBserver():
    """database class:
    support: VMtable, USERtable
    """
    def __init__(self, db_name, tables_base, detail = True):
        self.engine = sqlalchemy.create_engine('sqlite:///' + db_name, echo = detail)
        for table_base in tables_base:
            table_base.metadata.create_all(self.engine)
        Session = sqlalchemy.orm.sessionmaker(bind = self.engine)
        self.session = Session()
        
    def check_name(self, table, name):
        """DB.check_name(T, S) -> bool
        
        Return True if "S" is contain in database table "T" column "name", False othewise
        """
        for note_in_DB in self.session.query(table).filter(table.name == name):
            return (True, note_in_DB)
        return (False, None)

    def add(self, table, name, parameters):
        """DB.add(T, S, P) -> bool

        T [str] is a table name for addition
        S [str] will be added in column "name"
        P [turple] will be added in all other column 

        Return True if note hasn't already been added, False otherwise 
        """
        if self.check_name(table, name)[0]:
            return False
        new_note = table(name, parameters)
        self.session.add(new_note)
        self.session.commit()
        return True

    def delete(self, table, name):
        """DB.delete(name) -> bool
        
        name [str] is a existed note column "name"

        Return True if name is contained in database table "T" and was deleted successfuly,
               False if name isn't contained in database table "T",
               None if deletion was unsuccessful
        """
        delete_note = self.check_name(table, name)
        if not delete_note[0]:
            return False
        self.session.delete(delete_note[1])
        self.session.commit()
        return True

    def check_user(self, table, name, password):
        """Set "row"" in table "table" as active (column "active" = True)
        "row" is a row which contain name in column "name"
        """
        if not self.check_name(table, name)[0]:
            return None
            
        check_note = self.session.query(table).filter(table.name == name).one()
        return check_note.password == password 
            
    def set_active(self, table, name, active):
        """Set "active" in "row" in table with "table" like active
        row is a row which contain name in column "name"
        """
        if not self.check_name(table, name)[0]:
            return None
            
        set_note = self.session.query(table).filter(table.name == name).one()
        set_note.active = active
        self.session.commit()
        
    def set_ip(self, table, name, ip):
        """Set "ip"" in "row" in table with "table" like ip
        row is a row which contain name in column "name"
        """
        if not self.check_name(table, name)[0]:
            return None
            
        set_note = self.session.query(table).filter(table.name == name).one()
        set_note.ip = ip
        self.session.commit()
        
    def check_uuid(self, table, uuid_note):
        """DB.check_uuid(T, S) -> bool
        
        Return True if "S" is contain in database table "T" column "name", False othewise
        """
        for note_in_DB in self.session.query(table).filter(table.uuid_note == uuid_note):
            return (True, note_in_DB)
        return (False, None)

    def get_uuid(self, table, name, owner):
        for note_in_DB in self.session.query(table).filter(table.name == name, table.owner == owner):
            return (True, note_in_DB.uuid_note)
        return (False, None)
