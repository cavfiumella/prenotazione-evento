
import pandas as pd
from typing import Union


class Admin:

    """Admin operations class."""

    __credentials: pd.DataFrame = pd.DataFrame()


    def __init__(self, credentials: Union[pd.DataFrame,dict]):

        # parse dict
        if type(credentials) == dict:
            credentials = pd.DataFrame(credentials)

        # validate dataframe
        for col in ["username", "password"]:
            if col not in credentials.columns.tolist():
                raise ValueError("invalid credentials")

        self.__credentials = credentials


    def auth(self, username: str, password: str) -> bool:

        """Return True if user is registered and credentials are correct,
           False otherwise."""

        # look for user
        if username not in self.__credentials.username.tolist():
            return False

        # check password
        return password == self.__credentials.loc[lambda x: x.username == username].password.values[0]

### class Admin ###
