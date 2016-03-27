import argparse
from pprint import pprint
from song_picker.choices_file import ChoicesFile
from song_picker.setlist import Setlist

DEFAULT_CHOICES_FILE_PATH = './storage/choices'

class prepare(object):
    def __init__(self, path):
        self.c = ChoicesFile(path)

    def __enter__(self):
        self.c.load()
        return self.c

    def __exit__(self, type, value, traceback):
        self.c.save()

def handle_pick(args):
    with prepare(args.choices_file) as c:
        s = Setlist(c)
        songs = s.pick(args.songs)
        pprint(songs)

def handle_add(args):
    with prepare(args.choices_file) as c:
        c.add(args.song)

def handle_remove(args):
    with prepare(args.choices_file) as c:
        c.remove(args.song)

def handle_load(args):
    c = ChoicesFile(args.choices_file)
    c.load_raw(args.songs_file)
    c.save()

def set_up_arg_parsers():
    parser = argparse.ArgumentParser(description="Random setlist generator.")
    parser.add_argument(
        '-f', '--file',
        metavar='',
        dest='choices_file',
        default=DEFAULT_CHOICES_FILE_PATH,
        help='Path to internal choices file (default: storage/choices)',
    )

    subparsers = parser.add_subparsers(title='Commands', metavar="")

    # pick command
    parser_pick = subparsers.add_parser('pick', help='Randomly pick a number of songs')
    parser_pick.set_defaults(func=handle_pick)
    parser_pick.add_argument(
        'songs',
        metavar='SONGS',
        type=int,
        help='Number of songs to pick',
    )

    # add command
    parser_add = subparsers.add_parser('add', help='Add a new song to storage')
    parser_add.set_defaults(func=handle_add)
    parser_add.add_argument(
        'song',
        metavar='SONG',
        help='Add a new song to storage with format ARTIST - TITLE',
    )

    # remove command
    parser_remove = subparsers.add_parser('remove', help='Remove a song from storage')
    parser_remove.set_defaults(func=handle_remove)
    parser_remove.add_argument(
        'song',
        metavar='SONG',
        help='Remove a song from storage with format ARTIST - TITLE',
    )

    # load command
    parser_load = subparsers.add_parser('load', help='Load new songs from file')
    parser_load.set_defaults(func=handle_load)
    parser_load.add_argument(
        'songs_file',
        metavar='FILEPATH',
        help='Path to a list of songs to load. Separated by newlines.',
    )

    return parser.parse_args()

args = set_up_arg_parsers()
args.func(args)
