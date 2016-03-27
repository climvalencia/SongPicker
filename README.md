song_picker
===========

Builds a random setlist from its internal 'choices' file. The script assigns weights to each song to ensure less played songs are picked more often, and often played songs are picked less frequently.

No strict formatting needed when loading a new songs file, just needs 1 song per line.

You can take a look at the choices file to see the probability of each song to be picked when building a setlist.


Usage
=====
```python
$> python song_picker.py pick 3
['Boston - More than a Feeling',
 'Red Hot Chili Peppers - Californication',
 'Metallica - Nothing Else Matters']
```

Go and play!


Comments
========
This project was created as an exercise in self-learning Python and was mainly motivated by me needing a free tool to build random setlists for my guitar practice sessions.
