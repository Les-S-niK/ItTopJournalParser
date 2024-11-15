
## Pip modules: ##
from fake_useragent import UserAgent

## Local modules: ##
from journal_request_data import parser_str_date


def get_random_useragent() -> str:
    """Get the random useragent from fake_useragent library.

    Returns:
        str: String with the useragent.
    """
    return UserAgent().random


def get_login_headers() -> dict:
    """Get the headers for POST request to Journal API with the random user-agent.

    Returns:
        dict: Headers dictionary.
    """
    user_agent: str = get_random_useragent()
    login_headers: dict = {
        "authority": "msapi.top-academy.ru",
        "method": "POST",
        "path": "/api/v2/auth/login",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru_RU, ru",
        "authorization": "Bearer null",
        "content-type": "application/json",
        "origin": "https://journal.top-academy.ru",
        "priority": "u=1, i",
        "referer": "https://journal.top-academy.ru/",
        "user-agent": user_agent
    }
    
    return login_headers


def get_headers_for_requests(
    token: str,
) -> dict:
    """Get the headers for any GET request to Journal API.
    Token needs to pass it in auth field.

    Args:
        token (str): Auth token. You can get it after logging in the Journal.

    Returns:
        dict: Headers dictionary.
    """

    user_agent: str = get_random_useragent()
    headers: dict = {
        "authority": "msapi.top-academy.ru",
        "method": "GET",
        "path": f"/api/v2/schedule/operations/get-month?date_filter={parser_str_date}",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru_RU, ru",
        "authorization": f"Bearer {token}",
        "origin": "https://journal.top-academy.ru",
        "priority": "u=1, i",
        "referer": "https://journal.top-academy.ru/",
        "user-agent": f"{user_agent}"
    }
    
    return headers
