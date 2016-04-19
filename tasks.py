from __future__ import unicode_literals

import sys

from invoke import run, task


@task
def test(coverage=False, watch=False, warn=False):
    if watch:
        return watcher(test, coverage=coverage)
    cmd = 'py.test'
    if coverage:
        cmd += ' --cov=spotifyconnect --cov-report=term-missing'
    run(cmd, pty=True, warn=warn)


@task
def preprocess_header():
    run(
        'cpp spotifyconnect/spotify.armv6l.h > '
        'spotifyconnect/spotify.processed.armv6l.h && '
        'sed -i "s/__extension__//g" spotifyconnect/spotify.processed.armv6l.h'
        )
    run(
        'cpp spotifyconnect/spotify.armv7l.h > '
        'spotifyconnect/spotify.processed.armv7l.h && '
        'sed -i "s/__extension__//g" spotifyconnect/spotify.processed.armv7l.h'
        )


def watcher(task, *args, **kwargs):
    while True:
        run('clear')
        kwargs['warn'] = True
        task(*args, **kwargs)
        try:
            run(
                'inotifywait -q -e create -e modify -e delete '
                '--exclude ".*\.(pyc|sw.)" -r spotifyconnect/ tests/')
        except KeyboardInterrupt:
            sys.exit()
