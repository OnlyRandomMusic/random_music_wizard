import sqlite3
import os
from time import sleep


class Database:
    def __init__(self, database_name='database'):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.database_name = self.dir_path + '/' + database_name + '.db'
        self.connection = False
        self.cursor = None

    def sql_request(self, request, values=None):
        """values is a tuple"""
        if not self.connection:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()

            if values:
                cursor.execute(request, values)
            else:
                cursor.execute(request)

            data = cursor.fetchall()
            connection.commit()
            connection.close()
        else:
            # print('fast')

            if values:
                self.cursor.execute(request, values)
            else:
                self.cursor.execute(request)

            data = self.cursor.fetchall()
            self.connection.commit()

        return data

    def safe_sql_request(self, request, values=None):
        while True:
            try:
                data = self.sql_request(request, values)
                return data
            except:
                sleep(0.2)
                print('[DATABASE] SQL request error')

    def print_data(self, table, attribute='*'):
        data = self.safe_sql_request('SELECT {} FROM {}'.format(attribute, table))

        for element in data:
            print(element)

    def get_count(self, table):
        data = self.safe_sql_request('SELECT COUNT(*) FROM {}'.format(table))

        if data:
            return data[0][0]
        else:
            return 0

    def open_fast_connection(self):
        """open a fast access connection but needs to be close"""
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def close_fast_connection(self):
        try:
            self.connection.close()
        except:
            print("[DATABASE] error no fast connection currently open")
        self.connection = False
