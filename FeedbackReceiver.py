import threading
import communication.Receiver
import communication.StateInformationBroadcaster
import queue
from time import sleep

volume_step = 4  # the volume step in percentage


class FeedbackReceiver(threading.Thread):
    def __init__(self, mode):
        """instructions_queue is a list of instructions in order to communicate with the main"""
        threading.Thread.__init__(self)

        self.music_wizard = None
        self.mode = mode

        self.user_name = None
        self.need_to_stop_instance = False # to close current music_wizard instance
        self.initialized = False
        self.stop = False
        self.kill_main = False # to kill the main program

        self.instructions_queue = queue.Queue()
        self.receiver = communication.Receiver.Receiver(self.instructions_queue)

        self.broadcaster = communication.StateInformationBroadcaster.StateInformationBroadcaster(self)
        self.broadcaster.daemon = True
        self.broadcaster.start()

    def initialize(self, music_wizard):
        self.music_wizard = music_wizard
        self.initialized = True

    def run(self):
        print("[FEEDBACK] waiting for instructions")
        while True:
            self.receiver.receive()

            if self.instructions_queue.qsize() > 0:
                instruction, connexion = self.instructions_queue.get()
                self.decode_instruction(instruction, connexion)

            sleep(0.1)
            # print("[RASP] received instruction " + instruction)

            if self.stop:
                break

        print("[FEEDBACK] stopped")

    def decode_instruction(self, instruction, connexion):
        if "start" in instruction:
            self.user_name = instruction.split(':')[-1]
            print("[FEEDBACK] loading {} profile".format(self.user_name))

        if self.initialized:
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
                # stop the current music_wizard instance
                self.need_to_stop_instance = True
                print("[FEEDBACK] program ended")

            if "kill" in instruction:
                # kill the all python program
                self.need_to_stop_instance = True
                self.kill_main = True

            if "search" in instruction:
                research = instruction.split(':')
                # instruction structure : "search:research_text:(1 or 0)" last boolean to indicate if the music should be play immediatly or not
                self.music_wizard.queue_manager.song_chooser.play_search(research[1], int(research[2]), from_feedback=True)

            if "play" in instruction:
                self.music_wizard.player.play()

            if "pause" in instruction:
                self.music_wizard.player.pause()

            if "like" in instruction:
                if self.music_wizard.score_update_queue:
                    self.music_wizard.score_update_queue.put((self.music_wizard.player.current_music_id, 1))

            # if "get" in instruction and "title" in instruction:
            #     # obsolete thanks to broadcaster
            #     connexion.send(self.music_wizard.player.get_current_music_info())

            if "change_user" in instruction:
                # instruction structure : "change_user:new_user_name"
                # need to add if exploration mode:
                new_user_name = instruction.split(':')[1]
                print("[FEEDBACK] changing user, current user is now " + new_user_name)
                self.need_to_stop_instance = True
                self.user_name = new_user_name

            if "change_mode" in instruction:
                # instruction structure : "change_mode:new_mode:user_name" (user_name is optional, only for exploration)
                possible_modes = ['flow', 'exploration']
                new_mode = instruction.split(':')[1]

                if new_mode in possible_modes:
                    if new_mode != self.mode:
                        if new_mode == 'exploration':
                            if len(instruction.split(':')) < 3:
                                print("[FEEDBACK] couldn't change mode, user hasn't been specified")
                            else:
                                self.user_name = instruction.split(':')[2]
                                print("[FEEDBACK] changing user, current user is now " + self.user_name)

                                print("[FEEDBACK] changing mode, current mode is now " + new_mode)
                                self.need_to_stop_instance = True
                                self.mode = new_mode
                        else:
                            print("[FEEDBACK] changing mode, current mode is now " + new_mode)
                            self.need_to_stop_instance = True
                            self.mode = new_mode
                    else:
                        print("[FEEDBACK] current mode is already " + new_mode)
                else:
                    print("[FEEDBACK] instruction rejected, chosen mode: {} not in possible modes".format(new_mode))

    def instance_stopped(self):
        self.need_to_stop_instance = False
