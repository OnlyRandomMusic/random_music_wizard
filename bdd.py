import sqlite3


def create():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''CREATE TABLE music
                       (id, title_short, link, duration, r_date, preview_link, bpm, gain, artist_id,
                        album_id, path, downloaded)''')

        # cursor.execute('''CREATE TABLE album
        #                 (id, genre_ids, artist_id)''')
        #
        # cursor.execute('''CREATE TABLE artist
        #                 (id, name)''')
    except:
        print('base de donnée déja créée')

    conn.commit()
    conn.close()


def add_song(song, path=None, downloaded=False):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM music WHERE id=?', (song['id'],))

    if not cursor.fetchone():
        cursor.execute("INSERT INTO music VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
            song['id'], song['title_short'], song['link'], song['duration'], song['release_date'], song['preview'],
            song['bpm'], song['gain'], song['artist']['id'], song['album']['id'], path, downloaded))

        print("[RASP] Successfully added {} in database".format(song['title_short']))
    else:
        print("[RASP] Song {} already in database".format(song['title_short']))
        return

    conn.commit()
    conn.close()


def print_data():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM music')
    data = cursor.fetchall()
    conn.close()

    print(data)


def reset():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS music')
    cursor.execute('DROP TABLE IF EXISTS album')
    cursor.execute('DROP TABLE IF EXISTS artist')
    conn.commit()
    conn.close()
