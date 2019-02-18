import threading
import communication.Receiver
import queue
from time import sleep

volume_step = 4  # the volume step in percentage


class FeedbackReceiver(threading.Thread):
    def __init__(self):
        """instructions_queue is a list of instructions in order to communicate with the main"""
        threading.Thread.__init__(self)

        self.music_wizard = None

        self.user_name = None
        self.need_to_stop_main = False
        self.stop = False

        self.instructions_queue = queue.Queue()
        self.receiver = communication.Receiver.Receiver(self.instructions_queue)

    def initialize(self, music_wizard):
        self.music_wizard = music_wizard

    def run(self):
        print("[FEEDBACK] waiting for instructions")
        while True:
            self.receiver.receive()

            if self.instructions_queue.qsize() > 0:
                instruction, connexion = self.instructions_queue.get()
                self.decode_instruction(instruction, connexion)

            sleep(0.5)
            # print("[RASP] received instruction " + instruction)

            if self.stop:
                break

        print("[FEEDBACK] stopped")

    def decode_instruction(self, instruction, connexion):
        if "start" in instruction:
            self.user_name = instruction.split(':')[-1]
            print("[FEEDBACK] loading {} profile".format(self.user_name))

        if self.music_wizard.queue_manager.song_chooser and self.music_wizard.player:
            if "+" in instruction:
                step_number = instruction.count("+")
                volume = self.music_wizard.player.increase_volume(step_number * volume_step)
                print("[FEEDBACK] volume is now {}%".format(volume))

            if "-" in instruction:
                step_number = instruction.count("-")
                volume = self.music_wizard.player.increase_volume(- step_number * volume_step)
                print("[FEEDBACK] volume is now {}%".format(volume))

            if "next" in instruction:
                done = self.music_wizard.player.play_next_music(-0.5)
                if done:
                    print("[FEEDBACK] the music has been changed")
                else:
                    print("[FEEDBACK] the music can't be changed now")

            if "close" in instruction:
                self.need_to_stop_main = True
                print("[FEEDBACK] program ended")

            if "search" in instruction:
                research = instruction.split(':')
                # instruction structure : "search:research_text:(1 or 0)" last boolean to indicate if the music should be play immediatly or not
                self.music_wizard.queue_manager.song_chooser.play_search(research[1], int(research[2]), from_feedback=True)

            if "play" in instruction:
                self.music_wizard.player.play()

            if "pause" in instruction:
                self.music_wizard.player.pause()

            if "like" in instruction:
                self.music_wizard.score_update_queue.put((self.music_wizard.player.current_music_id, 1))

            if "get" in instruction and "title" in instruction:
                connexion.send(self.music_wizard.player.get_current_music_info())

    def main_stopped(self):
        self.need_to_stop_main = False
