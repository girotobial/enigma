"""Implements the rotors of the enigma machine"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Protocol, Type


class Rotor(Protocol):
    name: str
    forward_wiring: list[int]
    backward_wiring: list[int]
    rotor_position: int
    notch_position: int
    ring_setting: int

    def __init__(  # noqa too-many-arguments
        self,
        name: str,
        encoding: str,
        rotor_position: int,
        ring_setting: int,
        notch_position: int,
    ) -> None:
        ...

    def turnover(self) -> None:
        ...

    @property
    def is_at_rotor(self) -> bool:
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


class BasicRotor(Rotor):
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
    @dataclass(frozen=True)
    class RotorInput:
        encoding: str
        notch_position: int
        rotor_type: Type[Rotor]

    named_rotors_inputs = {
        NamedRotor.I: RotorInput("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16, BasicRotor),
        NamedRotor.II: RotorInput("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4, BasicRotor),
        NamedRotor.III: RotorInput("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21, BasicRotor),
        NamedRotor.IV: RotorInput("ESOVPZJAYQUIRHXLNFTGKDCMWB", 9, BasicRotor),
        NamedRotor.V: RotorInput("VZBRGITYUPSDNHLXAWMJQOFECK", 25, BasicRotor),
        NamedRotor.VI: RotorInput("JPGVOUMFYQBENHZRDKASXLICTW", 0, TwoNotchRotor),
        NamedRotor.VII: RotorInput("NZJHGRCXMYSWBOUFAIVLPEKQDT", 0, TwoNotchRotor),
        NamedRotor.VIII: RotorInput("FKQHTLXOCBJSPDZRAMEWNIUYGV", 0, TwoNotchRotor),
    }

    inputs = named_rotors_inputs[name]
    return inputs.rotor_type(
        str(name), inputs.encoding, rotor_position, ring_setting, inputs.notch_position
    )
