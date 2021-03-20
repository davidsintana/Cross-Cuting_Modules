# Imports ============================================================================================================ #
import sqlite3
from sqlite3 import Error

import importlib.util
spec = importlib.util.spec_from_file_location("UtilityLibrary.py", r"D:\Python\Central\UtilityLibrary.py")
util = importlib.util.module_from_spec(spec)
spec.loader.exec_module(util)

# ==================================================================================================================== #


class DataBase:

    def __init__(self, _db_path, _log_file_object):
        # Initializes an DB Object
        # Input: Complete Path of the DB
        # Input: List of DataBaseTable Objects
        # Input: Path of Logfile
        # Exception: ConnectionError = Database could not be found

        self.log_file = _log_file_object

        try:
            self.connection_object = sqlite3.connect(_db_path)

        except Error as error:
            self.log_file.write(error)
            raise ConnectionError

        else:
            self.cursor = self.connection_object.cursor()

    def create_table(self, _database_table_object):
        query = "CREATE TABLE IF NOT EXISTS " + _database_table_object.name + "("
        first_attribute = True

        for attribute in _database_table_object.attributes:

            if first_attribute is True:
                query += attribute
                first_attribute = False

            else:
                query += "," + attribute

        query += ");"
        self.log_file.write("Execute=" + query)

        try:
            self.cursor.execute(query)
            self.log_file.write("Query=" + query + " successfully executed")

        except Error as error:
            self.log_file.write(error)


class DataBaseTable(DataBase):
    # Initializes an SQL Table Object
    # SUPPOSITION: Index is equal to a 0:n length of the values.

    def __init__(self, _name, _attributes, _primary_index, _db_path, _log_file_path):
        super().__init__(_db_path, _log_file_path)

        self.name = str(_name)
        self.attributes = list(_attributes)
        self.primary_index = list(_primary_index)

        self.create_table(self)

    def insert(self, _entry_values):
        query = "INSERT INTO " + self.name + " ("
        attribute_is_first = True

        for attribute in self.attributes:

            if attribute_is_first:
                query += attribute
                attribute_is_first = False

            else:
                query += "," + attribute

        query += ") VALUES "

        value_is_first = True
        for value in _entry_values:

            if value_is_first:
                query += "(?"
                value_is_first = False

            else:
                query += ", ?"

        query += ")"
        self.log_file.write("Execute=" + query)
        self.cursor.execute(query, _entry_values)
        self.connection_object.commit()

        return self.cursor.lastrowid

    def update(self, _entry_values):

        query = "UPDATE " + self.name + " SET "
        is_first_attribute = True

        for attribute in self.attributes:

            if is_first_attribute:
                query += attribute + " = ?"
                is_first_attribute = False

            else:
                query += "," + attribute + "= ?"

        query += " WHERE "

        is_first_attribute = True
        for attribute in self.primary_index:

            if is_first_attribute:
                query += attribute + " = ? "

            else:
                query += "and " + attribute + " = ? "

        self.log_file.write("Execute=" + query)

        entry_index_values = _entry_values[0:len(self.primary_index)]
        list_of_values = _entry_values + entry_index_values
        self.log_file.write("Values=" + str(list_of_values))
        self.cursor.execute(query, list_of_values)
        self.connection_object.commit()

        return self.cursor.lastrowid

    def select(self, _index_values):
        # Functionality: Selects an entry based on its primary index
        # Input: Index values of the entry
        # Output: Tuple or None

        query = "SELECT * FROM " + self.name + " WHERE "
        is_first = True

        for attribute in self.primary_index:

            if is_first:
                query += attribute + " = ?"
                is_first = False

            else:
                query += " and " + attribute + " = ?"

        self.log_file.write("Execute=" + query)
        self.cursor.execute(query, _index_values)
        entry = self.cursor.fetchone()

        return entry

    def select_all(self):
        # Functionality: Delivers a List with all entries found as tuples
        # Output: List of Tuples (Entries)
        query = "SELECT * FROM " + self.name
        self.cursor.execute(query)
        entries = self.cursor.fetchall()

    def insert_or_update(self, _entry_values):
        # Functionality: Inserts or Updates depending on its existence
        # Input: Entry values
        # Output: ID of created/updated entry
        index_values = _entry_values[0:len(self.primary_index)]
        entry = self.select(index_values)

        if entry is None:
            entry_id = self.insert(_entry_values)
            self.log_file.write("Entry with index=" + str(index_values) + " not found, will be inserted")

        else:
            entry_id = self.update(_entry_values)
            self.log_file.write("Entry with index=" + str(index_values) + " exists, will be updated")

        return entry_id
