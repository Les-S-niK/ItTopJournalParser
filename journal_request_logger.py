
## Built-in modules: ##
from typing import Callable
from functools import wraps
from time import time
from os import PathLike

## Pip modules: ##
from loguru import logger

## Local modules: ##
from config.journal_request_data import dir_path


LOGGER_PATH: PathLike = f"{dir_path}/LOGS.log"
## Add and set the logger instanse. ##
logger.add(
    sink=LOGGER_PATH,
    colorize=True,
    level="DEBUG",
    compression="zip",
    rotation="1 MB"
)
## Logging the logger initialization: ##
logger.info(f"Logger was initialized. Logs path: {LOGGER_PATH}")


def request_logger(function: Callable) -> Callable:
    """Request logger for logging the requests to Journal API.

    Args:
        function (Callable): request function.

    Returns:
        Callable: Wrapper function.
    """
    @wraps(function)
    def wrapper(*args, **kwargs) -> dict:
        """Request function wrapper, logs the request and returns the response.

        Returns:
            dict: response.json object.
        """
        start_time: float = time()
        logger.debug(f">>> Running request {function.__name__}...")
        try:
            json_response: dict = function(*args, **kwargs)
            end_time: float = time() - start_time
            logger.debug(f""">>> Succesful response from {function.__name__}. 
                Took time: {round(end_time, 2)} sec.
                """)
            
            return json_response
        
        except Exception as error:
            logger.critical(f">>> An error was occured in {function.__name__} request. \n Error: {error}.")
            raise Exception(error)
    
    return wrapper