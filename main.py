import Player
import QueueManager
import queue
from time import sleep

print("[RASP] starting")

song_queue = queue.Queue()  # the queue used for receiving information from the song_chooser thread
instructions = queue.Queue()  # the the queue used for receiving information from the feedback_receiver thread

queue_manager = QueueManager.QueueManager(song_queue)  # creating a thread that will work in parallel
queue_manager.daemon = True  # when the main is closed this thread will also close

# feedback_receiver = (instructions)  # creating a thread that will work in parallel
# feedback_receiver.daemon = True  # when the main is closed this thread will also close

# feedback_receiver = FeedBackReceiver()
player = Player.Player()
sleep_time = 0.5

print("[RASP] vlc player initialized")


def load_music():
    global iterations_left
    new_path, duration = song_queue.get()
    iterations_left = duration / sleep_time  # WARNING the 0.1 is only for testing
    player.add_musics([new_path])


load_music()
player.play()

print("[RASP] starting to play")

queue_manager.start()

while True:
    iterations_left -= 1
    if iterations_left <= 0:
        player.music_ended()

    if song_queue.qsize() > 1 and player.need_recharge():
        load_music()

    # path, id_music = song_chooser.get_new_music()
    # player.add_music(path)
    # while len(queue>10):
    #    continue/wait

    # if feedback_receiver.feedback:
    #    agir en conséquence
    sleep(sleep_time)
    continue
