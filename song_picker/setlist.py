MAX_RETRIES = 3

class Setlist(object):

    def __init__(self, choices_file):
        self.choices_file = choices_file

    def pick(self, how_many, max_retries=MAX_RETRIES):
        """
        Returns a list of songs according to the number provided.
        """
        if not (how_many > 0):
            raise ValueError("Number of songs must be greater than 0")

        songs = []
        current_retries = 0

        while current_retries < max_retries:
            song = self.choices_file.pick()
            if song in songs:
                current_retries += 1
            else:
                songs.append(song)
                current_retries = 0
                if len(songs) == how_many:
                    break
        return songs
