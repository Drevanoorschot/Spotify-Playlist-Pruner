import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

import os

from mirror import Mirror
from pruner import Pruner

log_dir = "{home}/logs/".format(home=Path.home())

if not os.path.isdir(log_dir):
    print("no logging directory exists. Creating one...")
    os.makedirs(log_dir)

formatting = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler = RotatingFileHandler("{home}/logs/Spotify-pruner.log".format(home=Path.home()),
                              maxBytes=1024 * 1024,
                              backupCount=5)
handler.setFormatter(formatting)
logger = logging.Logger(name="API-calls")
logger.addHandler(handler)

p = Pruner()
m = Mirror()
if "prune" in sys.argv:
    p.prune_playlist()
    logger.info("playlist prune call completed")
if "image" in sys.argv:
    m.update_image()
    logger.info("image update call completed")
if "tracks" in sys.argv:
    m.update_tracks()
    logger.info("tracks update call completed")
if "title" in sys.argv:
    m.update_title()
    logger.info("title update call completed")
