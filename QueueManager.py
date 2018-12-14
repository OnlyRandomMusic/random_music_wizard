import SongChooser
import threading


class QueueManager(threading.Thread):
    def __init__(self, queue, database):
        """queue is a list of music_id in order to communicate with the main"""
        threading.Thread.__init__(self)
        self.queue = queue
        self.song_chooser = SongChooser.SongChooser(database)
        queue.put(self.song_chooser.get_start_song())

    def run(self):
        """an infinite loop which add songs to the queue"""
        print("[RASP] start downloading")
        while True:
            if self.queue.qsize() < 10:
                new_path = self.song_chooser.get_next_song()
                self.queue.put(new_path)
