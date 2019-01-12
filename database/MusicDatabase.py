from database import Database


class MusicDatabase(Database.Database):
    def __init__(self):
        # self.connexion = sqlite3.connect(database_name + '.db')
        Database.Database.__init__(self, "music_database")

    def create(self):
        try:
            self.sql_request('''CREATE TABLE music
                               (id, title_short, duration, preview_link, artist_id,
                                album_id, path, downloaded)''')

            self.sql_request('''CREATE TABLE artist
                                (id, name)''')
        except:
            print('[RASP] Music Database already created')

    def add_song(self, song, path=None, downloaded=0):
        data = self.sql_request('SELECT * FROM music WHERE id=?', (song['id'],))

        if data:
            print("[RASP] Song {} already in database".format(song['title_short']))
            return

        self.sql_request("INSERT INTO music VALUES (?,?,?,?,?,?,?,?)", (
            song['id'], song['title_short'], song['duration'], song['preview'],
            song['artist']['id'], song['album']['id'], path, downloaded))

        data = self.sql_request('SELECT * FROM artist WHERE id=?', (song['artist']['id'],))

        if not data:
            self.sql_request("INSERT INTO artist VALUES (?,?)", (song['artist']['id'], song['artist']['name']))

        print("[RASP] Successfully added {} in database".format(song['title_short']))

    def get_music_info(self, music_id, info_needed):
        # on utilise pas la connexion globale pour des problèmes de Thread
        data = None

        if info_needed == 'artist':
            data = self.sql_request(
                'SELECT name FROM music JOIN artist ON artist.id = artist_id WHERE music.id=?', (music_id,))
        elif info_needed == 'artist_id':
            data = self.sql_request('SELECT artist_id FROM music WHERE id=?', (music_id,))
        elif info_needed == 'title':
            data = self.sql_request('SELECT title_short FROM music WHERE id=?', (music_id,))
        elif info_needed == 'path':
            data = self.sql_request('SELECT path FROM music WHERE id=?', (music_id,))

        if data:
            return data[0][0]

    def song_downloaded(self, music_id, path):
        self.sql_request("""UPDATE music
SET downloaded = 1, path = "?"
WHERE id = ?""", (path, music_id))


m = MusicDatabase()
m.create()
