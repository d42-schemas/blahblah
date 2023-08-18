import random
import sys
from typing import Any, List, Sequence, TypeVar

__all__ = ("Random",)

from blahblah._consts import FLOAT_MIN, FLOAT_MAX

_T = TypeVar("_T")
SeedType = TypeVar("SeedType", int, float, str, bytes, bytearray)


class Random:
    def set_seed(self, seed: SeedType) -> None:
        random.seed(seed)

    def random_int(self, start: int, end: int) -> int:
        return random.randint(start, end)

    def random_float(self, start: float, end: float) -> float:
        return random.uniform(start, end)

    def random_float_with_precision(
        self, start: float, end: float, precision: int
    ) -> float:
        right_digits = random.randint(precision, sys.float_info.dig - 1)
        left_digits = max(1, sys.float_info.dig - right_digits)

        sign = random.choice(("+", "-"))
        left_number = random.randint(0, pow(10, left_digits) - 1)
        right_number = random.randint(0, pow(10, right_digits) - 1)

        result = round(float(f"{sign}{left_number}.{right_number}"), precision)

        # It is possible that result is higher or lower than max and min values, ensure that values
        # belong to specified numbers
        if result > end:
            result = result - (result - end + random.uniform(0, end))
        if result < start:
            result = result + (start - result + random.uniform(0, start))

        return round(result, precision)

    def random_str(self, length: int, alphabet: str) -> str:
        return "".join(random.choice(alphabet) for _ in range(length))

    def random_choice(self, sequence: Sequence[_T]) -> _T:
        return random.choice(sequence)

    def shuffle_list(self, elements: List[Any]) -> None:
        random.shuffle(elements)
