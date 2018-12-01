import Player
import QueueManager
import queue
from time import sleep

print("[RASP] starting")

song_queue = queue.Queue()  # the queue used for receiving information from the song_chooser thread
instructions = queue.Queue()  # the the queue used for receiving information from the feedback_receiver thread

queue_manager = QueueManager.QueueManager(song_queue)  # creating a thread that will work in parallel
queue_manager.daemon = True  # when the main is closed this thread will also close

#feedback_receiver = (instructions)  # creating a thread that will work in parallel
#feedback_receiver.daemon = True  # when the main is closed this thread will also close

# feedback_receiver = FeedBackReceiver()
player = Player.Player()

print("[RASP] vlc player initialized")

new_path = song_queue.get()
player.add_musics([new_path])
player.play()

print("[RASP] starting to play")

queue_manager.start()

while True:
    if song_queue.qsize() > 1 and player.need_recharge():
        new_path = song_queue.get()
        player.add_music(new_path)

    # path, id_music = song_chooser.get_new_music()
    # player.add_music(path)
    # while len(queue>10):
    #    continue/wait

    # if feedback_receiver.feedback:
    #    agir en conséquence
    sleep(3)
    continue



