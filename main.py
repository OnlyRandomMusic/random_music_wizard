import Player
import QueueManager
import queue
import Database
from time import sleep
import FeedbackReceiver

print("[RASP] starting")

database = Database.Database()
# database.reset()
database.create()

song_queue = queue.Queue()  # the queue used for receiving information from the song_chooser thread

queue_manager = QueueManager.QueueManager(song_queue, database)  # creating a thread that will work in parallel
queue_manager.daemon = True  # when the main is closed this thread will also close

player = Player.Player(song_queue, database)  # initialize the music player
sleep_time = 0.5

feedback_receiver = FeedbackReceiver.FeedbackReceiver(player)  # creating a thread that will work in parallel
feedback_receiver.daemon = True  # when the main is closed this thread will also close

print("[RASP] vlc player initialized")

player.play_next_music()

print("[RASP] starting to play")

queue_manager.start()
feedback_receiver.start()

while True:
    if player.music_ended():
        player.play_next_music()

    if feedback_receiver.stop:
        break

    sleep(sleep_time)
    continue
