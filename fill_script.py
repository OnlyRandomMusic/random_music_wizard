from database import playlist_database_filler

lowest_index = input('lowest_index ')
highest_index = input('highest_index ')
# step_size = input('step_size ')
n = input('n ')
file_name = input('file name ')

if file_name:
    playlist_database_filler.measure_population(int(lowest_index), int(highest_index), int(n), file_name, write_result_in_file=True)
