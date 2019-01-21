import sqlite3
import os


class Database:
    def __init__(self, database_name='database'):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.database_name = self.dir_path + '/' + database_name + '.db'
        self.connexion = False
        self.cursor = None

    def sql_request(self, request, values=None):
        """values is a tuple"""
        if not self.connexion:
            connexion = sqlite3.connect(self.database_name)
            cursor = connexion.cursor()

            if values:
                cursor.execute(request, values)
            else:
                cursor.execute(request)

            data = cursor.fetchall()
            connexion.commit()
            connexion.close()
        else:
            # print('fast')

            if values:
                self.cursor.execute(request, values)
            else:
                self.cursor.execute(request)

            data = self.cursor.fetchall()
            self.connexion.commit()

        return data

    def print_data(self, table, attribute='*'):
        data = self.sql_request('SELECT {} FROM {}'.format(attribute, table))

        for element in data:
            print(element)

    def get_count(self, table):
        data = self.sql_request('SELECT COUNT(*) FROM {}'.format(table))

        if data:
            return data[0][0]
        else:
            return 0

    def open_fast_connexion(self):
        """open a fast access connexion but needs to be close"""
        self.connexion = sqlite3.connect(self.database_name)
        self.cursor = self.connexion.cursor()

    def close_fast_connexion(self):
        try:
            self.connexion.close()
        except:
            print("error no connexion currently open")
        self.connexion = False
