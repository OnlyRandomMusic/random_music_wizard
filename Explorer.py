import requests_utils
import Database
from time import sleep
from random import randint


class Explorer:
    def __init__(self):
        self.database = Database.Database()

    def explore_related(self, music_id):
        artist_id = self.database.get_music_info(music_id, 'artist_id')

        # first step

    def playlist_brute_explore(self, n, m):
        """make requests to deezer about playlist between id = n and id = m"""
        identifier = n
        while True:
            try:
                data = requests_utils.get_request("playlist/" + str(identifier), True)
                if len(data['tracks']['data']) != 0:
                    self.database.add_raw_playlist(data)
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
                data = requests_utils.get_request("playlist/" + str(identifier), True)
                if len(data['tracks']['data']) != 0:
                    self.database.add_raw_playlist(data)
            except:
                print('fail')

    def playlist_moderate_explore(self, identifier=0, step_size=50, sleep_time=10):
        if identifier == 0:
            identifier = self.database.get_raw_playlist_max_id()

        while True:
            # self.playlist_brute_explore(identifier, identifier + step_size)
            # identifier += step_size
            # print(identifier)

            self.playlist_random_explore(step_size)

            sleep(sleep_time)


exp = Explorer()
exp.playlist_moderate_explore()
