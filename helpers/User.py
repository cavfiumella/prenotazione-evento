
class User:

    """User data."""

    __fields = ["seat", "name", "surname", "email", "time"]

    name: str = "None"
    surname: str = "None"
    email: str = "None"
    seat: int = -1
    agree: bool = False
    time: str = "None"


    def get_dict(self) -> dict:
        cmd = "{"
        for field in self.__fields:
            cmd += f"\"{field}\": self.{field},"
        cmd = cmd[:-1] + "}"
        return eval(cmd)
