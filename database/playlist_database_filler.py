from database import PlaylistDatabase
import requests_tools
from random import randint
from time import sleep

playlist_database = PlaylistDatabase.PlaylistDatabase()
playlist_database.create()


def playlist_brute_explore(n, m):
    """make requests to deezer about playlist between id = n and id = m"""
    identifier = n
    while True:
        try:
            data = requests_tools.get_request("playlist/" + str(identifier), True)
            if len(data['tracks']['data']) != 0:
                playlist_database.add_raw_playlist(data)
        except:
            print('fail')

        identifier += 1
        if identifier > m:
            break


def playlist_random_explore(lowest_id, highest_id, n=50):
    """make n requests to deezer about playlist randomly between id = a and id = b"""
    success_nb = 0

    for _ in range(n):
        identifier = randint(lowest_id, highest_id)

        try:
            data = requests_tools.get_request("playlist/" + str(identifier), True)
            if len(data['tracks']['data']) != 0:
                playlist_database.add_raw_playlist(data)
                success_nb += 1
        except:
            print('fail')

    return success_nb


def playlist_moderate_explore(identifier=0, step_size=50, sleep_time=10):
    if identifier == 0:
        identifier = playlist_database.get_raw_playlist_max_id()

    while True:
        # playlist_brute_explore(identifier, identifier + step_size)
        # identifier += step_size
        # print(identifier)

        playlist_random_explore(step_size)

        sleep(sleep_time)


def measure_population(lowest_id, highest_id, step_size, write_result_in_file=False, file_name=None):
    current_id = lowest_id
    population = []

    while current_id < highest_id:
        nb_success = playlist_random_explore(current_id, current_id + step_size)
        population.append((current_id, nb_success))
        current_id += step_size
        sleep(10)

    if write_result_in_file:
        write_in_file(population,
                      'population from ' + str(lowest_id) + ' to ' + str(highest_id) + ' step = ' + str(step_size))
    return population


def write_in_file(data_list, file_name='result'):
    with open(file_name + '.txt', 'w') as file:
        for elem in data_list:
            file.write(str(elem[0]) + ';' + str(elem[1]) + '\n')
