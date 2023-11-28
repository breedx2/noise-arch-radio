python3 playlist.py

# Download future files ahead of time
./download_ahead.sh 2>&1 > /dev/null &

# Clean up items more than 8 hours old
find data/items/ -type d -ctime .33 | xargs rm -rf 2>&1 > /dev/null
