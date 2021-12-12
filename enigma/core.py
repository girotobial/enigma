"""Common objects used by both analysis and machine"""


import enum
from dataclasses import dataclass, field


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
    rotors: list[NamedRotor] = field(default_factory=list)
    indicators: list[int] = field(default_factory=list)
    rings: list[int] = field(default_factory=list)
    plugboard: str = ""

    def __post_init__(self) -> None:
        if len(self.rotors) == 0:
            self.rotors = [NamedRotor.I, NamedRotor.II, NamedRotor.III]
        if len(self.indicators) == 0:
            self.indicators = [0, 0, 0]
        if len(self.rings) == 0:
            self.rings = [0, 0, 0]


def character_to_int(char: str) -> int:
    return ord(char) - 65


def int_to_char(val: int) -> str:
    return chr(val + 65)
