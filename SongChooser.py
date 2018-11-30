import utils
import os
import platform

OS_RASPBERRY = 'raspberrypi'

if platform.uname()[1] == OS_RASPBERRY:
    import deezloader


class SongChooser:
    def __init__(self, song_quality="MP3_256"):
        """music_quality can be FLAC, MP3_320, MP3_256 or MP3_128"""
        # name of the current directory in order to save musics in the right place
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.musics_path = self.dir_path + os.sep + "musics"
        self.music_quality = song_quality
        self.mail, self.password = utils.read_id()

    def download_song(self, link):
        """download a song from a Deezer link in the musics directory"""
        if platform.uname()[1] == OS_RASPBERRY:
            downloader = deezloader.Login(self.mail, self.password)
            downloader.download_trackdee(link, output=self.musics_path, check=False, quality=self.music_quality,
                                         recursive=True)
            # check=False for not check if song already exist
            # recursive=False for download the song if quality selected doesn't exist
            # quality can be FLAC, MP3_320, MP3_256 or MP3_128

        print("[RASP] download " + link)

    def get_new_song(self, song_data):
        """add a new song to the database and download it"""
        utils.record(song_data)
        link = song_data["link"]
        self.download_song(link)

    def get_new_playlist(self, link):
        """add each song of a playlist in the database and download them"""
        content = utils.get_request(link)
        song_list = content["tracks"]["data"]
        for song in song_list:
            self.get_new_song(song)

        paths = self.generate_path_list(song_list)
        return paths

    def get_test_playlist(self):
        """get the starting playlist for the rasp"""
        paths = self.get_new_playlist("https://api.deezer.com/playlist/5164440904")
        return paths

    def generate_path(self, song_data):
        title = song_data["title"]
        artist = song_data["artist"]["name"]
        path = "musics" + os.sep + artist + os.sep + artist + " " + title + ".mp3"

        return path

    def generate_path_list(self, songs_data):
        paths = []
        for song_data in songs_data:
            path = self.generate_path(song_data)
            paths.append(path)

        return paths
