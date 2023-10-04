from enum import Enum


class Relationship(Enum):
    NONE = 0
    HIERARCHICAL = 1
    EQUAL = 2
    HIERARCHICAL_TEMPORAL = 3
