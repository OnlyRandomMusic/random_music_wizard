import SongChooser
import threading
from time import sleep


class QueueManager(threading.Thread):
    def __init__(self, queue, music_database, player, user_name, score_update_queue, mode):
        """queue is a list of music_id in order to communicate with the main"""
        threading.Thread.__init__(self)
        self.queue = queue
        self.player = player
        self.score_update_queue = score_update_queue
        self.song_chooser = SongChooser.SongChooser(music_database, player, user_name, mode)
        self.stop = False
        self.working = True
        self.need_to_search = None

        queue.put(self.song_chooser.get_next_song())

    def run(self):
        """an infinite loop which add songs to the queue"""
        print("[QUEUE MANAGER] start downloading")
        while True:
            if self.need_to_search:
                research, immediately, from_feedback = self.need_to_search
                song_id = self.song_chooser.play_search(research)

                if song_id:
                    self.put_first(song_id)
                    self.score_update_queue.put((song_id, 0.5))
                    if immediately:
                        self.player.play_next_music(0)

            if self.queue.qsize() < 10:
                new_id = self.song_chooser.get_next_song()
                self.queue.put(new_id)
            else:
                sleep(0.5)

            if self.stop:
                break

        self.working = False
        print("[QUEUE MANAGER] stopped")

    def put_first(self, song_id):
        """function used to put a song at the beginning of the queue"""
        self.queue.put(song_id)
        self.queue.put(song_id)  # add two times in order to detect the end of the queue

        current_id = self.queue.get()
        old_ids = []  # list of old ids in order to place them in the queue again after the manipulation
        while current_id != song_id:
            old_ids.append(current_id)
            current_id = self.queue.get()  # the last id is not added to old_ids because it is the song_id

        for old_id in old_ids:
            self.queue.put(old_id)

    def make_search(self, research, immediately, from_feedback=False):
        self.need_to_search = (research, immediately, from_feedback)
