import json
import requests
import vlc
import time
import os
import platform

OS_RASPBERRY = 'raspberrypi'

if platform.uname()[1] == OS_RASPBERRY:
    import deezloader

# name of the current directory in order to save musics in the right place
dir_path = os.path.dirname(os.path.realpath(__file__))


def request_example(address):
    """return the content of a selected request in a json format"""
    request = requests.get(address)
    content = request.content.decode('utf-8')
    ordered_content = json.loads(content)
    return ordered_content


def play_song(path):
    """initialize a vlc player and
    begin to play a song with VLC
    path can be an url"""
    if platform.uname()[1] == OS_RASPBERRY:
        player = vlc.MediaPlayer(path)
        error_code = player.play()
        if error_code == -1:
            print("an error occurred in VLC")
    else:
        print("[RASP] play " + path)


def download_song(link, path, mail, password, quality="MP3_128"):
    """download a song from a Deezer link in a selected directory
    quality can be FLAC, MP3_320, MP3_256 or MP3_128"""
    if platform.uname()[1] == OS_RASPBERRY:
        downloader = deezloader.Login(mail, password)
        downloader.download_trackdee(link, output=path, check=False, quality=quality, recursive=True)
        # check=False for not check if song already exist
        # recursive=False for download the song if quality selected chose doesn't exist
    else:
        print("[RASP] download " + link)


def test_download_and_play(mail, password):
    """test if the download and the play function works"""
    download_song('https://www.deezer.com/us/track/3135553', dir_path + os.sep + 'musics', mail, password)
    play_song('musics' + os.sep + 'Daft Punk' + os.sep + 'Daft Punk One More Time.mp3')
    input("Press Enter to stop")


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


def record(new_data):
    """record the data in a json file"""
    with open('songDB.json', 'w') as outfile:
        json.dump(new_data, outfile)


def getSongDB():
    """get the song data as a list of songs"""
    with open('songDB.json') as json_file:
        data = json.load(json_file)
    return data


mail, password = read_id()
test_download_and_play(mail, password)
