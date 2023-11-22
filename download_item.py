import hashlib
import json
import os
import sys
import urllib.request

def download_item(id, quiet = False):
  meta_file = f'data/meta/{id}.json'
  file = open(meta_file, 'rt')
  meta = json.load(file)
  file.close()

  originals = [x for x in meta['files'] if x['source'] == 'original']

  if not os.path.exists('data/items'):
    os.mkdir('data/items')
  if not os.path.exists(f'data/items/{id}'):
    os.mkdir(f'data/items/{id}')

  originals = [x for x in originals if not x["name"].endswith('.xml')]

  for file in originals:
    url = f'https://archive.org/download/{id}/{file["name"]}'
    outfile = f'data/items/{id}/{file["name"]}'
    
    if os.path.exists(outfile):
      with open(outfile, 'rb', buffering=0) as f:
          sha = hashlib.file_digest(f, 'sha1').hexdigest()

      if file['sha1'] == sha:
        if not quiet:
          print(f'{outfile} exists and sha matches, skipping download')
        continue

    if not quiet:
      print(f'fetching {id} :: {file["name"]}')
    urllib.request.urlretrieve(url, outfile)


if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print('Argument required (identifier)')
    sys.exit(1)
  identifier = sys.argv[1]
  download_item(identifier)