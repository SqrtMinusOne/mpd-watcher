# mpd-watcher
A simple Python script to log [mpd](https://www.musicpd.org/) activity in csv format.

## Usage
Set the `LOG_FILE` variable to whereever you want to store the log and install the script. The program is way too tiny to make a separate config.

The connection to mpd drops from time to time for some reason, so the script will exit only if faced 10 (`EXCEPTION_COUNT`) exceptions in a minute. Which should happen only if mpd is actually not running.

The number of saved attributes can be extended via the `CUSTOM_ATTRS` variable.

Installation:
```bash
pip install .
```

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

The `get_lock` function uses [Linux domain sockets](https://stackoverflow.com/a/7758075) to prevent multiple instances of the script running concurrently.
