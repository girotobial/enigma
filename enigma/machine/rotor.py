"""Implements the rotors of the enigma machine"""

from __future__ import annotations


class Rotor:
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
