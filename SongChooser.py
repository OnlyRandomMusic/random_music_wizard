import utils
import os
import random
import deezer_load


class SongChooser:
    def __init__(self, database, song_quality="MP3_128"):
        """music_quality can be FLAC, MP3_320, MP3_256 or MP3_128"""
        # name of the current directory in order to save musics in the right place
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.musics_path = self.dir_path + os.sep + "musics"
        self.music_quality = song_quality
        self.database = database
        mail, password = utils.read_id()
        self.downloader = deezer_load.Login(mail, password)

        # to avoid making a lot of requests during the tests
        # self.starting_playlist = utils.get_request("https://api.deezer.com/playlist/5164440904")  # playlist raspi
        self.starting_playlist = utils.get_request("https://api.deezer.com/playlist/1083721131")  # playlist au coin du feu

        for song in self.starting_playlist["tracks"]["data"]:
            self.database.add_song(song)

    def download_song(self, music_id):
        """download a song from a Deezer link in the musics directory
        and return the path to it"""
        try:
            path = self.downloader.download_track(music_id, self.database, output=self.musics_path, quality=self.music_quality)
            # check=False for not check if song already exist
            # recursive=False for download the song if quality selected doesn't exist
            # quality can be FLAC, MP3_320, MP3_256 or MP3_128
            return path
        except:
            print("[RASP] error couldn't download " + self.database.get_music_info(music_id, 'title'))

    def get_new_song(self, song_data):
        """add a new song to the database and download it
        return True if no error occurs"""
        # self.database.add_song(song_data)
        path = self.download_song(song_data['id'])
        if path:
            self.database.song_downloaded(song_data['id'], path)
            return True

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
            success = self.get_new_song(random_song)

        queue_data = random_song['id']
        return queue_data

    def get_start_song(self):
        """get the starting song for the rasp"""
        queue_data = self.get_random_from_playlist(-1)
        return queue_data

    def get_next_song(self):
        """return the next song to play must be completed"""
        queue_data = self.get_random_from_playlist(-1)
        return queue_data
