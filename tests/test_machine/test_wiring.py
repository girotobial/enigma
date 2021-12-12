"""Tests for the wiring_obj class of the enigma machine"""


import pytest

from enigma.machine import wiring


def test_wiring_obj_encodes() -> None:
    encoding = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    wiring_ = wiring.Wiring(encoding)
    assert wiring_.encoding == encoding
    assert wiring_ == list(range(26))


def test_wiring_obj_encodes_null_string() -> None:
    encoding = ""
    wiring_ = wiring.Wiring(encoding)
    assert wiring_.encoding == encoding


@pytest.mark.parametrize(
    ("encoding", "inverse"),
    [
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "UWYGADFPVZBECKMTHXSLRINQOJ"),
    ],
)
def test_wiring_obj_inverse(encoding, inverse) -> None:
    wiring_ = wiring.Wiring(encoding)
    assert wiring_.inverse().encoding == inverse


@pytest.fixture
def wiring_obj() -> wiring.Wiring:
    return wiring.Wiring("EKMFLGDQVZNTOWYHXUSPAIBRCJ")


def test_wiring_obj_can_be_cast_to_list(
    wiring_obj,  # noqa redefined-outer-name
) -> None:
    wiring_list = list(wiring_obj)
    assert isinstance(wiring_list, list)


def test_wiring_obj_can_be_sliced(wiring_obj) -> None:  # noqa redefined-outer-name
    value = wiring_obj[0]
    assert value == 4
