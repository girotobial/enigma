"""Implements the rotors of the enigma machine"""

from __future__ import annotations

import enum
from collections import namedtuple
from typing import Protocol


class Rotor(Protocol):
    name: str
    forward_wiring: list[int]
    backward_wiring: list[int]
    rotor_position: int
    notch_position: int
    ring_setting: int
    is_at_notch: bool

    def turnover(self) -> None:
        ...


class NamedRotor(enum.Enum):
    I = enum.auto()  # noqa E741
    II = enum.auto()
    III = enum.auto()
    IV = enum.auto()
    V = enum.auto()
    VI = enum.auto()
    VII = enum.auto()
    VIII = enum.auto()


class BasicRotor:
    """A rotor in the enigma machine"""

    def __init__(  # noqa too-many-arguments
        self,
        name: str,
        encoding: str,
        rotor_position: int,
        ring_setting: int,
        notch_position: int,
    ) -> None:
        self.name = name
        self.forward_wiring = self._decode_wiring(encoding)
        self.backward_wiring = list(reversed(self.forward_wiring))
        self.rotor_position = rotor_position
        self.notch_position = notch_position
        self.ring_setting = ring_setting

    def turnover(self) -> None:
        """Turn the rotor"""
        self.rotor_position = (self.rotor_position + 1) % 26

    @staticmethod
    def _decode_wiring(encoding: str) -> list[int]:
        return list(map(lambda c: ord(c) - 65, encoding))

    @property
    def is_at_notch(self) -> bool:
        return self.rotor_position == self.notch_position


class TwoNotchRotor(BasicRotor):
    def __init__(  # noqa too-many-arguments
        self,
        name: str,
        encoding: str,
        rotor_position: int,
        ring_setting: int,
        notch_position: int,
    ) -> None:
        notch_position = 0
        super().__init__(name, encoding, rotor_position, ring_setting, notch_position)

    @property
    def is_at_notch(self) -> bool:
        return self.rotor_position in [12, 25]


def create_rotor(name: NamedRotor, rotor_position: int, ring_setting: int) -> Rotor:

    RotorInput = namedtuple("RotorInput", "encoding notch_position")
    named_rotors_inputs = {
        NamedRotor.I: RotorInput("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16),
        NamedRotor.II: RotorInput("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4),
        NamedRotor.III: RotorInput("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21),
        NamedRotor.IV: RotorInput("ESOVPZJAYQUIRHXLNFTGKDCMWB", 9),
        NamedRotor.V: RotorInput("VZBRGITYUPSDNHLXAWMJQOFECK", 25),
        NamedRotor.VI: RotorInput("JPGVOUMFYQBENHZRDKASXLICTW", 0),
        NamedRotor.VII: RotorInput("NZJHGRCXMYSWBOUFAIVLPEKQDT", 0),
        NamedRotor.VIII: RotorInput("FKQHTLXOCBJSPDZRAMEWNIUYGV", 0),
    }

    inputs = named_rotors_inputs[name]
    return BasicRotor(
        str(name), inputs.encoding, rotor_position, ring_setting, inputs.notch_position
    )
