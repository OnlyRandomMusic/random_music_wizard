import threading
import communication.Receiver
import queue
from time import sleep

volume_step = 4  # the volume step in percentage


class FeedbackReceiver(threading.Thread):
    def __init__(self):
        """instructions_queue is a list of instructions in order to communicate with the main"""
        threading.Thread.__init__(self)

        self.player = None
        self.song_chooser = None

        self.user_name = None
        self.stop = False

        self.instructions_queue = queue.Queue()
        self.receiver = communication.Receiver.Receiver(self.instructions_queue)

    def initialize(self, player, song_chooser, score_update_queue):
        self.player = player
        self.song_chooser = song_chooser
        self.score_update_queue = score_update_queue

    def run(self):
        print("[FEEDBACK] waiting for instructions")
        while True:
            self.receiver.receive()

            if self.instructions_queue.qsize() > 0:
                instruction = self.instructions_queue.get()
                self.decode_instruction(instruction)

            sleep(0.5)
            # print("[RASP] received instruction " + instruction)

    def decode_instruction(self, instruction):
        if "start" in instruction:
            self.user_name = instruction.split(':')[-1]
            print("[FEEDBACK] loading {} profile".format(self.user_name))

        if self.song_chooser and self.player:
            if "+" in instruction:
                step_number = instruction.count("+")
                volume = self.player.increase_volume(step_number * volume_step)
                print("[FEEDBACK] volume is now {}%".format(volume))

            if "-" in instruction:
                step_number = instruction.count("-")
                volume = self.player.increase_volume(- step_number * volume_step)
                print("[FEEDBACK] volume is now {}%".format(volume))

            if "next" in instruction:
                done = self.player.play_next_music(-0.5)
                if done:
                    print("[FEEDBACK] the music has been changed")
                else:
                    print("[FEEDBACK] the music can't be changed now")

            if "close" in instruction:
                self.stop = True
                print("[FEEDBACK] program ended")

            if "search" in instruction:
                research = instruction.split(':')
                # instruction structure : "search:research_text:(1 or 0)" last boolean to indicate if the music should be play immediatly or not
                self.song_chooser.play_search(research[1], int(research[2]), from_feedback=True)

            if "play" in instruction:
                self.player.play()

            if "pause" in instruction:
                self.player.pause()

            if "like" in instruction:
                self.score_update_queue.put((self.player.current_music_id, 1))
