"""The reflector component of an enigma machine"""

from __future__ import annotations

from typing import overload

from .. import core
from . import wiring


class Reflector:
    def __init__(self, encoding: str):
        self.wiring = wiring.Wiring(encoding)

    def _forward_int(self, value: int) -> int:
        return self.wiring[value]

    @overload
    def forward(self, value: str) -> str:
        ...

    @overload
    def forward(self, value: int) -> int:
        ...

    def forward(self, value: core.Encypherable) -> core.Encypherable:
        if isinstance(value, int):
            return self._forward_int(value)
        if isinstance(value, str) and len(value) == 1:
            value_int = core.character_to_int(value)
            enciphered = self._forward_int(value_int)
            return core.int_to_char(enciphered)
        raise NotImplementedError

    @classmethod
    def create(cls, name: str) -> Reflector:
        encodings = {
            "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
        }

        if (encoding := encodings.get(name)) is None:
            encoding = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
        return cls(encoding)
