#! /usr/bin/env python3

# line to add in rc.local to start on boot:
# su rengati -c "python3 home/rengati/random_music_wizard/main.py &"

import Player
import QueueManager
import queue
from database import MusicDatabase
import Explorer
from time import sleep
import FeedbackReceiver

print("[RASP] starting")

feedback_receiver = FeedbackReceiver.FeedbackReceiver()  # creating a thread that will work in parallel
feedback_receiver.daemon = True  # when the main is closed this thread will also close
feedback_receiver.start()

while not feedback_receiver.user_name:
    sleep(1)

user_name = feedback_receiver.user_name

music_database = MusicDatabase.MusicDatabase()
music_database.create()

explorer = Explorer.Explorer(user_name)

song_queue = queue.Queue()  # the queue used for receiving information from the song_chooser thread

player = Player.Player(song_queue, music_database, explorer)  # initialize the music player
sleep_time = 0.5

queue_manager = QueueManager.QueueManager(song_queue, music_database, player, user_name)  # creating a thread that will work in parallel
queue_manager.daemon = True  # when the main is closed this thread will also close

print("[RASP] vlc player initialized")

player.play_next_music(0)
# player.pause()

feedback_receiver.initialize(player, queue_manager.song_chooser)

print("[RASP] starting to play")

queue_manager.start()

while True:
    if player.music_ended():
        player.play_next_music(0.1)

    if feedback_receiver.stop:
        break

    sleep(sleep_time)
    continue
