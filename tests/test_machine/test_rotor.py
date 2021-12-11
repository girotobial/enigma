"""Tests for the rotor of the enigma machine"""

from enigma.machine import rotor


def test_rotor_intializes() -> None:
    """GIVEN a set of inputs

    THEN the rotor intializes
    AND stores that data
    """
    test_rotor = rotor.Rotor(
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
