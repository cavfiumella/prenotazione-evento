
import helpers.time


class Logbook:

    """Logbook of admins operations."""

    __path: str = "logbook"


    def __init__(self, path: str = "logbook"):
        self.__path = path


    def log(self, s: str):
        s = f"{helpers.time.format(helpers.time.now())} - {s}\n"
        with open(self.__path, mode="a") as file:
            file.write(s)


    def read(self) -> str:
        with open(self.__path, mode="r") as file:
            return file.read()

### class Logbook ###
