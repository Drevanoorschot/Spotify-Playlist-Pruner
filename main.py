import sys

from mirror import Mirror
from pruner import Pruner

p = Pruner()
m = Mirror()
if "prune" in sys.argv:
    p.prune_playlist()
if "image" in sys.argv:
    m.update_image()
if "tracks" in sys.argv:
    m.update_tracks()
if "title" in sys.argv:
    m.update_title()
