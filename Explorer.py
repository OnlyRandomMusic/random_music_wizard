import requests_tools
from database import MusicDatabase
from database import PlaylistDatabase
from database import UserDatabase
# from time import sleep


class Explorer:
    def __init__(self, user_name):
        self.music_database = MusicDatabase.MusicDatabase()
        self.playlist_database = PlaylistDatabase.PlaylistDatabase()
        self.user_database = UserDatabase.UserDatabase(user_name)
        self.user_database.open_fast_connexion()

    def set_score(self, music_id, score):
        if not score:
            return

        artist_id = self.music_database.get_music_info(music_id, 'artist_id')
        self.user_database.update_score(music_id, score)
        song_updated = [music_id]

        # first step
        songs_of_artist = requests_tools.songs_of_artist(artist_id)

        if songs_of_artist:
            for song in songs_of_artist:
                if not song['id'] in song_updated:
                    self.user_database.update_score(song['id'], score*0.5)
                    song_updated.append(song['id'])

            # second step
            collaborators = requests_tools.collaboration(artist_id, songs_of_artist)

            if collaborators:
                for collaborator in collaborators:
                    songs_of_collaborator = requests_tools.songs_of_artist(collaborator, 10)
                    for song in songs_of_collaborator:
                        if not song['id'] in song_updated:
                            self.user_database.update_score(song['id'], score*0.1)
                            song_updated.append(song['id'])

        # third step
        # playlist search

        print("[RASP] Scores updated")


# from database import UserDatabase
# m = MusicDatabase.MusicDatabase()
# d = UserDatabase.UserDatabase('remi')
# exp = Explorer(d)
# song = requests_tools.get_request('https://api.deezer.com/track/94935172')
# m.add_song(song)
# exp.set_score(94935172, 1)
# d.print_data('remi')
