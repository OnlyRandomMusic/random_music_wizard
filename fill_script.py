from database import playlist_database_filler

lowest_index = input('lowest_index ')
highest_index = input('highest_index ')
step_size = input('step_size ')

playlist_database_filler.measure_population(int(lowest_index), int(highest_index), int(step_size), True)
