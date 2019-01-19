import requests_tools
import os
from random import random
import deezer_load
from database import UserDatabase
from database import PlaylistDatabase


class SongChooser:
    def __init__(self, music_database, player, user_name, song_quality="MP3_128"):
        """music_quality can be FLAC, MP3_320, MP3_256 or MP3_128"""
        # name of the current directory in order to save musics in the right place
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.musics_path = self.dir_path + os.sep + "musics"
        self.music_quality = song_quality
        self.music_database = music_database
        self.player = player
        mail, password = self.read_id()
        self.downloader = deezer_load.Login(mail, password)
        self.user_database = UserDatabase.UserDatabase(user_name)
        self.playlist_database = PlaylistDatabase.PlaylistDatabase()

        # to avoid making a lot of requests during the tests
        # self.starting_playlist = requests_tools.get_request("https://api.deezer.com/playlist/5164440904")  # playlist raspi
        self.starting_playlist = requests_tools.get_request(
            "https://api.deezer.com/playlist/1083721131")  # playlist au coin du feu

        self.deezer_user_id = 430225295
        self.deezer_user_data = requests_tools.get_request("https://api.deezer.com/user/" + str(self.deezer_user_id))
        self.deezer_flow = []

        self.need_to_put_first = 0
        self.play_when_placed = False

        self.mem_size = 4
        self.score_list = [0] * self.mem_size
        self.score_threshold = 0

        # for song in self.starting_playlist["tracks"]["data"]:
        #     self.music_database.add_song(song)

    def download_song(self, music_id):
        """download a song from a Deezer link in the musics directory
        and add the path to it in the database"""
        try:
            path = self.downloader.download_track(music_id, self.music_database, output=self.musics_path,
                                                  quality=self.music_quality)
            # check=False for not check if song already exist
            # recursive=False for download the song if quality selected doesn't exist
            # quality can be FLAC, MP3_320, MP3_256 or MP3_128
            self.music_database.song_downloaded(music_id, path)
            return True
        except:
            print("[RASP] error couldn't download " + self.music_database.get_music_info(music_id, 'title'))

    def get_random_from_playlist(self, link):
        """choose a random song in a playlist add it in the database and download it"""
        if link == -1:
            content = self.starting_playlist
        else:
            content = requests_tools.get_request(link)

        song_list = content["tracks"]["data"]
        success = False
        while not success:
            random_index = random.randint(0, len(song_list) - 1)
            random_song = song_list[random_index]
            success = self.download_song(random_song['id'])

        queue_data = random_song['id']
        return queue_data

    def increase_flow_buffer(self):
        """increase the size of the self.flow list"""
        while not self.deezer_flow:
            flow = requests_tools.get_request(self.deezer_user_data['tracklist'])
            self.deezer_flow = self.deezer_flow + [song['id'] for song in flow['data']]

            for song in flow["data"]:
                self.music_database.add_song(song)

    def get_next_in_flow(self):
        """return the next music in the flow"""
        success = False
        while not success:
            if not self.deezer_flow:
                self.increase_flow_buffer()

            next_music_id = self.deezer_flow.pop(0)
            success = self.download_song(next_music_id)

        return next_music_id

    def get_next_song(self):
        """return the next song to play must be completed"""
        # queue_data = self.get_next_in_flow()

        success = False
        while not success:
            next_music_id = self.choose_next_song()
            success = self.download_song(next_music_id)

        queue_data = next_music_id
        return queue_data

    def choose_next_song(self):
        self.score_list.pop(0)

        if self.user_database.get_count(self.user_database.current_user) == 0:
            music_id = self.choose_original_song()
            self.score_list.append(0)
        else:
            # in order that the average score is higher than the threshold
            score_min = self.mem_size * self.score_threshold - sum(self.score_list)
            music_id = self.user_database.get_random_song(score_min)

            if music_id == 'fail':
                # no song with this min score
                if random() > 0.5:
                    music_id = self.user_database.get_random_song()
                else:
                    music_id = self.choose_original_song()
                self.score_list.append(0)
            else:
                # a song has been found
                self.score_list.append(self.user_database.get_score(music_id))

        return music_id

    def choose_original_song(self):
        return self.playlist_database.get_really_random_song()

    def play_search(self, research, immediately):
        """play the researched song, immediately or after the current song"""
        results = requests_tools.get_request("https://api.deezer.com/search?q=" + research)
        try:
            song = results['data'][0]
            self.music_database.add_song(song)
            self.download_song(song['id'])
            self.put_first(song['id'])

            if immediately:
                self.play_when_placed = True
        except:
            print('No results found')

    def put_first(self, music_id):
        self.need_to_put_first = music_id

    def now_placed(self):
        self.need_to_put_first = 0
        if self.play_when_placed:
            self.player.play_next_music(0)
            self.play_when_placed = False

    def read_id(self):
        """read the id (mail and password) in the file identifiers.txt
        the file must look like that :
        YOUR_EMAIL
        YOUR_PASSWORD"""
        try:
            with open(self.dir_path + "/identifiers.txt", "r") as id_file:
                ids = id_file.readlines()
                mail = ids[0]
                password = ids[1]
                return mail, password
        except:
            print("[error] missing the file identifiers.txt or missing mail and password in this file")
