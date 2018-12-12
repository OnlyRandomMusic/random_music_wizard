#!/usr/bin/python3
import os
import json
import mutagen
import spotipy
import requests
from tqdm import tqdm
from Crypto.Hash import MD5
from bs4 import BeautifulSoup
import spotipy.oauth2 as oauth2
from mutagen.id3 import ID3, APIC
from mutagen.easyid3 import EasyID3
from collections import OrderedDict
from binascii import a2b_hex, b2a_hex
from mutagen.flac import FLAC, Picture
from Crypto.Cipher import AES, Blowfish

req = requests.Session()
localdir = os.getcwd()


def generate_token():
    token = oauth2.SpotifyClientCredentials(client_id="4fe3fecfe5334023a1472516cc99d805",
                                            client_secret="0f02b7c483c04257984695007a4a8d5c").get_access_token()
    return token


token = generate_token()
spo = spotipy.Spotify(auth=token)
header = {
    "Accept-Language": "en-US,en;q=0.5"
}
params = {
    "api_version": "1.0",
    "api_token": "null",
    "input": "3",
    "method": "deezer.getUserData"
}


class TrackNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class AlbumNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidLink(Exception):
    def __init__(self, message):
        super().__init__(message)


class BadCredentials(Exception):
    def __init__(self, message):
        super().__init__(message)


class QuotaExceeded(Exception):
    def __init__(self, message):
        super().__init__(message)


class QualityNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class Login:
    def __init__(self, mail, password):
        check = json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", params).text)['results'][
            'checkFormLogin']
        post_data = {
            "type": "login",
            "mail": mail,
            "password": password,
            "checkFormLogin": check
        }
        if "success" == req.post("https://www.deezer.com/ajax/action.php", post_data).text:
            print("[RASP] Success, you are logged in")
        else:
            raise BadCredentials("[RASP] Invalid password or username")

    def download(self, track, location, quality, check):
        song = {}
        ids = track.split("/")[-1]
        name = ids + ".mp3"

        def login():
            try:
                token = json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", params).text)['results'][
                    'checkForm']
            except:
                token = json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", params).text)['results'][
                    'checkForm']
            data = {
                "api_version": "1.0",
                "input": "3",
                "api_token": token,
                "method": "song.getData"
            }
            param = json.dumps({"sng_id": ids})
            try:
                return json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", param, params=data).text)
            except:
                return json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", param, params=data).text)

        def md5hex(data):
            h = MD5.new()
            h.update(data)
            return b2a_hex(h.digest())

        def genurl(quality):
            data = b"\xa4".join(a.encode() for a in [song['md5'], quality, str(ids), str(song['media_version'])])
            data = b"\xa4".join([md5hex(data), data]) + b"\xa4"
            if len(data) % 16:
                data += b"\x00" * (16 - len(data) % 16)
            c = AES.new("jo6aey6haid2Teih", AES.MODE_ECB)
            c = b2a_hex(c.encrypt(data)).decode()
            return "https://e-cdns-proxy-8.dzcdn.net/mobile/1/" + c

        def calcbfkey(songid):
            h = md5hex(b"%d" % int(songid))
            key = b"g4el58wc0zvf9na1"
            return "".join(chr(h[i] ^ h[i + 16] ^ key[i]) for i in range(16))

        def blowfishDecrypt(data, key):
            c = Blowfish.new(key, Blowfish.MODE_CBC, a2b_hex("0001020304050607"))
            return c.decrypt(data)

        def decryptfile(fh, key, fo):
            i = 0
            for data in fh:
                if not data:
                    break
                if (i % 3) == 0 and len(data) == 2048:
                    data = blowfishDecrypt(data, key)
                fo.write(data)
                i += 1

        infos = login()
        while not "MD5_ORIGIN" in str(infos):
            infos = login()
        song['md5'] = infos['results']['MD5_ORIGIN']
        song['media_version'] = infos['results']['MEDIA_VERSION']
        try:
            if int(infos['results']['FILESIZE_' + quality]) > 0 and quality == "FLAC":
                quality = "9"
            elif int(infos['results']['FILESIZE_' + quality]) > 0 and quality == "MP3_320":
                quality = "3"
            elif int(infos['results']['FILESIZE_' + quality]) > 0 and quality == "MP3_256":
                quality = "5"
            elif int(infos['results']['FILESIZE_' + quality]) > 0 and quality == "MP3_128":
                quality = "1"
            else:
                if check:
                    raise QualityNotFound("The quality chose can't be downloaded")
                quality = "1"
        except KeyError:
            raise QualityNotFound("The quality chose can't be downloaded")
        try:
            fh = requests.get(genurl(quality))
        except:
            fh = requests.get(genurl(quality))
        if len(fh.content) == 0:
            raise TrackNotFound("")
        open(location + name, "wb").write(fh.content)
        fo = open(location + name, "wb")
        decryptfile(fh.iter_content(2048), calcbfkey(ids), fo)

