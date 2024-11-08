
## Local modules: ##
from journal_request_data import create_json_for_request
from journal_request_data import SHEDULE_KEY, LEADERBOARD_KEY
from journal_parser import JournalPasrser


def get_sorted_shedule(parser_obj: JournalPasrser) -> list[dict]:
    """Get the shedule from the JournalParser and sort it.

    Returns:
        list[dict]: sorted dictionary woth shedule data.
    """
    ## Check if shedule data is in parser attrs.
    if SHEDULE_KEY not in parser_obj.parsed_attr_names:
        return None
    
    shedule: list[dict] = getattr(parser_obj, SHEDULE_KEY)
    shedule.sort(key=lambda day_data: day_data.get("date"))

    return shedule