from setuptools import setup, find_packages

setup(
    name='mpd_watcher',
    version='1.0.0',
    description='A program to log MPD activity in CVS format',
    author='SqrtMinusOne',
    author_email='thexcloud@gmail.com',
    packages=find_packages(),
    install_requires=['python-mpd2'],
    entry_points='''
    [console_scripts]
    mpd_watcher=mpd_watcher.watcher:main
    '''
)
