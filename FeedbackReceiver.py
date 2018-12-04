import threading

volume_step = 4  # the volume step in percentage


class FeedbackReceiver(threading.Thread):
    def __init__(self, player):
        """instructions_queue is a list of instructions in order to communicate with the main"""
        threading.Thread.__init__(self)
        self.player = player
        self.stop = False

    def run(self):
        print("[RASP] waiting for instructions")
        while True:
            instruction = input()
            self.decode_instruction(instruction)
            # print("[RASP] received instruction " + instruction)

    def decode_instruction(self, instruction):
        if "help" in instruction:
            print("""+  increase the volume
-   decrease the volume
next   go to the next music
quit   exit the program""")

        if "+" in instruction:
            step_number = instruction.count("+")
            volume = self.player.increase_volume(step_number * volume_step)
            print("[RASP] volume is now {}%".format(volume))

        if "-" in instruction:
            step_number = instruction.count("-")
            volume = self.player.increase_volume(- step_number * volume_step)
            print("[RASP] volume is now {}%".format(volume))

        if "next" in instruction:
            self.player.play_next_music()
            print("[RASP] the music has been changed")

        if "quit" in instruction:
            self.stop = True
            print("[RASP] program ended")
