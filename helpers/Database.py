
import helpers.User

import pandas as pd
import random
import string
import os


class Database:

    """Manages prenotations file."""

    __n_seats: int = -1
    __path: str = "prenotations.csv"
    __fields = ["seat", "name", "surname", "email", "time"]


    def __init__(self, n_seats: int, path: str = None):
        self.__n_seats = n_seats
        if path != None: self.__path = path


    def __generate_id(self, length: int = 8) -> str:
        return "".join(random.sample(string.ascii_letters + string.digits, k=length))


    def __save_df(self, df: pd.DataFrame):
        df.to_csv(self.__path)


    def get_df(self) -> pd.DataFrame:
        if os.path.exists(self.__path):
            return pd.read_csv(self.__path, index_col="id")
        else:
            return pd.DataFrame(columns=self.__fields, index=pd.Index([], name="id"))


    def is_valid(self, user: helpers.User.User) -> str:

        if not user.name.isalpha():
            return "name"

        if not user.surname.isalpha():
            return "surname"

        if " " in user.email or "@" not in user.email or "." not in user.email.split("@")[-1]:
            return "email"

        if user.seat not in self.get_available_seats():
            return "seat"

        if not user.agree:
            return "agree"

        return "valid"


    def get_available_seats(self) -> pd.Series:

        available_seats = pd.Series([True]*self.__n_seats, index=pd.RangeIndex(1, self.__n_seats+1))

        if os.path.exists(self.__path):
            for x in self.get_df().seat.values:
                available_seats.loc[x] = False

        return available_seats.loc[available_seats.values].index


    def register(self, user: helpers.User.User) -> str:

        field = self.is_valid(user)

        if field != "valid":
            return field

        df = self.get_df()

        id = self.__generate_id()
        while id in df.index.tolist():
            id = self.__generate_id()

        prenotation = user.get_dict()

        # check if already registered
        if df.loc[lambda x: x.name == prenotation["name"]].loc[lambda x: x.surname == prenotation["surname"]].shape[0] != 0:
            return "already"

        df = df.append(pd.Series(prenotation, name=id))
        df = df.sort_values("seat")
        self.__save_df(df)

        return id


    def remove(self, id: str) -> int:

        df = self.get_df()
        n_before = df.shape[0]

        df = df.drop(id)
        n_after = df.shape[0]

        self.__save_df(df)

        return n_before - n_after
