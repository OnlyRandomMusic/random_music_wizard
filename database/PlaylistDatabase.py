from database import Database
from random import randint


class PlaylistDatabase(Database.Database):
    def __init__(self):
        # self.connexion = sqlite3.connect(database_name + '.db')
        Database.Database.__init__(self, "playlist_database")

    def create(self):
        try:
            self.sql_request('''CREATE TABLE raw_playlist
                            (address, id, name)''')

            # WARNING playlist_id is address and not the real playlist_id
            self.sql_request('''CREATE TABLE playlist_link
                            (playlist_id, music_id)''')
        except:
            print('[RASP] Playlist Database already created')

    def add_raw_playlist(self, playlist):
        data = self.sql_request('SELECT * FROM raw_playlist WHERE id=?', (playlist['id'],))

        if data:
            print("[RASP] Playlist {} already in database".format(playlist['title']))
            return

        address = self.get_count('raw_playlist')
        self.sql_request("INSERT INTO raw_playlist VALUES (?,?,?)", (
            address, playlist['id'], playlist['title']))

        for music in playlist['tracks']['data']:
            self.sql_request("INSERT INTO playlist_link VALUES (?,?)", (address, music['id']))

        print("[RASP] Successfully added {} in database".format(playlist['title']))

    def get_raw_playlist_max_id(self):
        data = self.sql_request('SELECT MAX(id) FROM raw_playlist')

        if data:
            if data[0][0] == None:
                return 0
            return data[0][0]

    def get_really_random_song(self):
        address_max = self.get_count("raw_playlist")-1
        address = randint(0, address_max)
        data = self.sql_request(
            'SELECT music_id FROM playlist_link WHERE playlist_id = {}'.format(str(address)))

        # print(data)
        index = randint(0, len(data) - 1)
        return data[index][0]


# d = PlaylistDatabase()
# print(d.get_count('playlist_link'))
# data = d.sql_request("SELECT music_id FROM playlist_link")
# music_ids = [elem[0] for elem in data]
# print(len(list(set(music_ids))))
# d.print_data('raw_playlist')
# print(d.get_really_random_song())
