import requests_tools
from database import MusicDatabase
from database import PlaylistDatabase
from database import UserDatabase
from time import sleep
from random import randint


class Explorer:
    def __init__(self, user_database):
        self.music_database = MusicDatabase.MusicDatabase()
        self.playlist_database = PlaylistDatabase.PlaylistDatabase()
        self.user_database = user_database

    def set_score(self, music_id, score):
        artist_id = self.music_database.get_music_info(music_id, 'artist_id')
        self.user_database.update_score(music_id, score)
        song_updated = [music_id]

        # first step
        songs_of_artist = requests_tools.songs_of_artist(artist_id)

        if songs_of_artist:
            for song in songs_of_artist:
                if not song['id'] in song_updated:
                    self.user_database.update_score(song['id'], score*0.5)
                    song_updated.append(song['id'])

            # second step
            collaborators = requests_tools.collaboration(artist_id, songs_of_artist)

            if collaborators:
                for collaborator in collaborators:
                    songs_of_collaborator = requests_tools.songs_of_artist(collaborator, 10)
                    for song in songs_of_collaborator:
                        if not song['id'] in song_updated:
                            self.user_database.update_score(song['id'], score*0.1)
                            song_updated.append(song['id'])

        # third step
        # playlist search

    def playlist_brute_explore(self, n, m):
        """make requests to deezer about playlist between id = n and id = m"""
        identifier = n
        while True:
            try:
                data = requests_tools.get_request("playlist/" + str(identifier), True)
                if len(data['tracks']['data']) != 0:
                    self.playlist_database.add_raw_playlist(data)
            except:
                print('fail')

            identifier += 1
            if identifier > m:
                break

    def playlist_random_explore(self, n):
        """make requests to deezer about playlist randomly"""
        for _ in range(n):
            identifier = randint(10000, 2000000000)

            try:
                data = requests_tools.get_request("playlist/" + str(identifier), True)
                if len(data['tracks']['data']) != 0:
                    self.playlist_database.add_raw_playlist(data)
            except:
                print('fail')

    def playlist_moderate_explore(self, identifier=0, step_size=50, sleep_time=10):
        if identifier == 0:
            identifier = self.playlist_database.get_raw_playlist_max_id()

        while True:
            # self.playlist_brute_explore(identifier, identifier + step_size)
            # identifier += step_size
            # print(identifier)

            self.playlist_random_explore(step_size)

            sleep(sleep_time)


# m = MusicDatabase.MusicDatabase()
# d = UserDatabase.UserDatabase('remi')
# exp = Explorer(d)
# song = requests_tools.get_request('https://api.deezer.com/track/94935172')
# m.add_song(song)
# exp.set_score(94935172, 1)
# d.print_data('remi')
