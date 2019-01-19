import SongChooser
import threading


class QueueManager(threading.Thread):
    def __init__(self, queue, music_database, player, user_name):
        """queue is a list of music_id in order to communicate with the main"""
        threading.Thread.__init__(self)
        self.queue = queue
        self.player = player
        self.song_chooser = SongChooser.SongChooser(music_database, player, user_name)
        queue.put(self.song_chooser.get_next_song())

    def run(self):
        """an infinite loop which add songs to the queue"""
        print("[RASP] start downloading")
        while True:
            if self.queue.qsize() < 10:
                new_id = self.song_chooser.get_next_song()
                self.queue.put(new_id)

            if self.song_chooser.need_to_put_first != 0:
                self.put_first(self.song_chooser.need_to_put_first)
                self.song_chooser.now_placed()

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
