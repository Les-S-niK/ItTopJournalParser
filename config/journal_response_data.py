
## Built-in modules: ##
from dataclasses import dataclass

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
