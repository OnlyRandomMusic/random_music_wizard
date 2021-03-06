from multiprocessing.connection import Client

try:
    address = ('localhost', 6000)
    conn = Client(address, authkey=b'secret password')
except:
    address = ('localhost', 6001)
    conn = Client(address, authkey=b'secret password')

print("""Welcome
If the music isn't playing, type start""")

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

    if "start" in message:
        user_name = input("Please enter the profile you want to load\n")
        if not user_name:
            user_name = 'remi'
        print("program starting ...")
        message = "start:" + user_name

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