# the custom function to download a track
    def download_track(self, music_id, database, output=localdir + "/musics/", check=False, quality="MP3_128",
                                   recursive=True):

        artist = database.get_music_info(music_id, 'artist')
        title = database.get_music_info(music_id, 'title')

        song = title + " - " + artist
        print("enter")
        # attention à cette ligne, elle est utile mais ne doit pas être oubliée lors de la génération du path
        # elle a pour but d'éviter les conflits si des caractères spéciaux sont présents dans les string
        dir = str(output) + "/" + artist.replace("/", "").replace("$", "S") + "/"
        print(dir)
        try:
            os.makedirs(dir)
        except:
            None
        print("dir")
        name = artist.replace("/", "").replace("$", "S") + " " + title.replace("/", "").replace("$", "S") + ".mp3"
        print(name)
        if os.path.isfile(dir + name):
            if not check:
                return dir + name
        print("[RASP] Downloading: " + song)
        try:
            self.download("http://www.deezer.com/track/" + str(music_id), dir, quality, recursive)
            print("lala")
        except TrackNotFound:
            print("[RASP] " + song + " not found at the url given, trying to search it")
            try:
                url = json.loads(requests.get(
                    "https://api.deezer.com/search/track/?q=" + title.replace("#", "") + " + " + artist.replace(
                        "#", "")).text)
            except:
                url = json.loads(requests.get(
                    "https://api.deezer.com/search/track/?q=" + title.replace("#", "") + " + " + artist.replace(
                        "#", "")).text)
            try:
                if url['error']['message'] == "Quota limit exceeded":
                    raise QuotaExceeded("Too much requests limit yourself")
            except KeyError:
                None
            try:
                for a in range(url['total'] + 1):
                    if url['data'][a]['title'] == title or url['data'][a]['title_short'] in title:
                        URL = url['data'][a]['link']
                        break
            except IndexError:
                try:
                    try:
                        url = json.loads(requests.get(
                            "https://api.deezer.com/search/track/?q=" + title.replace("#", "").split(" ")[
                                0] + " + " + artist.replace("#", "")).text)
                    except:
                        url = json.loads(requests.get(
                            "https://api.deezer.com/search/track/?q=" + title.replace("#", "").split(" ")[
                                0] + " + " + artist.replace("#", "")).text)
                    try:
                        if url['error']['message'] == "Quota limit exceeded":
                            raise QuotaExceeded("Too much requests limit yourself")
                    except KeyError:
                        None
                    for a in range(url['total'] + 1):
                        if title.split(" ")[0] in url['data'][a]['title']:
                            URL = url['data'][a]['link']
                            break
                except IndexError:
                    raise TrackNotFound("Track not found: " + song)
            self.download(URL, dir, quality, recursive)
        try:
            os.rename(dir + URL.split("/")[-1] + ".mp3", dir + name)
        except FileNotFoundError:
            None
        return dir + name

