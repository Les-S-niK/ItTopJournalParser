
## Built-in modules: ##
from collections import defaultdict


class JournalObject(object):
    """Base JournalObject class."""


class JournalLesson(JournalObject):
    """Class with lesson information."""
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


class JournalShedule(JournalObject):
    """Journal object with the journal shedule and methods to manage it."""
    def __init__(
        self,
        shedule: list[dict],
    ) -> None:
        """Create a JournalShedule object.

        Args:
            shedule (list[dict]): Parsed unsorted journal shedule from API.
        """
        self.shedule: list[dict] = shedule
    
    def sort_shedule(self) -> None:
        """Sort the shedule by dates.

        Args: 
            shedule (dict): Unsorted shedule from the Journal API.
        """
        ## Date key in the dict for sorting the shedule. ##
        DATE_KEY: str = "date"
        shedule: list[dict] = self.shedule
        
        shedule.sort(key=lambda day_data: day_data.get(DATE_KEY))

        sorted_shedule: defaultdict[str, list[dict]] = defaultdict(list)

        for day_data in shedule:
            date_value: str = day_data.get(DATE_KEY)
            sorted_shedule[date_value].append(day_data)

        self.shedule = dict(sorted_shedule)


class JournalLeaderboard(JournalObject):
    """Journal object with the journal students leaderboard and methods to manage it."""
    def __init__(
        self,
        leaderboard: list[dict],
    ) -> None:
        """Create a JournalLeaderboard object.

        Args:
            leaderboard (list[dict]): Parsed leaderboard from the Journal API.
        """
        self.leaderboard: list[dict] = leaderboard\
    
    def cut_from_leaderboard(
        self,
        students_count: int,
        from_beginning: bool,
    ) -> None:
        """Cut students from the leaderboard.

        Args:
            students_count (int): Students count to cut.
            from_beginning (bool): if True - cut from the beginning, else - from the ending.
        """
        if students_count > len(self.leaderboard):
            self.leaderboard = []
        else:
            if from_beginning:
                self.leaderboard = self.leaderboard[students_count:]
            else: 
                self.leaderboard = self.leaderboard[:students_count]