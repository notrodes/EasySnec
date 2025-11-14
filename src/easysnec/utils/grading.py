from __future__ import annotations
# from pydantic.dataclasses import dataclass
from dataclasses import dataclass
from enum import Enum
import datetime as dt

import uuid


class SuccessStatus(Enum):
    SUCCESS = 1
    INCOMPLETE = 2  # no start/finish time or start >= finish
    MISSES = 3  # or wrong order

@dataclass(frozen=True)
class InputData:
    card_id: int
    start_time: dt.datetime
    finish_time: dt.datetime
    punches: list[tuple[int, dt.datetime]]
    reading_id: str

    def score_against(self, course:Course):
        return get_correctness_of_course(self, course)

    @classmethod
    def from_si_result(self, si_result:dict):
        return InputData(
            card_id = si_result['card_number'],
            start_time = si_result['start'],
            finish_time = si_result['finish'],
            punches = si_result['punches'],
            reading_id = uuid.uuid5(),
            # other keys: 'check' (datetime), 'clear' (usually None)
        )

@dataclass(frozen=True)
class OutputData:
    # this is your test result - what you got right, what you got wrong
    course_name: str
    success_status: SuccessStatus
    missed_checkpoints: list[int]


@dataclass(frozen=True)
class Course:
    course_name: str
    is_score_o: bool
    stations: list[int]


def get_closest_course(card_data, courses):
    # fastDamerauLevenshtein
    # https://pypi.org/project/fastDamerauLevenshtein/#files
    s1 = [ punch[0] for punch in card_data['punches'] ]
    course_distances = {}

    for course in courses:
        s2 = course
        
        d: dict[tuple[int, int], int] = {}
        da: dict[T, int] = {}

        len1 = len(s1)
        len2 = len(s2)

        maxdist = len1 + len2
        d[-1, -1] = maxdist

        # matrix
        for i in range(len(s1) + 1):
            d[i, -1] = maxdist
            d[i, 0] = i
        for j in range(len(s2) + 1):
            d[-1, j] = maxdist
            d[0, j] = j

        for i, cs1 in enumerate(s1, start=1):
            db = 0
            for j, cs2 in enumerate(s2, start=1):
                i1 = da.get(cs2, 0)
                j1 = db
                if self.test_func(cs1, cs2):
                    cost = 0
                    db = j
                else:
                    cost = 1

                d[i, j] = min(
                    d[i - 1, j - 1] + cost,     # substitution (wrong station)
                    d[i, j - 1] + 1,            # insertion (missed station)
                    d[i - 1, j] + 1,            # deletion (extra station)
                    d[i1 - 1, j1 - 1] + (i - i1) - 1 + (j - j1),  # transposition (swapped stations)
                )

            da[cs1] = i

        course_distances[course] = d[len1, len2]

    return min(course_distances, key=course_distances.get)



def get_correctness_of_course(card_data, course):
    # todo: make buffer array that helps display which stations are wrong compared to correct course 
    # See: triResultatsScore() and getMissed() in ResultatPuce.java from EasyGecNG
    punches = [ punch[0] for punch in card_data['punches'] ]

    # temp solution
    return course == punches

        # buffer_string = ""
        # bufferBool = True
        # unsorted = True

        # while (unsorted):
        #     unsorted = False
        #     for i in range(len(punches)):
        #         if (punches[i] != punches[i + 1]):
        #             buffer_string = punches[i]
        #             punches[i] = punches[i + 1]
        #             punches[i + 1] = buffer_string
        #             unsorted = True
    

COURSES = [
    Course('Frog',      False,  [32, 40, 39, 38, 35, 34, 36, 37, 31, 33]),
    Course('Octopus',   False,  [34, 36, 39, 40, 32, 33, 37, 38, 31, 35]),
    Course('Penguin',   False,  [38, 39, 32, 34, 35, 36, 37, 33, 31, 40]),
    Course('Sheep',     False,  [40, 36, 34, 31, 32, 33, 35, 37, 38, 39]),
    Course('Lion',      False,  [31, 33, 36, 38, 39]),
    Course('Dog',       False,  [33, 32, 40, 38, 34]),
    Course('Bee',       False,  [35, 37, 38, 40, 33]),
    Course('Bird',      False,  [36, 34, 31, 38, 37]),
    Course('Elephant',  False,  [37, 34, 31, 40, 39]),
    Course('Crab',      False,  [39, 31, 32, 35, 37]),
]

ANIMAL_MAPPING = {
    'Frog': 32,
    'Octopus': 34,
    'Penguin': 38,
    'Sheep': 40,
    'Lion': 31,
    'Dog': 33,
    'Bee': 35,
    'Bird': 36,
    'Elephant': 37,
    'Crab': 39,
}

# This isnt real lol
CURRENT_COURSE = COURSES[9] # Crab