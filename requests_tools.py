import requests
import json


def songs_of_artist(self, artist_id, number_of_songs=25):
    song_list = get_request('{}/top?limit={}'.format(artist_id, number_of_songs), True)
    return song_list


def get_request(address, short_format=False):
    """return the content of a selected request in a json format"""
    if short_format:
        address = 'https://api.deezer.com/' + address

    request = requests.get(address)
    content = request.content.decode('utf-8')
    ordered_content = json.loads(content)
    return ordered_content
