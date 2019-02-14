#! /usr/bin/env python3

import Player
import QueueManager
import queue
from database import MusicDatabase
import ExplorationManager
from time import sleep
import FeedbackReceiver

auto_start = True
default_user = 'remi'

print("[MAIN] starting")

feedback_receiver = FeedbackReceiver.FeedbackReceiver()  # creating a thread that will work in parallel
feedback_receiver.daemon = True  # when the main is closed this thread will also close
feedback_receiver.start()

if auto_start:
    user_name = default_user
    feedback_receiver.user_name = default_user
else:
    while not feedback_receiver.user_name:
        sleep(1)
    user_name = feedback_receiver.user_name

music_database = MusicDatabase.MusicDatabase()
music_database.create()

score_update_queue = queue.Queue()
exploration_manager = ExplorationManager.ExplorationManager(user_name, score_update_queue)
exploration_manager.daemon = True

print("[MAIN] explorer initialized")

song_queue = queue.Queue()  # the queue used for receiving information from the song_chooser thread

player = Player.Player(song_queue, music_database, score_update_queue)  # initialize the music player
sleep_time = 0.5

queue_manager = QueueManager.QueueManager(song_queue, music_database, player, user_name, score_update_queue)  # creating a thread that will work in parallel
queue_manager.daemon = True  # when the main is closed this thread will also close

print("[MAIN] vlc player initialized")

player.play_next_music(0)
# player.pause()

feedback_receiver.initialize(player, queue_manager.song_chooser, score_update_queue)

print("[MAIN] starting to play")

queue_manager.start()
exploration_manager.start()

while True:
    if player.music_ended():
        player.play_next_music(0.1)

    if feedback_receiver.stop:
        break

    sleep(sleep_time)
    continue

print("[MAIN] bye bye")
