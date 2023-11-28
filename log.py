from datetime import datetime
import os

LOGFILE = 'data/playlist.log'

def log(msg):
  ts = datetime.now().replace(microsecond=0).isoformat()
  pid = os.getpid()
  with open(LOGFILE, 'at') as file:
    file.write(f'{ts} [{pid}]: {msg}\n')
