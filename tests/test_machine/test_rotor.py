"""Tests for the rotor of the enigma machine"""

from dataclasses import dataclass

import pytest

from enigma import core
from enigma.machine import rotor, wiring


@dataclass(frozen=True)
class _RotorAttrs:
    forward_wiring: wiring.Wiring
    notch_position: int


ROTOR_ENCODINGS = {
    core.NamedRotor.I: _RotorAttrs(wiring.Wiring("EKMFLGDQVZNTOWYHXUSPAIBRCJ"), 16),
    core.NamedRotor.II: _RotorAttrs(wiring.Wiring("AJDKSIRUXBLHWTMCQGZNPYFVOE"), 4),
    core.NamedRotor.III: _RotorAttrs(wiring.Wiring("BDFHJLCPRTXVZNYEIWGAKMUSQO"), 21),
    core.NamedRotor.IV: _RotorAttrs(wiring.Wiring("ESOVPZJAYQUIRHXLNFTGKDCMWB"), 9),
    core.NamedRotor.V: _RotorAttrs(wiring.Wiring("VZBRGITYUPSDNHLXAWMJQOFECK"), 25),
    core.NamedRotor.VI: _RotorAttrs(wiring.Wiring("JPGVOUMFYQBENHZRDKASXLICTW"), 0),
    core.NamedRotor.VII: _RotorAttrs(wiring.Wiring("NZJHGRCXMYSWBOUFAIVLPEKQDT"), 0),
    core.NamedRotor.VIII: _RotorAttrs(wiring.Wiring("FKQHTLXOCBJSPDZRAMEWNIUYGV"), 0),
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


@pytest.mark.parametrize(
    "name", [core.NamedRotor.VI, core.NamedRotor.VII, core.NamedRotor.VIII]
)
def test_create_rotor_vi_vii_viii_are_double_notched(name):
    t_rotor = rotor.create_rotor(name, 12, 0)
    assert t_rotor.is_at_notch
    t_rotor.rotor_position = 25
    assert t_rotor.is_at_notch


class TestBasicRotor:
    @staticmethod
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
        expected_wiring = wiring.Wiring("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        assert test_rotor.forward_wiring == expected_wiring
        assert test_rotor.backward_wiring == expected_wiring.inverse()

    @pytest.fixture
    def basic_rotor(self) -> rotor.BasicRotor:  # noqa no-self-use
        return rotor.BasicRotor("Test", "JPGVOUMFYQBENHZRDKASXLICTW", 1, 2, 3)

    def test_is_at_notch_is_false(self, basic_rotor) -> None:  # noqa no-self-use
        assert basic_rotor.is_at_notch is False

    def test_is_at_notch_is_true(self, basic_rotor) -> None:  # noqa no-self-use
        basic_rotor.notch_position = 1
        assert basic_rotor.is_at_notch is True

    @staticmethod
    def test_rotor_turnover(basic_rotor) -> None:
        for _ in range(26 * 4):
            old_position = basic_rotor.rotor_position
            basic_rotor.turnover()
            new_position = basic_rotor.rotor_position
            if old_position != 25:
                assert new_position - old_position == 1
            assert new_position < 26

    @staticmethod
    @pytest.mark.parametrize(
        "value", [*list(range(26)), *list(map(lambda i: chr(i + 65), range(26)))]
    )
    def test_rotor_enciphering_is_reversible(basic_rotor, value) -> None:
        assert basic_rotor.backward(basic_rotor.forward(value)) == value

    @staticmethod
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            *zip(
                list(map(lambda i: chr(i + 65), range(26))),
                list("JPGVOUMFYQBENHZRDKASXLICTW"),
            )
        ],
    )
    def test_rotor_encrypts_correctly(value, expected):
        t_rotor = rotor.BasicRotor("test", "JPGVOUMFYQBENHZRDKASXLICTW", 0, 0, 0)
        assert t_rotor.forward(value) == expected


class TestTwoNotchRotor:
    def test_is_at_notch_true_for_two_positions(self) -> None:  # noqa no-self-use
        rotor_six = rotor.TwoNotchRotor(
            "VI",
            "JPGVOUMFYQBENHZRDKASXLICTW",
            rotor_position=12,
            notch_position=0,
            ring_setting=0,
        )
        assert rotor_six.is_at_notch
        rotor_six.rotor_position = 25
        assert rotor_six.is_at_notch