###########

    def download_track_alternative(self, URL, output=localdir + "/musics/", check=False, quality="MP3_128",
                                   recursive=True):
        if output == localdir + "/Songs":
            if not os.path.isdir("Songs"):
                os.makedirs("Songs")

        if "?utm" in URL:
            URL, a = URL.split("?utm")
        URL = "http://www.deezer.com/track/" + URL.split("/")[-1]
        try:
            url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
        except:
            url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
        try:
            if url['error']['message'] == "Quota limit exceeded":
                raise QuotaExceeded("Too much requests limit yourself")
        except KeyError:
            None
        try:
            if "error" in str(url):
                raise InvalidLink("Invalid link ;)")
        except KeyError:
            None

        artist = url['artist']['name']
        title = url['title_short']

        song = title + " - " + artist

        # attention à cette ligne, elle est utile mais ne doit pas être oubliée lors de la génération du path
        # elle a pour but d'éviter les conflits si des caractères spéciaux sont présents dans les string
        dir = str(output) + "/" + artist.replace("/", "").replace("$", "S") + "/"
        try:
            os.makedirs(dir)
        except:
            None
        name = artist.replace("/", "").replace("$", "S") + " " + title.replace("/", "").replace("$", "S") + ".mp3"
        if os.path.isfile(dir + name):
            if not check:
                return dir + name

        print("[RASP] Downloading: " + song)
        try:
            self.download(URL, dir, quality, recursive)
        except TrackNotFound:
            print("[RASP] " + song + " not found at the url given, trying to search it")
            try:
                url = json.loads(requests.get(
                    "https://api.deezer.com/search/track/?q=" + title.replace("#", "") + " + " + artist.replace(
                        "#", "")).text)
            except:
                url = json.loads(requests.get(
                    "https://api.deezer.com/search/track/?q=" + title.replace("#", "") + " + " + artist.replace(
                        "#", "")).text)
            try:
                if url['error']['message'] == "Quota limit exceeded":
                    raise QuotaExceeded("Too much requests limit yourself")
            except KeyError:
                None
            try:
                for a in range(url['total'] + 1):
                    if url['data'][a]['title'] == title or url['data'][a]['title_short'] in title:
                        URL = url['data'][a]['link']
                        break
            except IndexError:
                try:
                    try:
                        url = json.loads(requests.get(
                            "https://api.deezer.com/search/track/?q=" + title.replace("#", "").split(" ")[
                                0] + " + " + artist.replace("#", "")).text)
                    except:
                        url = json.loads(requests.get(
                            "https://api.deezer.com/search/track/?q=" + title.replace("#", "").split(" ")[
                                0] + " + " + artist.replace("#", "")).text)
                    try:
                        if url['error']['message'] == "Quota limit exceeded":
                            raise QuotaExceeded("Too much requests limit yourself")
                    except KeyError:
                        None
                    for a in range(url['total'] + 1):
                        if title.split(" ")[0] in url['data'][a]['title']:
                            URL = url['data'][a]['link']
                            break
                except IndexError:
                    raise TrackNotFound("Track not found: " + song)
            self.download(URL, dir, quality, recursive)
        try:
            os.rename(dir + URL.split("/")[-1] + ".mp3", dir + name)
        except FileNotFoundError:
            None
        return dir + name

