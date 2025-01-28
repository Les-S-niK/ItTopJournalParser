# ItTopJournalParser
The Journal Parser, that gets some information from the public API.

You can use it for parsing shedule and leaderboard endpoints.
Additionaly, there is easy way to create shedule table .png image using the SheduleImage class:
-> from shedule_table_image.journal_shedule_table import SheduleImage

Usage example:
```
## Creating simple shedule table:
from journal_parser import JournalParser
from config.journal_request_data import create_json_for_request
from shedule_table_image.journal_shedule_table import SheduleImage
from config.journal_response_data import get_sorted_shedule


## You can insert your own data right here, but using the .env can help secure your data. 
APPLICATION_KEY: str = getenv("APPLICATION_KEY")
ID_CITY: str = getenv("ID_CITY")
PASSWORD: str = getenv("PASSWORD")
USERNAME: str = getenv("USER_NAME")

LOGIN_USER_DATA: dict = create_json_for_request(
    application_key=APPLICATION_KEY,
    id_city=ID_CITY,
    password=PASSWORD,
    username=USERNAME,
)

parser: JournalParser = JournalParser(
    login_json_data=LOGIN_USER_DATA
)

## Get shedule and sort it.
shedule: dict = parser.shedule
sorted_shedule: dict = get_sorted_shedule(shedule=shedule)
## Create shedule table image. 
shedule_image: SheduleImage = SheduleImage(shedule=sorted_shedule)
shedule_image.save_shedule_to_png()
```
