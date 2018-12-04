import sqlite3

def create():

    conn = sqlite3.connect ('example.db')
    c = conn.cursor()

    try:
        c . execute ( '''CREATE TABLE music
                       (id, title_short, link, duration, r_date, preview_link, bpm, gain, artist,
                        album, path, downloaded)''')

        c . execute ( '''CREATE TABLE album
                        (id, genre_id, artist)''')
    except:
        print('base de donnée dja créé')

    conn.commit()
    conn.close()

def add_song(song):

    conn = sqlite3.connect ('example.db')
    c = conn.cursor()

    c.execute ('SELECT * FROM music WHERE id=?',(song['id'],))

    if not c.fetchone():
        c.execute("INSERT INTO music VALUES (?,?,?)",(song['id'],song['title_short'],song['artist']['name']))

    conn.commit()
    conn.close()
