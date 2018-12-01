import utils
import os
import platform
import random

OS_RASPBERRY = 'raspberrypi'

if platform.uname()[1] == OS_RASPBERRY:
    import deezloader


class SongChooser:
    def __init__(self, song_quality="MP3_128"):
        """music_quality can be FLAC, MP3_320, MP3_256 or MP3_128"""
        # name of the current directory in order to save musics in the right place
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.musics_path = self.dir_path + os.sep + "musics"
        self.music_quality = song_quality
        mail, password = utils.read_id()
        if platform.uname()[1] == OS_RASPBERRY:
            self.downloader = deezloader.Login(mail, password)

    def download_song(self, link):
        """download a song from a Deezer link in the musics directory
        return True if an error occurred"""
        if platform.uname()[1] == OS_RASPBERRY:
            try:
                self.downloader.download_trackdee(link, output=self.musics_path, check=False, quality=self.music_quality,
                                             recursive=True)
                # check=False for not check if song already exist
                # recursive=False for download the song if quality selected doesn't exist
                # quality can be FLAC, MP3_320, MP3_256 or MP3_128
            except:
                print("[RASP] error couldn't download " + link)
                return True

        # print("[RASP] download " + link)

    def get_new_song(self, song_data):
        """add a new song to the database and download it"""
        link = song_data["link"]
        # print("[RASP] downloading song " + link)
        error = self.download_song(link)
        if not error:
            utils.record(song_data)

    def get_new_playlist(self, link):
        """add each song of a playlist in the database and download them"""
        # print("[RASP] downloading playlist " + link)
        content = utils.get_request(link)
        song_list = content["tracks"]["data"]
        for song in song_list:
            self.get_new_song(song)

        paths = self.generate_path_list(song_list)
        return paths

    def get_random_from_playlist(self, link):
        """choose a random song in a playlist add it in the database and download it"""
        content = utils.get_request(link)
        song_list = content["tracks"]["data"]
        random_index = random.randint(0, len(song_list) - 1)
        random_song = song_list[random_index]
        self.get_new_song(random_song)

        path = self.generate_path(random_song)
        return path

    def get_test_playlist(self):
        """get the testing playlist for the rasp"""
        paths = self.get_new_playlist("https://api.deezer.com/playlist/5164440904")
        return paths

    def get_start_song(self):
        """get the starting song for the rasp"""
        path = self.get_random_from_playlist("https://api.deezer.com/playlist/5164440904")
        return path

    def generate_path(self, song_data):
        title = song_data["title"]
        artist = song_data["artist"]["name"]
        path = "musics" + os.sep + artist + os.sep + artist + " " + title + ".mp3"
        print("[RASP] downloaded song " + title)
        return path

    def generate_path_list(self, songs_data):
        paths = []
        for song_data in songs_data:
            path = self.generate_path(song_data)
            paths.append(path)

        return paths

    def get_next_song(self):
        """return the next song to play must be completed"""
        path = self.get_random_from_playlist("https://api.deezer.com/playlist/5164440904")
        return path
