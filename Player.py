import vlc


class Player:
    def __init__(self, queue, music_database, score_update_queue):
        """initialize a player and set a path for the file it will read"""
        self.instance = vlc.Instance()
        self.music_player = self.instance.media_player_new()  # the class used to play the tracks
        self.set_volume(35)
        self.current_music_id = 0  # the id of the music played
        self.music_queue = queue
        self.music_database = music_database
        self.score_update_queue = score_update_queue

    def play_next_music(self, score):
        """play the selected music"""
        if self.music_queue.qsize() > 0:
            old_id = self.current_music_id
            self.current_music_id = self.music_queue.get()
            music_path = self.music_database.get_music_info(self.current_music_id, 'path')

            if music_path:
                song = self.instance.media_new(music_path)
                self.music_player.set_media(song)
                self.music_player.play()

                self.score_update_queue.put((old_id, score))

                return True
            else:
                self.current_music_id = old_id
                print("[PLAYER] music could not be found")
        return False

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
        # print(self.music_player.get_position())
        return self.music_player.get_position() > 0.995

    def play(self):
        if not self.music_player.is_playing():
            self.music_player.play()
            print("[PLAYER] music now playing")
        else:
            print("[PLAYER] music already playing")

    def pause(self):
        if self.music_player.is_playing():
            self.music_player.pause()
            print("[PLAYER] music now paused")
        else:
            print("[PLAYER] music already paused")
