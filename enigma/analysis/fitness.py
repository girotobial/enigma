"""Implements fitness functions used in cryptoanalysis."""

import collections


def index_of_coincidence(
    text: str, normalizing_coeficient: int = 26, normalize: bool = True
) -> float:
    """The index of coincidence is the probability of two randomly selected letters being equal.

    Parameters
    ----------
    text : str
        The text to analyze
    normalizing_coeficient : int, optional
        The normalizing coefficient, usually the number of unique characters
        in the language's alphabet, by default 26. Ignored if normalize is false
    normalize : bool, optional
        Whether to normalize the output , by default True

    Returns
    -------
    float
    """
    if not normalize:
        normalizing_coeficient = 1

    text_length = len(text)
    denominator = text_length * (text_length - 1) / normalizing_coeficient

    character_counts = collections.Counter(text.upper())
    numerator = sum(count * (count - 1) for count in character_counts.values())

    return numerator / denominator if denominator != 0 else 0
