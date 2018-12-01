import vlc


class Player:
    def __init__(self):
        """initialize a player and set a path for the file it will read"""
        self.instance = vlc.Instance()
        self.music_player = self.instance.media_list_player_new()
        self.media_list = self.instance.media_list_new([])
        self.music_player.set_media_list(self.media_list)

    def add_music(self, path):
        """add a music at the end of the current Playlist"""
        self.media_list.add_media(path)

    def add_musics(self, path_list):
        """add a group of musics at the end of the current Playlist"""
        for path in path_list:
            self.media_list.add_media(path)

    def play(self):
        """launch te player"""
        self.music_player.play()

    def set_volume(self, percentage):
        self.music_player.audio_set_volume(percentage)

    def need_recharge(self):
        return self.media_list.count() < 10
