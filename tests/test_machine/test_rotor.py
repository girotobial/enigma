"""Tests for the rotor of the enigma machine"""

from dataclasses import dataclass

import pytest

from enigma.machine import rotor


def test_rotor_intializes() -> None:
    """GIVEN a set of inputs

    THEN the rotor intializes
    AND stores that data
    """
    test_rotor = rotor.BasicRotor(
        name="Test",
        encoding="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        rotor_position=1,
        notch_position=2,
        ring_setting=3,
    )
    assert test_rotor.name == "Test"
    assert test_rotor.rotor_position == 1
    assert test_rotor.notch_position == 2
    assert test_rotor.ring_setting == 3
    assert test_rotor.forward_wiring == list(range(26))
    assert test_rotor.backward_wiring == list(reversed(list(range(26))))


@dataclass(frozen=True)
class _RotorAttrs:
    forward_wiring: list[int]
    notch_position: int


def _encode(string: str) -> list[int]:
    return list(map(lambda c: ord(c) - 65, string))


ROTOR_ENCODINGS = {
    rotor.NamedRotor.I: _RotorAttrs(_encode("EKMFLGDQVZNTOWYHXUSPAIBRCJ"), 16),
    rotor.NamedRotor.II: _RotorAttrs(_encode("AJDKSIRUXBLHWTMCQGZNPYFVOE"), 4),
    rotor.NamedRotor.III: _RotorAttrs(_encode("BDFHJLCPRTXVZNYEIWGAKMUSQO"), 21),
    rotor.NamedRotor.IV: _RotorAttrs(_encode("ESOVPZJAYQUIRHXLNFTGKDCMWB"), 9),
    rotor.NamedRotor.V: _RotorAttrs(_encode("VZBRGITYUPSDNHLXAWMJQOFECK"), 25),
    rotor.NamedRotor.VI: _RotorAttrs(_encode("JPGVOUMFYQBENHZRDKASXLICTW"), 0),
    rotor.NamedRotor.VII: _RotorAttrs(_encode("NZJHGRCXMYSWBOUFAIVLPEKQDT"), 0),
    rotor.NamedRotor.VIII: _RotorAttrs(_encode("FKQHTLXOCBJSPDZRAMEWNIUYGV"), 0),
}


@pytest.mark.parametrize(("name", "expected_attrs"), list(ROTOR_ENCODINGS.items()))
def test_create_rotor_with_a_historic_configuration(name, expected_attrs) -> None:
    """GIVEN a rotor
    WHEN create_rotor is called with a historic configuration name.
    THEN intialize a rotor with that configuration
    """
    rotor_t: rotor.Rotor = rotor.create_rotor(name, 1, 2)
    assert rotor_t.forward_wiring == expected_attrs.forward_wiring
    assert rotor_t.name == str(name)
    assert rotor_t.notch_position == expected_attrs.notch_position
    assert rotor_t.rotor_position == 1
    assert rotor_t.ring_setting == 2


class TestBasicRotor:
    @pytest.fixture
    def basic_rotor(self) -> rotor.Rotor:  # noqa no-self-use
        return rotor.BasicRotor("Test", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1, 2, 3)

    def test_is_at_notch_is_false(self, basic_rotor) -> None:  # noqa no-self-use
        assert basic_rotor.is_at_notch is False

    def test_is_at_notch_is_true(self, basic_rotor) -> None:  # noqa no-self-use
        basic_rotor.notch_position = 1
        assert basic_rotor.is_at_notch is True
