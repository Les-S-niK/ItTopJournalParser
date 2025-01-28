
## Built-in modules: ##
from dataclasses import dataclass


def get_sorted_shedule(shedule: dict) -> list[dict]:
    """Get the shedule from the JournalParser and sort it.

    Args: 
        shedule (dict): Unsorted shedule from Journal API.

    Returns:
        list[dict]: sorted dictionary woth shedule data.
    """
    ## The date key in the dict. ##
    DATE_KEY: str = "date"
    shedule.sort(key=lambda day_data: day_data.get(DATE_KEY))
    
    sorted_shedule: dict[str, list[dict]] = {}
    
    for day_data in shedule:
        ## Sorting the shedule dict by date. ##
        date_value: str = day_data.get(DATE_KEY)
        if date_value not in sorted_shedule:
            sorted_shedule[date_value] = [day_data]
        else:
            sorted_shedule[date_value].append(day_data)

    return sorted_shedule


@dataclass
class JournalLesson(object):
    """Class with lesson room_name, date, end etc.

    Args:
        object (class): Base inhetitance class.
    """
    def __init__(
        self,
        lesson: dict 
    ) -> None:
        """Set lesson attributes from the dictionary lesson object from a shedule. 

        Args:
            lesson (dict): The lesson from the Journal shedule.
        """
        self.date: str = lesson.get("date")
        self.start_time: str = lesson.get("started_at")
        self.end_time: str = lesson.get("finished_at")
        self.room_name: str = lesson.get("room_name")
        self.subject_name: str = lesson.get("subject_name")
        self.teacher_name: str = lesson.get("teacher_name")
        self.number: int = lesson.get("lesson")
    
    
    def __repr__(self) -> str:
        """Return a lesson subject name.

        Returns:
            str: Subject name.
        """
        return self.subject_name