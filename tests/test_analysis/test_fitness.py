"""Tests for the fitness functions in the analysis module"""

import pytest

from enigma.analysis import fitness


def test_index_of_coincidence_correct_output() -> None:
    """
    GIVEN a string

    THEN the correct ioc is returned
    """
    test_string = (
        "QPWKA LVRXC QZIKG RBPFA EOMFL JMSDZ VDHXC XJYEB IMTRQ WNMEA"
        "IZRVK CVKVL XNEIC FZPZC ZZHKM LVZVZ IZRRQ WDKEC HOSNY XXLSP"
        "MYKVQ XJTDC IOMEE XDQVS RXLRL KZHOV"
    ).replace(" ", "")

    result = fitness.index_of_coincidence(test_string)
    assert result == pytest.approx(1.11618, rel=1e-3)


def test_index_of_coincidence_no_input() -> None:
    """
    GIVEN index_of_coincidence

    WHEN an empty string is inputted
    THEN 0 is returned
    """
    assert fitness.index_of_coincidence("") == 0
