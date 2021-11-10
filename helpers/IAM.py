
# Identity and Access Manager for admin access


import pandas as pd
from typing import Union


class IAM:

    _credentials: pd.DataFrame = pd.DataFrame()


    def __init__(self, credentials: Union[pd.DataFrame,dict]):

        # parse dict
        if type(credentials) == dict:
            credentials = pd.DataFrame(credentials)

        # validate dataframe
        for col in ['username', 'password']:
            if col not in credentials.columns.tolist():
                raise ValueError('invalid credentials')

        self._credentials = credentials


    def auth(self, username: str, password: str) -> bool:

        '''Return True if user is registered and credentials are correct,
           False otherwise'''

        # look for user
        if username not in self._credentials.username.tolist():
            return False

        # check password
        return password == self._credentials.loc[lambda x: x.username == username].password.values[0]

### class IAM ###
