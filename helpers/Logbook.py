
"""Logbook of admins operations."""

import helpers.time


class Logbook:

    _path: str = None


    def __init__(self, path: str = 'book.log'):
        self._path = path


    def log(self, s: str):
        s = helpers.time.format(helpers.time.now()) + ' - ' + s + '\n'
        with open(self._path, mode='a') as file:
            file.write(s)


    def read(self) -> str:
        with open(self._path, mode='r') as file:
            return file.read()

### class Logbook ###
