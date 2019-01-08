from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')

while True:
    message = input()

    if "help" in message:
            print("""
+       increase the volume
-       decrease the volume
play    start playing music
pause   pause the music
next    go to the next music
quit    exit the program
close   end the main program
search  search for a music""")

    if "search" in message:
            research = input("What are you searching for ?  ")
            immediately = input("Would you like to play it immediately ? (yes/no) ")

            if 'y' in immediately or 'Y' in immediately:
                message = "search:{}:{}".format(research, '1')
            else:
                message = "search:{}:{}".format(research, '0')

    if message == 'quit':
        break

    conn.send(message)


conn.close()
