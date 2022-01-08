# mpd-watcher
A simple Python script to log [mpd](https://www.musicpd.org/) activity in csv format.

## Usage
Installation:
```bash
pip install .
```

Put the configuration file to cwd or `~/.config/mpd-watcher/settings.toml`. Example config:
```toml
log_folder = '/home/pavel/logs-sync/mpd/logs'
exception_timeout = 5
exception_count = 10
listened_threshold = 0.5
custom_attrs = ['musicbrainz_albumid', 'musicbrainz_artistid', 'musicbrainz_trackid']
```

Set the `log_folder` variable to wherever you want to store the log and install the script. The program is way too tiny to make a separate config.

The connection to MPD drops from time to time for some reason, so the script will exit only if faced 10 (`exception_count`) exceptions in a minute. This should happen only if MPD is actually not running.

The number of saved attributes can be extended via the `custom_attrs` variable.

`listened_threshold` determines the percent of the file after which it is considered "listened".


Start: `mpd_watcher` or `python -m mpd_watcher`

Example [supervisor](http://supervisord.org/configuration.html) config:
```ini
[program:mpd-watcher]
command=/home/pavel/Programs/miniconda3/bin/python -m mpd_watcher
autostart=true
autorestart=true
stopsignal=KILL
```

## Requirements
* Python >= 3.6
* [python-mpd2](https://pypi.org/project/python-mpd2/)

The `get_lock` function uses [Linux domain sockets](https://stackoverflow.com/a/7758075) to prevent multiple instances of the script from running concurrently.
