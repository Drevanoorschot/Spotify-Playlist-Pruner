# Spotify playlist pruner
Spotify tool that helps you keep number of songs per user of a collaborative playlist in check

## Installation
1. clone the repo
2. run `pip install -r requirements.txt`
3. copy `config-example.py` to `config.py`
4. fill out config to your needs
5. run with `python pruner.py` (for now this will run a one time clean)
6. For a 15 second prune interval, add the following to your crontab:
```bash
* * * * * python3 {INSTALL_DIRECTORY}/pruner.py
* * * * * sleep 15; python3 {INSTALL_DIRECTORY}/pruner.py
* * * * * sleep 30; python3 {INSTALL_DIRECTORY}/pruner.py
* * * * * sleep 45; python3 {INSTALL_DIRECTORY}/pruner.py
```
