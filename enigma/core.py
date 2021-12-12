"""Common objects used by both analysis and machine"""


import enum
from dataclasses import dataclass


class NamedRotor(enum.Enum):
    I = enum.auto()  # noqa E741
    II = enum.auto()
    III = enum.auto()
    IV = enum.auto()
    V = enum.auto()
    VI = enum.auto()
    VII = enum.auto()
    VIII = enum.auto()


@dataclass
class EnigmaKey:
    rotors: list[NamedRotor] = [NamedRotor.I, NamedRotor.II, NamedRotor.III]
    indicators: list[int] = [0, 0, 0]
    rings: list[int] = [0, 0, 0]
    plugboard: str = ""
