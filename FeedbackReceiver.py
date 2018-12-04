import threading

volume_step = 4  # the volume step in percentage


class FeedbackReceiver(threading.Thread):
    def __init__(self, player):
        """instructions_queue is a list of instructions in order to communicate with the main"""
        threading.Thread.__init__(self)
        self.player = player

    def run(self):
        print("[RASP] waiting for instructions")
        while True:
            instruction = input()
            decode_instruction(instruction, self.player)
            # print("[RASP] received instruction " + instruction)


def decode_instruction(instruction, player):
    if "+" in instruction:
        step_number = instruction.count("+")
        player.increase_volume(step_number * volume_step)
        print("[RASP] volume increased by {}%".format(step_number * volume_step))
    if "-" in instruction:
        step_number = instruction.count("-")
        player.increase_volume(- step_number * volume_step)
        print("[RASP] volume decreased by {}%".format(step_number * volume_step))
