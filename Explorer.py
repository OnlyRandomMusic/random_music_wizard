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
        self.user_database.reset_music_played()
        self.nb_playlist_explore = 5

    def set_score(self, music_id, score):
        print("[EXPLORER] updating scores")

        if not score:
            return

        artist_id = self.music_database.get_music_info(music_id, 'artist_id')
        self.user_database.update_score(music_id, score)
        song_updated = [music_id]
        database_buffer = []

        # first step
        songs_of_artist = requests_tools.songs_of_artist(artist_id)

        if songs_of_artist:
            for song in songs_of_artist:
                if not song['id'] in song_updated:
                    # self.user_database.update_score(song['id'], score*0.5)
                    song_updated.append(song['id'])
                    # self.music_database.add_song(song, verbose=False)
                    database_buffer.append((song, 0.5))

            print("[EXPLORER] first step done")

            # second step
            collaborators = requests_tools.collaboration(artist_id, songs_of_artist)

            if collaborators:
                for collaborator in collaborators:
                    songs_of_collaborator = requests_tools.songs_of_artist(collaborator, 10)
                    for song in songs_of_collaborator:
                        if not song['id'] in song_updated:
                            # self.user_database.update_score(song['id'], score*0.1)
                            song_updated.append(song['id'])
                            # self.music_database.add_song(song, verbose=False)
                            database_buffer.append((song, 0.1))

        print("[EXPLORER] second step done")

        # third step
        # playlist search
        playlist_ids = self.playlist_database.get_related_playlists(music_id, self.nb_playlist_explore)

        for playlist_id in playlist_ids:
            playlist = requests_tools.safe_request('playlist/' + str(playlist_id), True)
            for song in playlist['tracks']['data']:
                # self.music_database.add_song(song)
                # self.user_database.update_score(song['id'], score * 0.05)
                database_buffer.append((song, 0.05))

        self.user_database.open_fast_connexion()
        for elem in database_buffer:
            self.user_database.update_score(elem[0]['id'], score*elem[1])
        self.user_database.close_fast_connexion()

        self.music_database.open_fast_connexion()
        for elem in database_buffer:
            self.music_database.add_song(elem[0], verbose=False)
        self.music_database.close_fast_connexion()

        print("[EXPLORER] Scores updated")


# from database import UserDatabase
# m = MusicDatabase.MusicDatabase()
# d = UserDatabase.UserDatabase('remi')
# exp = Explorer(d)
# song = requests_tools.safe_request('https://api.deezer.com/track/94935172')
# m.add_song(song)
# exp.set_score(94935172, 1)
# d.print_data('remi')
