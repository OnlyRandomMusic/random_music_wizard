#! /usr/bin/env python3

# line to add in rc.local to start on boot:
# su rengati -c "python3 home/rengati/random_music_wizard/main.py &"

from time import sleep
import FeedbackReceiver
import MusicWizard

start_on_boot = False

print("[MAIN] starting")

feedback_receiver = FeedbackReceiver.FeedbackReceiver()  # creating a thread that will work in parallel
feedback_receiver.daemon = True  # when the main is closed this thread will also close
feedback_receiver.start()

if start_on_boot:
    music_wizard = MusicWizard.MusicWizard(feedback_receiver)
    feedback_receiver.user_name = music_wizard.user_name
else:
    while not feedback_receiver.user_name:
        sleep(1)
    music_wizard = MusicWizard.MusicWizard(feedback_receiver, feedback_receiver.user_name)

music_wizard.run()
