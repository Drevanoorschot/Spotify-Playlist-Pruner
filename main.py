import logging
import sys

from mirror import Mirror
from pruner import Pruner

# logging.basicConfig(
#     filename="logs.log",
#     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
# )
formatting = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler = logging.FileHandler("logs.log")
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
