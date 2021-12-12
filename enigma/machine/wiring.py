"""Wiring helper class"""

from __future__ import annotations

from collections.abc import MutableSequence

from ..core import character_to_int, int_to_char


class Wiring(MutableSequence):
    def __init__(self, encoding: str):
        self.__coding = self._decode(encoding.upper())

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Wiring):
            return self.__coding == __o.__coding  # noqa protected-access
        if isinstance(__o, list):
            return self.__coding == __o
        raise NotImplementedError

    def __getitem__(self, idx) -> int:  # type: ignore
        return self.__coding[idx]  # type:ignore

    def __setitem__(self, idx: int, val: object) -> None:  # type:ignore
        if not isinstance(val, int):
            raise NotImplementedError
        self.__coding[idx] = val

    def __delitem__(self, idx: int) -> None:  # type:ignore
        del self.__coding[idx]

    def insert(self, index: int, value: object) -> None:  # type:ignore
        if not isinstance(value, int):
            raise NotImplementedError
        self.__coding.insert(index, value)

    def __len__(self) -> int:
        return len(self.__coding)

    def __repr__(self) -> str:
        return f"Wiring('{self.encoding}')"

    def __str__(self) -> str:
        return str(self.__coding)

    @classmethod
    def _from_decoded(cls, decoded: list[int]) -> Wiring:
        instance = cls("A")
        instance.__coding = decoded  # noqa unused-private-member
        return instance

    @staticmethod
    def _decode(encoding: str) -> list[int]:
        return list(map(character_to_int, encoding))

    @property
    def encoding(self) -> str:
        return "".join(list(map(int_to_char, self.__coding)))

    def inverse(self) -> Wiring:
        inverse = [0] * len(self)
        for i, val in enumerate(self):
            inverse[val] = i
        return Wiring._from_decoded(inverse)
