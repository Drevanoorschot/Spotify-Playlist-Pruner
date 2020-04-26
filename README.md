# Spotify playlist pruner
Spotify tool that helps you keep number of songs per user of a collaborative playlist in check.
Also supports the mirroring of playlists to add the possibility to make a collaborative playlist public.
The pruner does requirer to setup your own Spotify API developer keys.

## Installation
1. clone the repo
2. copy `config-example.py` to `config.py`
3. fill out config to your needs
4. run `python main.py` with one (or more) of the following arguments (space seperated):
    - `pruner` for playlist pruning
    - `image` for updating mirrors playlist cover image
    - `tracks` for updating mirrors playlist tracks (removes old tracks and adds new tracks)
    - `title` for updating mirrors playlist title (removes any substring containing `" (private)"` too)

It is advised to setup a crontab for periodic updates