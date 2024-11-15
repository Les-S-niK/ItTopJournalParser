
## Built-in modules: ##
from textwrap import fill
from dataclasses import dataclass
from datetime import datetime

## Pip modules: ##
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont
from PIL.ImageDraw import ImageDraw as ImgDraw

## Local modules: ##
from journal_request_data import dir_path, parser_date
from journal_response_data import JournalLesson


@dataclass
class SheduleImagePreferences(object):
    """A dataclass for all shedule Image prefs. 

    Args:
        object (class): Basic inheritance class.
    """
    IMG_WIDTH: int = 1920
    IMG_HEIGHT: int = 1080
    WEEK_DAYS: tuple[str] = ("Пн", "Вт", "Ср", "Чт", "Пт")
    CELL_WIDTH: int = IMG_WIDTH // len(WEEK_DAYS)
    CELL_HEIGHT: int = 206  
    HEADER_HEIGHT: int = 50
    
    FONT_SIZE: int = 20
    HEADER_FONT: FreeTypeFont = ImageFont.truetype(
        font="LiberationSans-Bold.ttf",
        size=FONT_SIZE + 5
    )
    TEXT_FONT: FreeTypeFont = ImageFont.truetype(
        font="LiberationSans-Bold.ttf",
        size=FONT_SIZE
    )

    HEADER_COLOR: tuple[int] = (200, 200, 255) 
    CELL_COLOR: tuple[int] = (240, 240, 240)
    BORDER_COLOR: tuple[int] = (0, 0, 0)        
    TEXT_COLOR: tuple[int] = (0, 0, 0)


class SheduleImage(object):
    """A shedule image, that creates by the shedule from the JournalAPI.

    Args:
        object (class)
    """
    ## Get the image prefs from 
    image_prefs: SheduleImagePreferences = SheduleImagePreferences()
    
    def __init__(
        self,
        shedule: dict,
    ) -> None:
        """Initialize class, that uses PIL to create table with shedule.

        Args:
            shedule (dict): shedule dictionary from json Journal response.
        """
        self.shedule: dict = shedule
        self.image: Image = Image.new(
            mode='RGB',
            size=(
                self.image_prefs.IMG_WIDTH,
                self.image_prefs.IMG_HEIGHT
            ),
            color=(255, 255, 255)
        )
        self.drawed_image: ImgDraw = ImageDraw.Draw(self.image)
        self._create_table_with_shedule()
        
        return None


    def save_shedule_to_png(self) -> None:
        """Save the shedule image to png file.
        """
        self.image.save(f'{dir_path}/shedule_table.png')


    def _create_table_with_shedule(self) -> None:
        """
        Create the table image using PIL library.
        We create table and passing the values from the shedule in it there.
        """
        self.__delete_old_dates()

        for index, day in enumerate(self.image_prefs.WEEK_DAYS):
            x: int = index * self.image_prefs.CELL_WIDTH
            y: int = 0 
            self.drawed_image.rectangle(
                [
                    x,
                    y,
                    x + self.image_prefs.CELL_WIDTH,
                    self.image_prefs.HEADER_HEIGHT
                ],
                fill=self.image_prefs.HEADER_COLOR
            )
            
            bbox: tuple[float] = self.drawed_image.textbbox(
                (x, y),
                day,
                font=self.image_prefs.HEADER_FONT
            )
            
            self.drawed_image.text(
                (
                    x + (self.image_prefs.CELL_WIDTH - bbox[2] + bbox[0]) / 2,
                    y + (self.image_prefs.HEADER_HEIGHT - (bbox[3] - bbox[1])) / 2),
                day,
                fill=self.image_prefs.TEXT_COLOR,
                font=self.image_prefs.HEADER_FONT
            )

        for index, lessons_day in zip(range(len(self.image_prefs.WEEK_DAYS)), list(self.shedule.values())):
            
            placed_lessons: list[bool] = [False] * 5

            for lesson_info in lessons_day:
                lesson: JournalLesson = JournalLesson(lesson_info)
                lesson_number: int = lesson.number - 1

                if 0 <= lesson_number < 5:
                    text = f"""
{fill(lesson.subject_name, width=20)},
{lesson.start_time} - {lesson.end_time},
Аудитория: {fill(lesson.room_name, width=20)},
Препод: {fill(lesson.teacher_name, width=20)}
                    """
                    x: int = index * self.image_prefs.CELL_WIDTH
                    y: int = self.image_prefs.HEADER_HEIGHT + lesson_number * self.image_prefs.CELL_HEIGHT

                    self.drawed_image.rectangle(
                        [
                            x,
                            y,
                            x + self.image_prefs.CELL_WIDTH,
                            y + self.image_prefs.CELL_HEIGHT
                        ],
                        outline=self.image_prefs.BORDER_COLOR,
                        fill=self.image_prefs.CELL_COLOR
                    )

                    self.drawed_image.text(
                        (
                            x + 10,
                            y + 10
                        ),
                        text,
                        fill=self.image_prefs.TEXT_COLOR,
                        font=self.image_prefs.TEXT_FONT
                    )
                    
                    placed_lessons[lesson_number] = True

        return None


    def __delete_old_dates(self) -> None:
        """Delete old lesson dates from the shedule.
        """
        for day_date in list(self.shedule.keys()):
            date: list[str] = day_date.split("-")
            if parser_date > datetime(
                year=int(date[0]),
                month=int(date[1]),
                day=int(date[2])
            ): 
                del self.shedule[day_date]
        
        return None