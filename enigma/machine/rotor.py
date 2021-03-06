"""Implements the rotors of the enigma machine"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol, Type, overload

from .. import core
from . import wiring


class Rotor(Protocol):
    name: str
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
    def is_at_notch(self) -> bool:
        ...

    @overload
    def forward(self, value: int) -> int:
        ...

    @overload
    def forward(self, value: str) -> str:
        ...

    def forward(self, value: core.Encypherable) -> core.Encypherable:
        ...

    @overload
    def backward(self, value: int) -> int:
        ...

    @overload
    def backward(self, value: str) -> str:
        ...

    def backward(self, value: core.Encypherable) -> core.Encypherable:
        ...

    @property
    def forward_wiring(self) -> wiring.Wiring:
        ...

    @property
    def backward_wiring(self) -> wiring.Wiring:
        ...


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
        self.wiring = wiring.Wiring(encoding)
        self.rotor_position = rotor_position
        self.notch_position = notch_position
        self.ring_setting = ring_setting

    def turnover(self) -> None:
        """Turn the rotor"""
        self.rotor_position = (self.rotor_position + 1) % 26

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.name}, {self.wiring.encoding},"
            f" {self.rotor_position}, {self.notch_position}, {self.ring_setting})"
        )

    @property
    def forward_wiring(self) -> wiring.Wiring:
        return self.wiring

    @property
    def backward_wiring(self) -> wiring.Wiring:
        return self.wiring.inverse()

    @property
    def is_at_notch(self) -> bool:
        return self.rotor_position == self.notch_position

    def _encipher(self, value: int, wiring_: Sequence[int]) -> int:
        shift: int = self.rotor_position - self.ring_setting
        return (wiring_[(value + shift + 26) % 26] - shift + 26) % 26

    def _encipher_char(self, value: str, wiring_: Sequence[int]) -> str:
        int_val = core.character_to_int(value)
        return core.int_to_char(self._encipher(int_val, wiring_))

    @overload
    def forward(self, value: int) -> int:
        ...

    @overload
    def forward(self, value: str) -> str:
        ...

    def forward(self, value: core.Encypherable) -> core.Encypherable:
        if isinstance(value, str) and len(value) == 1:
            return self._encipher_char(value, self.forward_wiring)

        if isinstance(value, int):
            return self._encipher(value, self.forward_wiring)
        raise NotImplementedError

    @overload
    def backward(self, value: int) -> int:
        ...

    @overload
    def backward(self, value: str) -> str:
        ...

    def backward(self, value: core.Encypherable) -> core.Encypherable:
        if isinstance(value, str) and len(value) == 1:
            return self._encipher_char(value, self.backward_wiring)

        if isinstance(value, int):
            return self._encipher(value, self.backward_wiring)
        raise NotImplementedError


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


def create_rotor(
    name: core.NamedRotor, rotor_position: int, ring_setting: int
) -> Rotor:
    @dataclass(frozen=True)
    class RotorInput:
        encoding: str
        notch_position: int
        rotor_type: Type[Rotor]

    named_rotors_inputs = {
        core.NamedRotor.I: RotorInput("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16, BasicRotor),
        core.NamedRotor.II: RotorInput("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4, BasicRotor),
        core.NamedRotor.III: RotorInput("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21, BasicRotor),
        core.NamedRotor.IV: RotorInput("ESOVPZJAYQUIRHXLNFTGKDCMWB", 9, BasicRotor),
        core.NamedRotor.V: RotorInput("VZBRGITYUPSDNHLXAWMJQOFECK", 25, BasicRotor),
        core.NamedRotor.VI: RotorInput("JPGVOUMFYQBENHZRDKASXLICTW", 0, TwoNotchRotor),
        core.NamedRotor.VII: RotorInput("NZJHGRCXMYSWBOUFAIVLPEKQDT", 0, TwoNotchRotor),
        core.NamedRotor.VIII: RotorInput(
            "FKQHTLXOCBJSPDZRAMEWNIUYGV", 0, TwoNotchRotor
        ),
    }

    inputs = named_rotors_inputs[name]
    return inputs.rotor_type(
        str(name), inputs.encoding, rotor_position, ring_setting, inputs.notch_position
    )
