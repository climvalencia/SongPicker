import random

RETUNE_FACTOR = 0.5
SEPARATOR = ' - '

class ChoicesFile(object):

    def __init__(self, path=None):
        self.file_path = path
        self.temp_choices = {}

    def load_raw(self, raw_file_path):
        """
        Reads lines from a separate file and assigns default weights
        to them.
        """
        with open(raw_file_path, 'r') as open_file:
            choices = open_file.read().splitlines()
        weight = 1.0 / len(choices)
        temp_choices = {}
        for choice in iter(choices):
            temp_choices[choice] = float(weight)
        self.temp_choices = temp_choices

    def load(self):
        """
        Reads lines from a choices file and overwrites the current
        list of choices in memory.
        """
        with open(self.file_path, 'r') as open_file:
            raw_choices = open_file.read().splitlines()
        temp_choices = {}
        for raw_choice in iter(raw_choices):
            (weight, choice) = self._string_to_choice(raw_choice)
            temp_choices[choice] = float(weight)
        self.temp_choices = temp_choices

    def save(self):
        """
        Writes to the choices file the current list of choices.
        """
        with open(self.file_path, 'w+') as open_file:
            for temp_choice, weight in self.temp_choices.iteritems():
                open_file.write(self._choice_to_string(temp_choice, weight))

    def add(self, new_choice):
        """
        Rebalances all weights in the current list of choices and adds
        the new choice with a given normalized default weight.
        """
        if new_choice in self.temp_choices:
            return

        temp_choices = dict(self.temp_choices)
        total = 0
        length = len(temp_choices)
        weight_per_choice = length / float(length + 1)

        for temp_choice, weight in temp_choices.iteritems():
            new_weight = weight * weight_per_choice
            self.temp_choices[temp_choice] = new_weight
            total += new_weight
        self.temp_choices[new_choice] = 1 - total

    def remove(self, choice):
        """
        Removes the choice and rebalances all weights in the
        remaining list of choices.
        """
        try:
            weight_removed = self.temp_choices.pop(choice)
        except KeyError:
            return

        length = len(self.temp_choices)
        if length == 0:
            return

        temp_choices = dict(self.temp_choices)
        weight_per_choice = weight_removed / length
        for temp_choice, weight in temp_choices.iteritems():
            new_weight = weight + weight_per_choice
            self.temp_choices[temp_choice] = new_weight

    def pick(self):
        """
        Returns a random weighted choice from the list of choices.

        Rebalances weights in the choices per pick so that the last
        picked choice is less likely to be picked again, while
        increasing the likelyhood of all other choices to be picked.
        """
        temp_choices = dict(self.temp_choices)
        total = sum(w for (c, w) in temp_choices.iteritems())
        r = random.uniform(0, total)
        upto = 0
        for c, w in temp_choices.iteritems():
            if upto + w > r:
                self._retune_choices(w, c, self.temp_choices)
                return c
            upto += w
        assert False, "Shouldn't get here"

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, new_file_path):
        self.file_path = new_file_path

    def _retune_choices(self, weight, choice, choices):
        if len(choices) == 1:
            return

        new_weight = weight * RETUNE_FACTOR
        increment_weight = new_weight / (len(choices) - 1)
        choices_copy = dict(choices)
        for c, w in choices_copy.iteritems():
            if c != choice:
                choices[c] = w + increment_weight
            elif c == choice:
                choices[c] = new_weight

    def _choice_to_string(self, choice, weight):
        return str(weight) + SEPARATOR + choice + '\n'

    def _string_to_choice(self, string):
        return string.split(SEPARATOR, 1)
