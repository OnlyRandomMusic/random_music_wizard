import requests
import json
import Database
from time import sleep

database = Database.Database()


# database.reset()
# database.create()


def brute_explore(n, m):
    """make requests to deezer about playlist between id = n and id = m"""
    identifier = n
    while True:
        try:
            data = get_request("https://api.deezer.com/playlist/" + str(identifier))
            if len(data['tracks']['data']) != 0:
                database.add_raw_playlist(data)
        except:
            print('fail')

        identifier += 1
        if identifier > m:
            break


def get_request(address):
    """return the content of a selected request in a json format"""
    request = requests.get(address)
    content = request.content.decode('utf-8')
    ordered_content = json.loads(content)
    return ordered_content


def moderate_explore(identifier=database.get_raw_playlist_max_id(), step_size=50, sleep_time=10):
    while True:
        brute_explore(identifier, identifier + step_size)
        identifier += step_size
        print(identifier)
        sleep(sleep_time)


moderate_explore()
# print(database.get_raw_playlist_max_id())
# database.print_data('playlist_link')
print(database.get_count('raw_playlist'))
print(database.get_count('playlist_link'))
