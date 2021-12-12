from typing import overload

from enigma import core
from enigma.machine.wiring import Wiring


class Plugboard:
    def __init__(self, connections: str) -> None:
        self.wiring = self._decode_plugboard(connections)

    def _forward_int(self, char: int) -> int:
        return self.wiring[char]

    @overload
    def forward(self, char: int) -> int:
        ...

    @overload
    def forward(self, char: str) -> str:
        ...

    def forward(self, char: core.Encypherable) -> core.Encypherable:
        if isinstance(char, int):
            return self._forward_int(char)
        if isinstance(char, str):
            char_int = core.character_to_int(char)
            encoded = self._forward_int(char_int)
            return core.int_to_char(encoded)
        raise NotImplementedError

    @staticmethod
    def _identity_plugboard() -> Wiring:
        return Wiring._from_decoded(list(range(26)))  # noqa protected-access

    def _decode_plugboard(self, connections: str) -> Wiring:
        if connections == "":
            return self._identity_plugboard()  # noqa protected-access

        pairings = connections.split("[^a-zA-Z]")
        plugged_characters: set[int] = set()

        mapping = self._identity_plugboard()

        for pair in pairings:
            if len(pair) != 2:
                return self._identity_plugboard()

            char1 = core.character_to_int(pair[0])
            char2 = core.character_to_int(pair[2])

            if char1 in plugged_characters or char2 in plugged_characters:
                return self._identity_plugboard()

            plugged_characters.add(char1)
            plugged_characters.add(char2)

            mapping[char1] = char2
            mapping[char2] = char1

        return mapping
