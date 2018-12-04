import vlc


class Player:
    def __init__(self):
        """initialize a player and set a path for the file it will read"""
        self.instance = vlc.Instance()
        self.music_player = self.instance.media_player_new()  # the class used to play the tracks
        self.set_volume(60)
        self.current_music = 0  # the id of the music played

    def play_music(self, path):
        """play the selected music"""
        self.current_music = path
        song = self.instance.media_new(path)
        self.music_player.set_media(song)
        self.music_player.play()

    def set_volume(self, percentage):
        """set the player volume between 0 and 100"""
        self.music_player.audio_set_volume(percentage)

    def increase_volume(self, percentage):
        """increase the player volume (which is between 0 and 100), percentage can be negative"""
        current_vol = self.music_player.audio_get_volume()
        new_vol = current_vol + percentage
        if new_vol > 100:
            new_vol = 100
        elif new_vol < 0:
            new_vol = 0
        self.music_player.audio_set_volume(new_vol)
        return new_vol

    def music_ended(self):
        """called when the main detect that the song is finished"""
        return self.music_player.get_position() == 1.

    #def check_if_track_changed(self):
    #    real_current_media = self.music_player.get_media()
    #    print(self.current_media.tracks_get())
    #    if self.current_media != real_current_media:
    #        self.nb_media_played += 1
    #        self.current_media = real_current_media
