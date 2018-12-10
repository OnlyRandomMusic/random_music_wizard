import sqlite3


class Database:
    def __init__(self, database_name='database'):
        self.connexion = sqlite3.connect(database_name + '.db')

    def create(self):
        cursor = self.connexion.cursor()

        try:
            cursor.execute('''CREATE TABLE music
                           (id, title_short, link, duration, r_date, preview_link, bpm, gain, artist_id,
                            album_id, path, downloaded)''')

            # cursor.execute('''CREATE TABLE album
            #                 (id, genre_ids, artist_id)''')
            #
            cursor.execute('''CREATE TABLE artist
                            (id, name)''')
        except:
            print('base de donnée déja créée')

        self.connexion.commit()

    def add_song(self, song, path=None, downloaded=False):
        cursor = self.connexion.cursor()

        cursor.execute('SELECT * FROM music WHERE id=?', (song['id'],))

        if cursor.fetchone():
            print("[RASP] Song {} already in database".format(song['title_short']))
            return

        cursor.execute("INSERT INTO music VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
            song['id'], song['title_short'], song['link'], song['duration'], song['release_date'], song['preview'],
            song['bpm'], song['gain'], song['artist']['id'], song['album']['id'], path, downloaded))

        cursor.execute('SELECT * FROM artist WHERE id=?', (song['artist']['id'],))

        if not cursor.fetchone():
            cursor.execute("INSERT INTO artist VALUES (?,?)", (song['artist']['id'], song['artist']['name']))

        self.connexion.commit()
        print("[RASP] Successfully added {} in database".format(song['title_short']))

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
