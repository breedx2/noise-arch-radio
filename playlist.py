import os
import random
import json
from download_item import download_item

# outputs the next playlist filename while maintaining the playlist.
# playlist is a text file, one identifier per line

PLAYLIST_FILE = 'data/playlist'
PLAYLIST_ITEM = 'data/playlist.item'
PLAYLIST_CURFILE = 'data/playlist.curfile'
PLAYLIST_NEXT = 'data/playlist.nextfiles'

def list_all_items():
  file_list = os.listdir('data/meta')
  files = [f for f in file_list if os.path.isfile(os.path.join('data/meta', f))]
  return [f.replace('.json', '') for f in files ]

def read_meta(id):
  with open(f'data/meta/{id}.json', 'rt') as file:
    return json.load(file)

# create a new randomized playlist from metadata items
def generate_playlist():
  items = list_all_items()
  random.shuffle(items)
  with open(PLAYLIST_FILE, 'wt') as out:
    for item in items:
      out.write(f'{item}\n')

# returns the top item in the playlist and overwrites
# the playlist file.
def pop_playlist():
  with open(PLAYLIST_FILE, 'rt') as file:
    lines = file.read().splitlines()
  item = lines[0]
  if len(lines) == 1:
    # remove to regenerate for next time
    os.remove(PLAYLIST_FILE)
  else:
    with open(PLAYLIST_FILE, 'wt') as file:
      file.write('\n'.join(lines[1:]))
  return item

def original_files(meta):
  return [x for x in meta['files'] if x['source'] == 'original']

def is_audio_format(format):
  return any(x in format.lower() for x in ['mp3', 'ogg', 'wav'])

def audio_files(meta):
  originals = original_files(meta)
  return [x for x in originals if is_audio_format(x['format'])]

def pop_next_file():
  with open(PLAYLIST_NEXT, 'rt') as file:
    lines = file.read().splitlines()
  if len(lines) == 1:
    # remove to regen next time
    os.remove(PLAYLIST_NEXT)
  else:
    with open(PLAYLIST_NEXT, 'wt') as file:
      file.write('\n'.join(lines[1:]))
  return lines[0]

## __main__ 

if not os.path.exists(PLAYLIST_FILE):
  generate_playlist()

if os.path.exists(PLAYLIST_NEXT):
  pass
else:
  item = pop_playlist()
  with open(PLAYLIST_ITEM, 'wt') as file:
    file.write(item)

  meta = read_meta(item)
  audio = audio_files(meta)
  audio_files = sorted([f'data/items/{item}/{x["name"]}' for x in audio])
  # print(audio_files)
  with open(PLAYLIST_NEXT, 'wt') as file:
    file.write('\n'.join(audio_files))

  download_item(item, quiet = True)

filename = pop_next_file()
with open(PLAYLIST_CURFILE, 'wt') as file:
  file.write(filename)
print(filename)

# TODO: Ensure next 3 downloaded in the hopper