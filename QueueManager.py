import SongChooser
import threading


class QueueManager(threading.Thread):
    def __init__(self, queue, database, player):
        """queue is a list of music_id in order to communicate with the main"""
        threading.Thread.__init__(self)
        self.queue = queue
        self.player = player
        self.song_chooser = SongChooser.SongChooser(database)
        queue.put(self.song_chooser.get_next_song())

    def run(self):
        """an infinite loop which add songs to the queue"""
        print("[RASP] start downloading")
        while True:
            if self.queue.qsize() < 10:
                new_id = self.song_chooser.get_next_song()
                self.queue.put(new_id)

            if self.song_chooser.need_to_play_now != 0:
                song_id = self.song_chooser.need_to_play_now
                self.queue.put(song_id)
                self.queue.put(song_id)  # add two times in order to detect hte end of the queue
                self.song_chooser.now_played()

                current_id = self.queue.get()
                while current_id != song_id:
                    current_id = self.queue.get()

                self.player.play_next_music()