###############################

    def download_trackdee(self, URL, output=localdir + "/Songs/", check=True, quality="MP3_128", recursive=True):
        if output == localdir + "/Songs":
            if not os.path.isdir("Songs"):
                os.makedirs("Songs")
        array = []
        music = []
        artist = []
        album = []
        tracknum = []
        discnum = []
        year = []
        genre = []
        ar_album = []
        if "?utm" in URL:
            URL, a = URL.split("?utm")
        URL = "http://www.deezer.com/track/" + URL.split("/")[-1]
        try:
            url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
        except:
            url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
        try:
            if url['error']['message'] == "Quota limit exceeded":
                raise QuotaExceeded("Too much requests limit yourself")
        except KeyError:
            None
        try:
            if "error" in str(url):
                raise InvalidLink("Invalid link ;)")
        except KeyError:
            None
        try:
            url1 = json.loads(
                requests.get("http://api.deezer.com/album/" + str(url['album']['id']), headers=header).text)
        except:
            url1 = json.loads(
                requests.get("http://api.deezer.com/album/" + str(url['album']['id']), headers=header).text)
        try:
            if url1['error']['message'] == "Quota limit exceeded":
                raise QuotaExceeded("Too much requests limit yourself")
        except KeyError:
            None
        try:
            image = url['album']['cover_xl'].replace("1000", "1200")
        except:
            try:
                image = requests.get(URL).text
            except:
                image = requests.get(URL).text
            image = BeautifulSoup(image, "html.parser").find("img", class_="img_main").get("src").replace("120", "1200")
        music.append(url['title_short'])

        array.append(url['artist']['name'])  # modified

        # for a in url['contributors']:
        #    array.append(a['name'])
        # if len(array) > 1:
        #    for a in array:
        #        for b in range(len(array)):
        #            try:
        #                if a in array[b] and a != array[b]:
        #                    del array[b]
        #            except IndexError:
        #                break
        artist.append(", ".join(OrderedDict.fromkeys(array)))
        album.append(url['album']['title'])
        tracknum.append(url['track_position'])
        discnum.append(url['disk_number'])
        year.append(url['album']['release_date'])
        song = music[0] + " - " + artist[0]
        try:
            if url1['error']['message'] == "no data":
                raise TrackNotFound("Track not found: " + song)
        except KeyError:
            None
        try:
            for a in url1['genres']['data']:
                genre.append(a['name'])
        except:
            None
        for a in url1['contributors']:
            if a['role'] == "Main":
                ar_album.append(a['name'])
        dir = str(output) + "/" + artist[0].replace("/", "").replace("$", "S") + "/"
        try:
            os.makedirs(dir)
        except:
            None
        name = artist[0].replace("/", "").replace("$", "S") + " " + music[0].replace("/", "").replace("$", "S") + ".mp3"
        if os.path.isfile(dir + name):
            if check == False:
                return dir + name
            ans = input("Song already exist do you want to redownload it?(y or n):")
            if not ans == "y":
                return
        print("\nDownloading:" + song)
        try:
            self.download(URL, dir, quality, recursive)
        except TrackNotFound:
            try:
                url = json.loads(requests.get(
                    "https://api.deezer.com/search/track/?q=" + music[0].replace("#", "") + " + " + artist[0].replace(
                        "#", "")).text)
            except:
                url = json.loads(requests.get(
                    "https://api.deezer.com/search/track/?q=" + music[0].replace("#", "") + " + " + artist[0].replace(
                        "#", "")).text)
            try:
                if url['error']['message'] == "Quota limit exceeded":
                    raise QuotaExceeded("Too much requests limit yourself")
            except KeyError:
                None
            try:
                for a in range(url['total'] + 1):
                    if url['data'][a]['title'] == music[0] or url['data'][a]['title_short'] in music[0]:
                        URL = url['data'][a]['link']
                        break
            except IndexError:
                try:
                    try:
                        url = json.loads(requests.get(
                            "https://api.deezer.com/search/track/?q=" + music[0].replace("#", "").split(" ")[
                                0] + " + " + artist[0].replace("#", "")).text)
                    except:
                        url = json.loads(requests.get(
                            "https://api.deezer.com/search/track/?q=" + music[0].replace("#", "").split(" ")[
                                0] + " + " + artist[0].replace("#", "")).text)
                    try:
                        if url['error']['message'] == "Quota limit exceeded":
                            raise QuotaExceeded("Too much requests limit yourself")
                    except KeyError:
                        None
                    for a in range(url['total'] + 1):
                        if music[0].split(" ")[0] in url['data'][a]['title']:
                            URL = url['data'][a]['link']
                            break
                except IndexError:
                    raise TrackNotFound("Track not found: " + song)
            self.download(URL, dir, quality, recursive)
        try:
            os.rename(dir + URL.split("/")[-1] + ".mp3", dir + name)
        except FileNotFoundError:
            None
        try:
            image = requests.get(image).content
        except:
            image = requests.get(image).content
        try:
            tag = EasyID3(dir + name)
            tag.delete()
        except mutagen.id3.ID3NoHeaderError:
            try:
                tag = mutagen.File(dir + name, easy=True)
                tag.add_tags()
            except mutagen.flac.FLACVorbisError:
                tag = FLAC(dir + name)
                tag.delete()
                images = Picture()
                images.type = 3
                images.data = image
                tag.add_picture(images)
        except:
            return dir + name
        tag['artist'] = artist[0]
        tag['title'] = music[0]
        tag['date'] = year[0]
        tag['album'] = album[0]
        tag['tracknumber'] = str(tracknum[0])
        tag['discnumber'] = str(discnum[0])
        tag['genre'] = " & ".join(genre)
        tag['albumartist'] = ", ".join(ar_album)
        tag.save()
        try:
            audio = ID3(dir + name)
            audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image)
            audio.save()
        except:
            None
        return dir + name

    def download_name(self, artist, song, output=localdir + "/Songs/", check=True, quality="MP3_128", recursive=True):
        global spo
        try:
            search = spo.search(q="track:" + song + " artist:" + artist)
        except:
            token = generate_token()
            spo = spotipy.Spotify(auth=token)
            search = spo.search(q="track:" + song + " artist:" + artist)
        try:
            return self.download_trackspo(search['tracks']['items'][0]['external_urls']['spotify'], output, check,
                                          quality=quality, recursive=recursive)
        except IndexError:
            raise TrackNotFound("Track not found: " + artist + " - " + song)
