#! /usr/bin/env python3

# line to add in rc.local to start on boot:
# su rengati -c "python3 home/rengati/random_music_wizard/main.py &"

import Player
import QueueManager
import queue
from database import MusicDatabase
from time import sleep
import FeedbackReceiver

print("[RASP] starting")

music_database = MusicDatabase.MusicDatabase()
# database.reset()
music_database.create()

song_queue = queue.Queue()  # the queue used for receiving information from the song_chooser thread

player = Player.Player(song_queue, music_database)  # initialize the music player
sleep_time = 0.5

queue_manager = QueueManager.QueueManager(song_queue, music_database, player)  # creating a thread that will work in parallel
queue_manager.daemon = True  # when the main is closed this thread will also close

feedback_receiver = FeedbackReceiver.FeedbackReceiver(player, queue_manager.song_chooser)  # creating a thread that will work in parallel
feedback_receiver.daemon = True  # when the main is closed this thread will also close

print("[RASP] vlc player initialized")

player.play_next_music()
# player.pause()

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
