import os
import sys

from dynaconf import Dynaconf

settings_files = [
    'settings.toml',
    os.path.expanduser('~/.config/mpd-watcher/settings.toml')
]

if all([not os.path.exists(p) for p in settings_files]):
    print(
        'No config file found. Install one at ~/.config/mpd-watcher/settings.toml'
    )
    sys.exit(1)

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=settings_files,
)
