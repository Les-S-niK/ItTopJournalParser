
## Pip modules: ##
from requests import Session, Response
from requests.exceptions import RequestException

## Local modules: ##
from config.journal_headers import get_login_headers, get_headers_for_requests
from config.journal_request_data import JournalUrlsConfig
from journal_request_logger import request_logger


class JournalParser(object):
    """ItTopJournal parser. It parses the data from the ItTopJournal API.

    Args:
        object (class): Basic inheritance class.
    """
    def __init__(
        self,
        login_json_data: dict
    ) -> None:
        """Journal Parser initialization for parsing the data from the ItTopJournal API
        There will be a new self. attrs with parsed information from API. You can check all of them with self.parsed_attr_names.

        Args:
            login_json_data (dict): dict object with 4 fields:
            You can get all of it in the JournalAPI. 
            https://journal.top-academy.ru/ru/auth/login/index
            
            APPLICATION_KEY = YOUR_APP_KEY
            ID_CITY = YOUR_ID_CITY (sometimes it can be "null").
            PASSWORD = YOUR_PASSWORD
            USER_NAME = YOUR_USERNAME
        """
        self.JOURNAL_URLS: JournalUrlsConfig = JournalUrlsConfig()
        
        ## Get all the URLS from UrlsConfig dataclass and delete the login url: ##
        URLS_TO_GET_DATA: list[str] = [url for url in JournalUrlsConfig()]
        URLS_TO_GET_DATA.remove(self.JOURNAL_URLS.LOGIN_URL)
        self.parsed_attr_names: list = [variable_name for _, variable_name in URLS_TO_GET_DATA]

        with Session() as session:
            access_token: str = self._login_in_journal_api(
                session=session,
                login_json_data=login_json_data
            )
            request_headers: dict = get_headers_for_requests(token=access_token) 
            ## Set new self attrs for each in list url: ##
            for url, var_name in URLS_TO_GET_DATA:
                setattr(
                    self,
                    var_name,
                    self._get_request_to_journal(
                        url=url,
                        headers=request_headers,
                        session=session
                    )
                )
        
        return None


    @staticmethod
    def check_response_status(response: Response) -> None:
        """Check the response status. If the status is not in 200-299, it raises an exception.
        
        Args:
            response (Response): response object. You can get it after request to api.
        
        Raises: 
            RequestException: if response.status_code is not in range 200-299.
        """
        if not response.ok:
            raise RequestException(f"Failed to login in the JournalApi. Status code: {response.status_code}")

        return None


    @request_logger
    def _get_request_to_journal(
        self,
        url: str,
        session: Session,
        headers: dict
    ) -> dict:
        """Universal get request to journal API.

        Args:
            url: (str): URL for the request.
            session (Session): requests.Session object.
            headers (dict): Headers with the access token from login request.

        Returns:
            dict: Json data from API.
        """
        response: Response = session.get(
            url=url,
            headers=headers
        ) 
        self.check_response_status(response=response)
        
        return response.json()


    @request_logger
    def _login_in_journal_api(
        self,
        session: Session,
        login_json_data: dict
    ) -> str:
        """Logging in the JournalApi with json data and get the token after login.

        Args:
            session (Session): requests.Session object.
            
        Returns:
            str: API token.
        """
        login_headers: dict = get_login_headers()
        
        response: Response = session.post(
            url=self.JOURNAL_URLS.LOGIN_URL[0],
            headers=login_headers,
            json=login_json_data
        )
        self.check_response_status(response=response)
        
        ## Get the token from API response: ##
        TOKEN_DICT_KEY: str = "access_token"
        access_token: str = response.json().get(TOKEN_DICT_KEY)
        
        return access_token
