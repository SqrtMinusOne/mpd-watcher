import csv
import logging
import os
import socket
import sys
import time
from datetime import datetime, timedelta

from mpd import MPDClient

# LOG_FILE = '/home/pavel/.mpd/mpd-watcher-log.csv'
LOG_FOLDER = '/home/pavel/logs-sync/mpd/logs/'
EXCEPTION_TIMEOUT = 5
EXCEPTION_COUNT = 10
LISTENED_THRESHOLD = 0.5
CUSTOM_ATTRS = [
    'musicbrainz_albumid', 'musicbrainz_artistid', 'musicbrainz_trackid'
]

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    stream=sys.stdout)

current_song = None


def get_log_filename():
    return os.path.join(
        LOG_FOLDER,
        f'{datetime.now().strftime("%Y-%m-%d")}-{socket.gethostname()}-log.csv'
    )


def get_lock(process_name):
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        get_lock._lock_socket.bind('\0' + process_name)
        logging.info('Got the lock')
    except socket.error:
        logging.info('Lock already exists, exiting')
        sys.exit()


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
        'type': evt_type,
        **{attr: song.get(attr, '')
           for attr in CUSTOM_ATTRS}
    }

    fieldnames = event.keys()
    log_file = get_log_filename()
    log_exists = os.path.exists(log_file)
    mode = 'a' if log_exists else 'w'
    with open(log_file, mode) as f:
        writer = csv.DictWriter(f, fieldnames)
        if not log_exists:
            writer.writeheader()
            logging.info('Initialized CSV log')
        writer.writerow(event)
        logging.info('Saved an entry')


def get_current_song(mpd: MPDClient):
    status = mpd.status()
    song = mpd.currentsong()
    if song and status['state'] != 'stop':
        time_elapsed = float(status['elapsed'])
        song['start_time'] = datetime.now() - timedelta(
            seconds=int(time_elapsed))
        return song
    return None


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
    logging.info('Connect successful, running')
    return mpd


def main():
    last_error = datetime.now()
    error_count = 0

    get_lock('mpd_watcher')

    while True:
        try:
            mpd = connect()
            watch(mpd)
        except Exception as exp:
            logging.error(repr(exp))
            logging.error('Waiting %s seconds, error count: %s',
                          EXCEPTION_TIMEOUT, error_count)
            time.sleep(EXCEPTION_TIMEOUT)

            if (datetime.now() - last_error).seconds > 60:
                error_count = 0
            last_error = datetime.now()
            error_count += 1
            if error_count > EXCEPTION_COUNT:
                raise exp


if __name__ == "__main__":
    main()
