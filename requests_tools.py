import requests
import json
from time import sleep


def songs_of_artist(artist_id, number_of_songs=30):
    """return the main songs of a given artist"""
    song_list = safe_request('artist/{}/top?limit={}'.format(artist_id, number_of_songs), True)
    if 'error' in song_list.keys():
        return
    return song_list['data']


def collaboration(artist_id, songs_list=None):
    """return the artists which have made collaborations with a given artist
    song_list is the dict returned by songs_of_artist"""
    if not songs_list:
        songs_list = songs_of_artist(artist_id)

    artists_list = []

    for song in songs_list:
        if "contributors" in song.keys():
            for artist in song['contributors']:
                if not artist['id'] in artists_list and artist['id'] != artist_id:
                    artists_list.append(artist['id'])

    return artists_list


def safe_request(address, short_format=False):
    """return the content of a selected request in a json format
    and if the request failed do it again"""
    while True:
        try:
            data = get_request(address, short_format)
            return data
        except:
            sleep(0.2)
            print('[REQUEST] API REQUEST request error')


def get_request(address, short_format=False):
    """return the content of a selected request in a json format"""
    if short_format:
        address = 'https://api.deezer.com/' + address

    request = requests.get(address)
    content = request.content.decode('utf-8')
    ordered_content = json.loads(content)
    return ordered_content
