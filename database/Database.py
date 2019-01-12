import sqlite3
import os


class Database:
    def __init__(self, database_name='database'):
        # self.connexion = sqlite3.connect(database_name + '.db')
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.database_name = self.dir_path + '/' + database_name + '.db'

    def sql_request(self, request, values=None):
        """values is a tuple"""
        connexion = sqlite3.connect(self.database_name)
        cursor = connexion.cursor()
        if values:
            cursor.execute(request, values)
        else:
            cursor.execute(request)
        data = cursor.fetchall()
        connexion.commit()
        connexion.close()
        return data

    def create_table(self, table_name, attributes):
        """create a table with the given attributes (as a tuple)"""
        try:
            self.sql_request('''CREATE TABLE ?
                           (''' + '?,'*(len(attributes)-1) + '?)', attributes)
            print('''CREATE TABLE ?
                           (''' + '?,'*(len(attributes)-1) + '?)')
            print(tuple(attributes))
        except:
            print('[RASP] Table {} already created'.format(table_name))

    def print_data(self, table, attribute='*'):
        data = self.sql_request('SELECT ? FROM ?', (attribute, table))

        for element in data:
            print(element)
