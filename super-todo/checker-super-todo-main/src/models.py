from enum import Enum

class NoteFilter(Enum):
    ALL = "ALL"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"

class NoteSort(Enum):
    TIMESTAMP = "TIMESTAMP"
    COMPLETED_AT = "COMPLETED_AT"
