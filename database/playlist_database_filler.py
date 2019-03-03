from database import PlaylistDatabase
import requests_tools
from random import randint
from random import sample
from time import sleep
import os

playlist_database = PlaylistDatabase.PlaylistDatabase()
playlist_database.create()
playlist_database.open_fast_connection()


def playlist_brute_explore(n, m):
    """make requests to deezer about playlist between id = n and id = m"""
    identifier = n
    while True:
        try:
            data = requests_tools.safe_request("playlist/" + str(identifier), True)
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
            data = requests_tools.safe_request("playlist/" + str(identifier), True)
            if len(data['tracks']['data']) != 0:
                playlist_database.add_raw_playlist(data)
                success_nb += 1
        except:
            continue

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


def measure_population(lowest_id, highest_id, n, file_name, step_size=0, write_result_in_file=False):
    if step_size == 0:
        step_size = (highest_id - lowest_id) // 50

    population = {}
    step_ids = [lowest_id + k * step_size for k in range(int((highest_id - lowest_id) / step_size))]
    nb_iterations = 50 // len(step_ids)

    if nb_iterations == 0:
        print('error')
        return

    for step_id in step_ids:
        population[step_id] = 0

    for i in range(n):
        for _ in range(nb_iterations):
            shuffled_step_ids = sample(step_ids, len(step_ids))

            for step_id in shuffled_step_ids:
                nb_success = playlist_random_explore(step_id, step_id + step_size, 1)
                population[step_id] += nb_success
        print(str(100*(i+1)/n) + "%")
        sleep(10)

    if write_result_in_file:
        write_in_file(population,
                      'data' + os.sep + file_name)

    playlist_database.close_fast_connection()
    return population


def write_in_file(data_dict, file_name='result'):
    with open(file_name + '.txt', 'w') as file:
        for elem in data_dict.keys():
            file.write(str(elem) + ';' + str(data_dict[elem]) + '\n')
