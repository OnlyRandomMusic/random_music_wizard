import Player
import SongChooser
import utils


song_chooser = SongChooser.SongChooser()
# feedback_receiver = FeedBackReceiver()
player = Player.Player()
path_list = song_chooser.get_test_playlist()
player.add_musics(path_list)
player.play()

while True:

    # path, id_music = song_chooser.get_new_music()
    # player.add_music(path)
    # while len(queue>10):
    #    continue/wait

    # if feedback_receiver.feedback:
    #    agir en conséquence

    continue



