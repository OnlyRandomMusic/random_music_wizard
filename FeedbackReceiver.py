import threading
import communication.Receiver
import queue

volume_step = 4  # the volume step in percentage


class FeedbackReceiver(threading.Thread):
    def __init__(self, player, song_chooser):
        """instructions_queue is a list of instructions in order to communicate with the main"""
        threading.Thread.__init__(self)
        self.player = player
        self.song_chooser = song_chooser
        self.stop = False

        self.instructions_queue = queue.Queue()
        self.receiver = communication.Receiver.Receiver(self.instructions_queue)
        self.receiver.daemon = True

    def run(self):
        print("[RASP] waiting for instructions")
        while True:
            self.receiver.receive()

            if self.instructions_queue.qsize() > 0:
                instruction = self.instructions_queue.get()
                self.decode_instruction(instruction)

            # print("[RASP] received instruction " + instruction)

    def decode_instruction(self, instruction):
        if "+" in instruction:
            step_number = instruction.count("+")
            volume = self.player.increase_volume(step_number * volume_step)
            print("[RASP] volume is now {}%".format(volume))

        if "-" in instruction:
            step_number = instruction.count("-")
            volume = self.player.increase_volume(- step_number * volume_step)
            print("[RASP] volume is now {}%".format(volume))

        if "next" in instruction:
            done = self.player.play_next_music(-0.5)
            if done:
                print("[RASP] the music has been changed")
            else:
                print("[RASP] the music can't be changed now")

        if "close" in instruction:
            self.stop = True
            print("[RASP] program ended")

        if "search" in instruction:
            research = instruction.split(':')
            # instruction structure : "search:research_text:(1 or 0)" last boolean to indicate if the music should be play immediatly or not
            self.song_chooser.play_search(research[1], int(research[2]))

        if "play" in instruction:
            self.player.play()

        if "pause" in instruction:
            self.player.pause()

        if "like" in instruction:
            self.player.explorer.set_score(self.player.current_music_id, 1)
