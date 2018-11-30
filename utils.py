import requests
import json


# utils for the database
def record(new_data):
    """record the data in a json file"""
    with open('songDB.json', 'w') as outfile:
        json.dump(new_data, outfile)


def get_song_db():
    """get the song data as a list of songs"""
    with open('songDB.json') as json_file:
        data = json.load(json_file)
    return data


# utils for the requests
def get_request(address):
    """return the content of a selected request in a json format"""
    request = requests.get(address)
    content = request.content.decode('utf-8')
    ordered_content = json.loads(content)
    return ordered_content


def get_playlist_data(playlist_link):
    """retrun the list of the data of every song in the playlist"""


# random utils
def read_id():
    """read the id (mail and password) in the file identifiers.txt
    the file must look like that :
    YOUR_EMAIL
    YOUR_PASSWORD"""
    try:
        with open("identifiers.txt", "r") as id_file:
            ids = id_file.readlines()
            mail = ids[0]
            password = ids[1]
            return mail, password
    except:
        print("[error] missing the file identifier.txt or missing mail and password in this file")
