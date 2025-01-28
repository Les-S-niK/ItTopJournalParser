
## Local modules: ##
from journal_parser import JournalParser
from config.journal_request_data import create_json_for_request
from shedule_table_image.journal_shedule_table import SheduleImage
from config.journal_response_data import get_sorted_shedule
from os import getenv


APPLICATION_KEY: str = getenv("APPLICATION_KEY")
ID_CITY: str = getenv("ID_CITY")
PASSWORD: str = getenv("PASSWORD")
USERNAME: str = getenv("USER_NAME")

LOGIN_USER_DATA: dict = create_json_for_request(
    application_key=APPLICATION_KEY,
    id_city=ID_CITY,
    password=PASSWORD,
    user_name=USERNAME,
)

parser: JournalParser = JournalParser(
    login_json_data=LOGIN_USER_DATA
)

shedule: dict = parser.shedule
sorted_shedule: dict = get_sorted_shedule(shedule=shedule)

shedule_image: SheduleImage = SheduleImage(shedule=sorted_shedule)
shedule_image.save_shedule_to_png()