import collections


def index_of_coincidence(text: str, normalizing_coeficient: int = 26) -> float:

    text_length = len(text)
    denominator = text_length * (text_length - 1) / normalizing_coeficient

    character_counts = collections.Counter(text.upper())
    numerator = sum(count * (count - 1) for count in character_counts.values())

    return numerator / denominator if denominator != 0 else 0
