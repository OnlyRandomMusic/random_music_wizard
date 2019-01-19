from database import Database
from random import randint


class UserDatabase(Database.Database):
    def __init__(self, user_name):
        # self.connexion = sqlite3.connect(database_name + '.db')
        Database.Database.__init__(self, "user_database")
        self.current_user = user_name
        self.create_user(user_name)

    def create_user(self, user_name):
        try:
            self.sql_request('''CREATE TABLE {}
                           (address, music_id, score, has_been_played)'''.format(user_name))
        except:
            print('[RASP] User already created')

    def reset_music_played(self):
        self.open_fast_connexion()
        for address in range(self.get_count(self.current_user)):
            self.sql_request(
                """UPDATE {} SET has_been_played = {} WHERE address = ?""".format(self.current_user, 'FALSE'),
                (address,))

        self.close_fast_connexion()

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
            address = self.get_count(self.current_user)
            self.sql_request("INSERT INTO {} VALUES (?,?,?,?)".format(self.current_user),
                             (address, music_id, score_to_add, "'false'"))
        else:
            score += score_to_add
            self.sql_request("""UPDATE {} SET score = {} WHERE music_id = ?""".format(self.current_user, score),
                             (music_id,))

    def get_average_score(self):
        """return the average score of all musics in the user table"""
        data = self.sql_request('SELECT AVG(score) FROM {}'.format(self.current_user))
        if not data:
            return 0
        return data[0][0]

    def get_random_song(self, score_min='no'):
        """return a random song with a better score than score_min and return 'fail' if no songs fits"""
        if score_min == 'no':
            address_max = self.get_count(self.current_user) - 1
            address = randint(0, address_max)
            data = self.sql_request("SELECT music_id FROM {} WHERE address = {} AND has_been_played = 'false'".format(self.current_user, address))

            if not data:
                return 'fail'

            music_id = data[0][0]
        else:
            data = self.sql_request(
                "SELECT music_id FROM {} WHERE score >= {} AND has_been_played = 'false'".format(self.current_user, str(score_min)))

            if not data:
                return 'fail'

            index = randint(0, len(data) - 1)
            music_id = data[index][0]

        return music_id

    def has_been_played(self, music_id):
        self.sql_request("""UPDATE {} SET has_been_played = {} WHERE music_id = ?""".format(self.current_user, "'true'"),
                         (music_id,))


# d = UserDatabase('remi')
# d.update_score(12, 1)
# d.update_score(4, -1)
# d.update_score(12, 0.1)
# d.update_score(11, 0.5)
# d.update_score(11, -0.5)
# d.print_data('remi')
# print(d.get_average_score())
# print(d.get_random_song(20))
# print(d.get_random_song(0))
# print(d.get_random_song())
