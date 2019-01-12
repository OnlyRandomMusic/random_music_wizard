from database import Database


class UserDatabase(Database.Database):
    def __init__(self):
        # self.connexion = sqlite3.connect(database_name + '.db')
        Database.Database.__init__(self, "user_database")

    def create_user(self, user_name):
        try:
            self.sql_request('''CREATE TABLE {}
                           (music_id, score)'''.format(user_name))
        except:
            print('[RASP] User already created')


