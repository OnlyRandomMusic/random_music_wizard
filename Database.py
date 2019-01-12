import sqlite3
import os


class Database:
    def __init__(self, database_name='database'):
        # self.connexion = sqlite3.connect(database_name + '.db')
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.database_name = self.dir_path + '/' + database_name + '.db'

    def sql_request(self, request, values=None):
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

    def create(self):
        try:
            self.sql_request('''CREATE TABLE music
                           (id, title_short, duration, preview_link, artist_id,
                            album_id, path, downloaded)''')

            # self.sql_request('''CREATE TABLE album
            #                 (id, genre_ids, artist_id)''')

            self.sql_request('''CREATE TABLE artist
                            (id, name)''')

            self.sql_request('''CREATE TABLE raw_playlist
                            (id, name)''')

            self.sql_request('''CREATE TABLE playlist_link
                            (playlist_id, music_id)''')
        except:
            print('[RASP] Database already created')

    def create_user(self, user_name):
        try:
            self.sql_request('''CREATE TABLE {}
                           (music_id, score)'''.format(user_name))
        except:
            print('[RASP] User already created')

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
                'SELECT name FROM music JOIN artist ON artist.id = artist_id WHERE music.id={}'.format(music_id))
        elif info_needed == 'artist_id':
            data = self.sql_request('SELECT artist_id FROM music WHERE id={}'.format(music_id))
        elif info_needed == 'title':
            data = self.sql_request('SELECT title_short FROM music WHERE id={}'.format(music_id))
        elif info_needed == 'path':
            data = self.sql_request('SELECT path FROM music WHERE id={}'.format(music_id))

        if data:
            return data[0][0]

    def song_downloaded(self, music_id, path):
        self.sql_request("""UPDATE music
SET downloaded = 1, path = "{}"
WHERE id = {}""".format(path, music_id))

    def add_raw_playlist(self, playlist):
        data = self.sql_request('SELECT * FROM raw_playlist WHERE id=?', (playlist['id'],))

        if data:
            print("[RASP] Playlist {} already in database".format(playlist['title']))
            return

        self.sql_request("INSERT INTO raw_playlist VALUES (?,?)", (
            playlist['id'], playlist['title']))

        for music in playlist['tracks']['data']:
            self.sql_request("INSERT INTO playlist_link VALUES (?,?)", (playlist['id'], music['id']))

        print("[RASP] Successfully added {} in database".format(playlist['title']))

    def print_data(self, table='music', attribute='*'):
        data = self.sql_request('SELECT {} FROM {}'.format(attribute, table))

        for element in data:
            print(element)

    def get_raw_playlist_max_id(self):
        data = self.sql_request('SELECT MAX(id) FROM raw_playlist')

        if data:
            if data[0][0] == None:
                return 0
            return data[0][0]

    def get_count(self, table):
        data = self.sql_request('SELECT COUNT(*) FROM {}'.format(table))

        if data:
            return data[0][0]

    def reset(self):
        self.sql_request('DROP TABLE IF EXISTS music')
        self.sql_request('DROP TABLE IF EXISTS album')
        self.sql_request('DROP TABLE IF EXISTS artist')
        # self.sql_request('DROP TABLE IF EXISTS raw_playlist')  # ATTENTION à ne pas décommenter
        # self.sql_request('DROP TABLE IF EXISTS playlist_link')  # ATTENTION à ne pas décommenter
