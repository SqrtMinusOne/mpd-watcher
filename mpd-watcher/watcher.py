import csv
import os

from datetime import datetime, timedelta

from mpd import MPDClient

LOG_FILE = '/home/pavel/.mpd/mpd-watcher-log.csv'
LISTENED_THRESHOLD = 0.5

current_song = None

def write_song(song):
    time_listened = (datetime.now() - song['start_time']).seconds
    duration = float(song['duration'])
    if (time_listened / duration > LISTENED_THRESHOLD):
        evt_type = 'listened'
    else:
        evt_type = 'skipped'

    event = {
        'file': song['file'],
        'artist': song.get('artist', ''),
        'album_artist': song.get('albumartist', ''),
        'title': song.get('title', ''),
        'album': song.get('album'),
        'time': song['start_time'].isoformat(' ', 'seconds'),
        'type': evt_type
    }

    fieldnames = event.keys()
    log_exists = os.path.exists(LOG_FILE)
    mode = 'a' if log_exists else 'w'
    with open(LOG_FILE, mode) as f:
        writer = csv.DictWriter(f, fieldnames)
        if not log_exists:
            writer.writeheader()
        writer.writerow(event)


def get_current_song(mpd: MPDClient):
    status = mpd.status()
    song = mpd.currentsong()
    if song:
        time_elapsed = float(status['elapsed'])
        song['start_time'] = datetime.now() - timedelta(seconds=int(time_elapsed))
    return song


def watch(mpd: MPDClient):
    global current_song

    while True:
        song = get_current_song(mpd)

        if not current_song:
            current_song = song
        elif not song or (song and song['file'] != current_song['file']):
            write_song(current_song)
            current_song = song

        mpd.idle('player')

def connect():
    mpd = MPDClient()
    mpd.connect('localhost', 6600)
    return mpd

if __name__ == "__main__":
    last_error = datetime.now()
    error_count = 0

    while True:
        try:
            mpd = connect()
            watch(mpd)
        except Exception as exp:
            if (datetime.now() - last_error).seconds > 60:
                error_count = 0
            last_error = datetime.now()
            error_count += 1
            if error_count > 10:
                raise exp

