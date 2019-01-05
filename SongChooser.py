import utils
import os
import random
import deezer_load


class SongChooser:
    def __init__(self, database, song_quality="MP3_128"):
        """music_quality can be FLAC, MP3_320, MP3_256 or MP3_128"""
        # name of the current directory in order to save musics in the right place
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        print(self.dir_path)
        self.musics_path = self.dir_path + os.sep + "musics"
        self.music_quality = song_quality
        self.database = database
        mail, password = utils.read_id()
        self.downloader = deezer_load.Login(mail, password)

        # to avoid making a lot of requests during the tests
        # self.starting_playlist = utils.get_request("https://api.deezer.com/playlist/5164440904")  # playlist raspi
        self.starting_playlist = utils.get_request(
            "https://api.deezer.com/playlist/1083721131")  # playlist au coin du feu

        self.user_id = 430225295
        self.user_data = utils.get_request("https://api.deezer.com/user/" + str(self.user_id))
        self.flow = []

        self.need_to_play_now = False

        for song in self.starting_playlist["tracks"]["data"]:
            self.database.add_song(song)

    def download_song(self, music_id):
        """download a song from a Deezer link in the musics directory
        and add the path to it in the database"""
        try:
            path = self.downloader.download_track(music_id, self.database, output=self.musics_path,
                                                  quality=self.music_quality)
            # check=False for not check if song already exist
            # recursive=False for download the song if quality selected doesn't exist
            # quality can be FLAC, MP3_320, MP3_256 or MP3_128
            self.database.song_downloaded(music_id, path)
            return True
        except:
            print("[RASP] error couldn't download " + self.database.get_music_info(music_id, 'title'))

    def get_random_from_playlist(self, link):
        """choose a random song in a playlist add it in the database and download it"""
        if link == -1:
            content = self.starting_playlist
        else:
            content = utils.get_request(link)

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
        while not self.flow:
            flow = utils.get_request(self.user_data['tracklist'])
            self.flow = self.flow + [song['id'] for song in flow['data']]

            for song in flow["data"]:
                self.database.add_song(song)

    def get_next_in_flow(self):
        """return the next music in the flow"""
        success = False
        while not success:
            if not self.flow:
                self.increase_flow_buffer()

            next_music_id = self.flow.pop(0)
            success = self.download_song(next_music_id)

        return next_music_id

    def get_next_song(self):
        """return the next song to play must be completed"""
        # queue_data = self.get_random_from_playlist(-1)
        queue_data = self.get_next_in_flow()
        return queue_data

    def play_search(self, research):
        """play the researched song"""
        results = utils.get_request("https://api.deezer.com/search?q=" + research)
        try:
            song = results['data'][0]
            self.database.add_song(song)
            self.download_song(song['id'])
            self.play_now(song['id'])
        except:
            print('No results found')

    def play_now(self, music_id):
        self.need_to_play_now = music_id

    def now_played(self):
        self.need_to_play_now = 0

    def read_id(self):
        """read the id (mail and password) in the file identifiers.txt
        the file must look like that :
        YOUR_EMAIL
        YOUR_PASSWORD"""
        print(self.dir_path + "/identifiers.txt")
        try:
            with open(self.dir_path + "/identifiers.txt", "r") as id_file:
                ids = id_file.readlines()
                mail = ids[0]
                password = ids[1]
                return mail, password
        except:
            print("[error] missing the file identifiers.txt or missing mail and password in this file")


