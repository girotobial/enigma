from __future__ import annotations

from typing import overload

from .. import core
from . import plugboard, reflector, rotor


class EnigmaMachine:
    def __init__(
        self,
        rotors: list[rotor.Rotor],
        reflector_: reflector.Reflector,
        plugboard_: plugboard.Plugboard = plugboard.Plugboard(""),
    ):
        self.rotors = rotors
        self.reflector = reflector_
        self.plugboard = plugboard_

    @classmethod
    def from_key(cls, key: core.EnigmaKey) -> EnigmaMachine:
        rotors = [
            rotor.create_rotor(name, position, ring_setting)
            for name, position, ring_setting in zip(
                key.rotors, key.indicators, key.rings
            )
        ]
        plugboard_ = plugboard.Plugboard(key.plugboard)

        return cls(rotors, reflector.Reflector.create("B"), plugboard_)

    def rotate(self) -> None:
        def rotate_rotors(rotors: list[rotor.Rotor]) -> list[rotor.Rotor]:
            rightmost_rotor = rotors[-1]

            if rightmost_rotor.is_at_notch and len(rotors) != 1:
                rotors[:-1] = rotate_rotors(rotors[:-1])

            rightmost_rotor.turnover()
            return rotors

        self.rotors = rotate_rotors(self.rotors)

    @overload
    def _encrypt(self, character: int) -> int:
        ...

    @overload
    def _encrypt(self, character: str) -> str:
        ...

    def _encrypt(self, character: core.Encypherable) -> core.Encypherable:
        self.rotate()

        for rotor_ in self.rotors:
            character = rotor_.forward(character)

        character = self.reflector.forward(character)

        for rotor_ in reversed(self.rotors):
            character = rotor_.backward(character)

        return character

    def encrypt(self, message: str) -> str:
        return "".join((self._encrypt(char) for char in message))
