import vlc


class Player:
    def __init__(self):
        """initialize a player and set a path for the file it will read"""
        self.instance = vlc.Instance()
        self.music_list_player = self.instance.media_list_player_new()  # the class used to play list of tracks
        # self.music_player = self.music_list_player.get_media_player()  # the MediaPlayer object used in music_list_player
        self.media_list = self.instance.media_list_new([])  # the playlist that we will be using
        self.music_list_player.set_media_list(self.media_list)  # assign the media_list to the media_player_list
        # self.current_media = self.music_player.get_media()  # variable used to detect when the music change
        self.nb_media_played = 1  # number of tracks already played

    def add_music(self, path):
        """add a music at the end of the current Playlist"""
        self.media_list.add_media(path)

    def add_musics(self, path_list):
        """add a group of musics at the end of the current Playlist"""
        for path in path_list:
            self.media_list.add_media(path)

    def play(self):
        """launch te player"""
        self.music_list_player.play()

    def next_music(self):
        """pass to the next music (never tested)"""
        print("[RASP] pass to the next music")
        self.music_list_player.next()

    def set_volume(self, percentage):
        self.music_list_player.audio_set_volume(percentage)

    def need_recharge(self):
        """doesn't work because media_list size isn't changed when a music is finished"""
        return self.media_list.count() - self.nb_media_played < 10

    def music_ended(self):
        self.nb_media_played += 1
        print("[RASP] music ended")

    #def check_if_track_changed(self):
    #    real_current_media = self.music_player.get_media()
    #    print(self.current_media.tracks_get())
    #    if self.current_media != real_current_media:
    #        self.nb_media_played += 1
    #        self.current_media = real_current_media
