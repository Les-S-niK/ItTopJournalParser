
## Built-in modules: ## 
from os.path import dirname
from os import PathLike
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator

## Pip modules: ##
from dotenv import load_dotenv


dir_path: PathLike = dirname(__file__)
env_file_path: PathLike = f"{dir_path}/.env"
## Load all environment variables from .env file: ##
load_dotenv(dotenv_path=env_file_path)

## Get the date with this format: year-month-day ##
today_date: datetime = datetime.now()
## Add one day to today_date 'cause we need to get data for tomorrow day: ##
next_day: datetime = today_date + timedelta(days=1)

if not next_day.weekday() == 0:
    parser_date: datetime = today_date - timedelta(days=next_day.weekday())


parser_str_date: str = parser_date.strftime('%Y-%m-%d')


## Keys for urls: ##
SHEDULE_KEY: str = "shedule"
LEADERBOARD_KEY: str = "leaderboard"
LOGIN_KEY: str = "login"


@dataclass
class JournalUrlsConfig(object):
    """Config with all the URLS that we need to parse.

    Args:
        object (class): Basic inheritance class.
    """
    ## First value in dict - url, second - variable name in JournalParser class.
    LOGIN_URL: str = ("https://msapi.top-academy.ru/api/v2/auth/login", LOGIN_KEY)
    SHEDULE_URL: str = (f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter={parser_str_date}", SHEDULE_KEY)
    GROUP_LEADERBOAR_URL: str = ("https://msapi.top-academy.ru/api/v2/dashboard/progress/leader-group", LEADERBOARD_KEY)

    def __iter__(self) -> Generator[str, None, None]:
        """Simple generator to iterate over all the URLs in the config.

        Yields:
            Generator[str, None, None]: Yields all the public URLS.
        """
        for url in list(self.__dict__.values()):
            yield url


def create_json_for_request(
    application_key: str,
    id_city: str,
    password: str,
    username: str,
) -> dict[str, str]:
    """Create the dict with all the necessary data for the request.

    Returns:
        dict[str, str]: Dictionary with the necessary data for POST request to the login API.
"""
    json_data: dict = {
        "application_key": application_key,
        "id_city": id_city,
        "password": password,
        "username": username,
    }
    
    return json_data