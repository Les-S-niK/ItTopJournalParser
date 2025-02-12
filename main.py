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

## Local modules: ##
from journal_parser import JournalParser
from config import create_json_for_request
from journal_shedule_table import SheduleImage
from os import getenv


APPLICATION_KEY: str = getenv("APPLICATION_KEY")
ID_CITY: str = getenv("ID_CITY")
PASSWORD: str = getenv("PASSWORD")
USERNAME: str = getenv("USER_NAME")
FILENAME: str = "shedule_image"

LOGIN_USER_DATA: dict = create_json_for_request(
    application_key=APPLICATION_KEY,
    id_city=ID_CITY,
    password=PASSWORD,
    username=USERNAME,
)

parser: JournalParser = JournalParser(login_json_data=LOGIN_USER_DATA)

parser.shedule_object.sort_shedule()
journal_shedule: list[dict] = parser.shedule_object.shedule

journal_leaderboard: list[dict] = parser.leaderboard_object.leaderboard

shedule_image = SheduleImage(shedule=journal_shedule)
shedule_image.save_shedule_to_png(filename="shedule_image")