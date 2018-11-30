"""
song_chooser = SongChooser()
feedback_receiver = FeedBackReceiver()
player = vlc.MediaPlayer(path_to_start_music)
player.play()

while True:

    path, id_music = song_chooser.get_new_music()
    player.addqueue(path)
    while len(queue>10):
        continue/wait

    if feedback_receiver.feedback:
        agir en conséquence

"""


