from database import Database


class UserDatabase(Database.Database):
    def __init__(self, user_name):
        # self.connexion = sqlite3.connect(database_name + '.db')
        Database.Database.__init__(self, "user_database")
        self.current_user = user_name
        self.create_user(user_name)

    def create_user(self, user_name):
        try:
            self.sql_request('''CREATE TABLE {}
                           (music_id, score)'''.format(user_name))
        except:
            print('[RASP] User already created')

    def get_score(self, music_id):
        """return the score of a given music or 'not found' if it isn't in the table"""
        data = self.sql_request('SELECT score FROM {} WHERE music_id={}'.format(self.current_user, music_id))
        if not data:
            return 'not found'
        return data[0][0]

    def update_score(self, music_id, score_to_add):
        """update the score of a song or add it to the user table"""
        score = self.get_score(music_id)

        if score == 'not found':
            # attention injection SQL possible à ce niveau
            self.sql_request("INSERT INTO {} VALUES (?,?)".format(self.current_user), (music_id, score_to_add))
        else:
            score += score_to_add
            self.sql_request("""UPDATE {} SET score = {} WHERE music_id = ?""".format(self.current_user, score),
                             (music_id,))

# d = UserDatabase('remi')
# d.update_score(12,1)
# d.update_score(4,-1)
# d.update_score(12,0.1)
# d.update_score(11,0.5)
# d.update_score(11,-0.5)
# d.print_data('remi')
