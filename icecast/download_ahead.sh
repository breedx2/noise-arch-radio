#!/bin/bash

for item in $(head -3 data/playlist) ; do
  python3 download_item.py $item
done