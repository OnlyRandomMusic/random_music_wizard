import sqlite3


def create():
    conn = sqlite3.connect('.db')
    c = conn.cursor()

    try:
        c.execute('''CREATE TABLE music
                       (id, title_short, link, duration, r_date, preview_link, bpm, gain, artist_id,
                        album_id, path, downloaded)''')

        c.execute('''CREATE TABLE album
                        (id, genre_id, artist_id)''')

        c.execute('''CREATE TABLE artist
                        (id, name)''')

    except:
        print('base de donnée déja créée')

    conn.commit()
    conn.close()


def add_song(song, path=None, downloaded=False):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute('SELECT * FROM music WHERE id=?', (song['id'],))

    if not c.fetchone():
        c.execute("INSERT INTO music VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
            song['id'], song['title_short'], song['link'], song['duration'], song['release_date'], song['preview'],
            song['bpm'], song['gain'], song['artist']['id'], song['album']['id'], path, downloaded))

        print("[RASP] Successfully added {} in database".format(song['title_short']))
    else:
        print("[RASP] Song {} already in database".format(song['title_short']))

    conn.commit()
    conn.close()


def get_all_songs(print_title=False):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('SELECT id, title_short FROM music')
    data = c.fetchall()

    if print_title:
        for song in data:
            print(song[1])

    conn.close()
    return [song[0] for song in data]
