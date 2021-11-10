
import pandas as pd
import os
from typing import Union


class Answer:

    _path: str = None
    _n_seats: int = -1
    _fields = ['seat', 'name', 'surname', 'email', 'phone']

    name: str = 'None'
    surname: str = 'None'
    email: str = 'None'
    phone: str = 'None'
    seat: int = -1
    agree: bool = False


    def __init__(self, path, n_seats):
        self._path = path
        self._n_seats = n_seats


    def _remove_spaces(self):
        self.name = self.name.replace(' ', '')
        self.surname = self.surname.replace(' ', '')
        self.phone = self.phone.replace(' ', '')


    def get_available_seats(self) -> pd.Series:

        available_seats = pd.Series([True]*self._n_seats, index=pd.RangeIndex(1, self._n_seats+1))

        if os.path.exists(self._path):
            for x in pd.read_csv(self._path).seat.values:
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

        if not self.phone.lstrip('+').isdigit():
            return 'phone'

        if self.seat not in self.get_available_seats():
            return 'seat'

        if not self.agree:
            return 'agree'


    def save(self) -> Union[None,str]:

        self._remove_spaces()
        field = self.is_valid()

        if type(field) == str:
            return field

        if os.path.exists(self._path):
            df = pd.read_csv(self._path)
        else:
            df = pd.DataFrame(columns=self._fields)

        df = df.append(self.get_dict(), ignore_index=True)
        df = df.sort_values('seat')
        df.to_csv(self._path, index=False)

### class Answer ###
