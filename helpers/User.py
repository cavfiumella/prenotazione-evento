
# non-admin user operations


from . import time as helpers_time

import pandas as pd
import os
import random
import string
from typing import Union


class User:

    _path: str = None
    _n_seats: int = -1
    _fields = ['seat', 'name', 'surname', 'email', 'time']

    name: str = 'None'
    surname: str = 'None'
    email: str = 'None'
    seat: int = -1
    agree: bool = False
    time: str = 'None'


    def __init__(self, path, n_seats):
        self._path = path
        self._n_seats = n_seats


    def _remove_spaces(self):
        self.name = self.name.strip()
        self.surname = self.surname.strip()


    def _generate_id(self, length: int = 8) -> str:
        return ''.join(random.sample(string.ascii_letters + string.digits, k=length))


    def _get_df(self) -> pd.DataFrame:
        if os.path.exists(self._path):
            return pd.read_csv(self._path, index_col='id')
        else:
            return pd.DataFrame(columns=self._fields, index=pd.Index([], name='id'))


    def _set_time(self) -> None:
        self.time = helpers_time.format(helpers_time.now())


    def get_available_seats(self) -> pd.Series:

        available_seats = pd.Series([True]*self._n_seats, index=pd.RangeIndex(1, self._n_seats+1))

        if os.path.exists(self._path):
            for x in self._get_df().seat.values:
                available_seats.loc[x] = False

        return available_seats.loc[available_seats.values].index


    def get_dict(self) -> dict:
        cmd = '{'
        for field in self._fields:
            cmd += f'"{field}": self.{field},'
        cmd = cmd[:-1] + '}'
        return eval(cmd)


    def is_valid(self) -> Union[None,str]:

        if not self.name.isalpha():
            return 'name'

        if not self.surname.isalpha():
            return 'surname'

        if ' ' in self.email or '@' not in self.email or '.' not in self.email.split('@')[-1]:
            return 'email'

        if self.seat not in self.get_available_seats():
            return 'seat'

        if not self.agree:
            return 'agree'


    def save(self) -> str:

        self._remove_spaces()
        field = self.is_valid()

        if type(field) == str:
            return field

        df = self._get_df()

        id = self._generate_id()
        while id in df.index.tolist():
            id = self._generate_id()

        # set prenotation time
        self._set_time()

        prenotation = self.get_dict()

        # check if already registered
        if df.loc[lambda x: x.name == prenotation['name']].loc[lambda x: x.surname == prenotation['surname']].shape[0] != 0:
            return 'already'

        df = df.append(pd.Series(prenotation, name=id))
        df = df.sort_values('seat')
        df.to_csv(self._path)

        return id

### class User ###
