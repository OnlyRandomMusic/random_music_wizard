import requests
import json


def songs_of_artist(artist_id, number_of_songs=30):
    """return the main songs of a given artist"""
    song_list = get_request('artist/{}/top?limit={}'.format(artist_id, number_of_songs), True)
    return song_list


def collaboration(artist_id, songs_list=None):
    """return the artists which have made collaborations with a given artist
    song_list is the dict returned by songs_of_artist"""
    if not songs_list:
        songs_list = songs_of_artist(artist_id)

    artists_list = []

    for song in songs_list['data']:
        if "contributors" in song.keys():
            for artist in song['contributors']:
                if not artist['id'] in artists_list and artist['id'] != artist_id:
                    artists_list.append(artist['id'])

    return artists_list


def get_request(address, short_format=False):
    """return the content of a selected request in a json format"""
    if short_format:
        address = 'https://api.deezer.com/' + address

    request = requests.get(address)
    content = request.content.decode('utf-8')
    ordered_content = json.loads(content)
    return ordered_content
