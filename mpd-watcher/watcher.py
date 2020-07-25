from mpd import MPDClient
from datetime import datetime, timedelta

current_song = None

def write_song(song):
    print(song)

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

