import sqlite3


class Database:
    def __init__(self, database_name='database'):
        self.connexion = sqlite3.connect(database_name + '.db')

    def create(self):
        cursor = self.connexion.cursor()

        try:
            cursor.execute('''CREATE TABLE music
                           (id, title_short, link, duration, preview_link, artist_id,
                            album_id, path, downloaded)''')

            # cursor.execute('''CREATE TABLE album
            #                 (id, genre_ids, artist_id)''')
            #
            cursor.execute('''CREATE TABLE artist
                            (id, name)''')
        except:
            print('[RASP] Database already created')

        self.connexion.commit()

    def add_song(self, song, path=None, downloaded=0):
        cursor = self.connexion.cursor()

        cursor.execute('SELECT * FROM music WHERE id=?', (song['id'],))

        if cursor.fetchone():
            print("[RASP] Song {} already in database".format(song['title_short']))
            return

        print(song.keys())
        cursor.execute("INSERT INTO music VALUES (?,?,?,?,?,?,?,?,?)", (
            song['id'], song['title_short'], song['link'], song['duration'], song['preview'],
            song['artist']['id'], song['album']['id'], path, downloaded))

        cursor.execute('SELECT * FROM artist WHERE id=?', (song['artist']['id'],))

        if not cursor.fetchone():
            cursor.execute("INSERT INTO artist VALUES (?,?)", (song['artist']['id'], song['artist']['name']))

        self.connexion.commit()
        print("[RASP] Successfully added {} in database".format(song['title_short']))

    def get_music_info(self, music_id, info_needed):
        cursor = self.connexion.cursor()
        if info_needed == 'artist':
            cursor.execute(
                'SELECT name FROM music JOIN artist ON artist.id = artist_id WHERE music.id={}'.format(music_id))
        elif info_needed == 'title':
            cursor.execute('SELECT title_short FROM music WHERE id={}'.format(music_id))
        elif info_needed == 'path':
            cursor.execute('SELECT path FROM music WHERE id={}'.format(music_id))

        data = cursor.fetchone()[0]
        return data

    def song_downloaded(self, music_id, path):
        cursor = self.connexion.cursor()
        cursor.execute("""UPDATE music
SET downloaded = 1, path = '{}'
WHERE id = {}""".format(path, music_id))

    def print_data(self, table='music', attribute='*'):
        cursor = self.connexion.cursor()
        cursor.execute('SELECT {} FROM {}'.format(attribute, table))
        data = cursor.fetchall()

        for element in data:
            print(element)

    def reset(self):
        cursor = self.connexion.cursor()
        cursor.execute('DROP TABLE IF EXISTS music')
        cursor.execute('DROP TABLE IF EXISTS album')
        cursor.execute('DROP TABLE IF EXISTS artist')
        self.connexion.commit()

    def close(self):
        self.connexion.close()
