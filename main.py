import Player
import QueueManager
import queue
from time import sleep
import FeedbackReceiver

print("[RASP] starting")

song_queue = queue.Queue()  # the queue used for receiving information from the song_chooser thread
# instructions = queue.Queue()  # the the queue used for receiving information from the feedback_receiver thread

queue_manager = QueueManager.QueueManager(song_queue)  # creating a thread that will work in parallel
queue_manager.daemon = True  # when the main is closed this thread will also close

player = Player.Player()  # initialize the music player
sleep_time = 0.2

feedback_receiver = FeedbackReceiver.FeedbackReceiver(player)  # creating a thread that will work in parallel
feedback_receiver.daemon = True  # when the main is closed this thread will also close

print("[RASP] vlc player initialized")

new_path = song_queue.get()
player.play_music(new_path)

print("[RASP] starting to play")

queue_manager.start()
feedback_receiver.start()

while True:
    if song_queue.qsize() > 1 and player.music_ended():
        new_path = song_queue.get()
        player.play_music(new_path)

    # path, id_music = song_chooser.get_new_music()
    # player.add_music(path)
    # while len(queue>10):
    #    continue/wait

    # if feedback_receiver.feedback:
    #    agir en conséquence
    sleep(sleep_time)
    continue
