
import json
import os
from internetarchive import search_items, get_item


COLLECTION = 'noise-arch'

print(f'Fetching identifiers for {COLLECTION}')
results = search_items(f'collection:{COLLECTION}')
identifiers = [x['identifier'] for x in results]
print(f'Fetched {len(identifiers)} potential identifiers')

if not os.path.exists('data/meta'):
  os.mkdir('data/meta')

for id in identifiers:
  print(f'Fetching metadata for {id}')
  item = get_item(id)
  meta = item.item_metadata
  originals = [x for x in meta['files'] if x['source'] == 'original']
  print(f'  item has {len(originals)} original files')
  mp3s = [x for x in originals if 'mp3' in x['format'].lower()]
  if len(mp3s) > 0:
    print(f'  {id} has {len(mp3s)} mp3 files')
    out = open(f'data/meta/{id}.json', 'wt')
    out.write(json.dumps(meta, indent=2))
    out.close()
  else:
    print(f'  {id} has no mp3 files, skipping...')

