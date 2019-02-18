import Explorer
import threading
from time import sleep


# Thread used to manage exploration of the database with the score updates
# its main goal is to explore in parallel in order not to block user instructions


class ExplorationManager(threading.Thread):
    def __init__(self, user_name, score_update_queue):
        threading.Thread.__init__(self)
        self.user_name = user_name
        self.explorer = Explorer.Explorer(user_name)
        self.score_update_queue = score_update_queue
        self.stop = False
        self.working = True

    def run(self):
        while True:
            if self.score_update_queue.qsize() > 0:
                score_update = self.score_update_queue.get()
                music_id, score = score_update
                self.explorer.set_score(music_id, score)
            else:
                sleep(0.5)

            if self.stop:
                break

        self.working = False
        print("[EXPLORATION MANAGER] stopped")
