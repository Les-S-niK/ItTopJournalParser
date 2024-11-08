"""This code uses options from the .env file.
To make this code work, you need to authorize in the Journal API by visiting the URL https://journal.top-academy.ru/ru/auth/login/index
and obtain your JSON information from the network manager (press Ctrl + Shift + I -> Network). After logging in, 
you will see the "login" Fetch/XHR action. 
Then, you need to copy this information to the .env file in the same directory as this script.
It should look like this:
APPLICATION_KEY = YOUR_APP_KEY
ID_CITY = YOUR_ID_CITY (sometimes it can be null).
PASSWORD = YOUR_PASSWORD
USER_NAME = YOUR_USERNAME
"""

## Built-in modules: ## 
from os import getenv
from os import path
from os import PathLike
from dataclasses import dataclass
from datetime import datetime
from typing import Generator

## Pip modules: ##
from dotenv import load_dotenv


ENV_FILE_PATH: PathLike = f"{path.dirname(__file__)}/.env"
## Load all environment variables from .env file: ##
load_dotenv(dotenv_path=ENV_FILE_PATH)

## Get the date with this format: year-month-day ##
TODAY_DATE: datetime = datetime.now().strftime('%Y-%m-%d')
## Keys for urls: ##
SHEDULE_KEY: str = "shedule"
LEADERBOARD_KEY: str = "leaderboard"


@dataclass
class JournalUrlsConfig(object):
    """Config with all the URLS that we need to parse.

    Args:
        object (class): Basic inheritance class.
    """
    ## First value in dict - url, second - variable name in JournalParser class.
    LOGIN_URL: str = ("https://msapi.top-academy.ru/api/v2/auth/login", "login")
    SHEDULE_URL: str = (f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter={TODAY_DATE}", SHEDULE_KEY)
    GROUP_LEADERBOAR_URL: str = ("https://msapi.top-academy.ru/api/v2/dashboard/progress/leader-group", LEADERBOARD_KEY)


    def __iter__(self) -> Generator[str, None, None]:
        """Simple generator to iterate over all the URLs in the config.

        Yields:
            Generator[str, None, None]: Yields all the public URLS.
        """
        for url in list(self.__dict__.values()):
            yield url


def create_json_for_request() -> dict:
    """Create a dict with all the necessary data for the request.

    Returns:
        dict: Dictionary with data for POST request to login API.
    
    Raises:
        ValueError: If data in .env file is incorrect.
    """
    APPLICATION_KEY: str = getenv("APPLICATION_KEY")
    ID_CITY: str = getenv("ID_CITY")
    PASSWORD: str = getenv("PASSWORD")
    USERNAME: str = getenv("USER_NAME")
    
    if not all((APPLICATION_KEY, ID_CITY, PASSWORD, USERNAME)):
        raise ValueError("Some of the .env args are not set. You need to create .env file in one DIR with this script.")
    
    json_data: dict = {
        "application_key": APPLICATION_KEY,
        "id_city": ID_CITY,
        "password": PASSWORD,
        "username": USERNAME
    }
    
    
    return json_data