import random
import sys
from typing import Any, List, Sequence, TypeVar

from niltype import Nil, Nilable

__all__ = ("Random",)

_T = TypeVar("_T")
SeedType = TypeVar("SeedType", int, float, str, bytes, bytearray)


class Random:
    def set_seed(self, seed: SeedType) -> None:
        random.seed(seed)

    def random_int(self, start: int, end: int) -> int:
        return random.randint(start, end)

    def random_float(self, start: float, end: float, precision: Nilable[int] = Nil) -> float:
        if precision is Nil:
            return random.uniform(start, end)

        if start >= 0:
            sign = 1
        elif end <= 0:
            sign = -1
        else:
            sign = random.choice((1, -1))

        # Generate a random number of right digits within the precision limit
        right_digits = random.randint(0, precision)

        # Calculate the potential maximum left digits based on the range
        left_digits = max(1, sys.float_info.dig - right_digits)

        # Generate random left and right parts
        left_number = sign * random.randint(0, pow(10, left_digits) - 1)
        right_number = random.randint(0, pow(10, right_digits) - 1)

        result = float(f"{left_number}.{right_number}")

        # Adjust the result if it's out of the [start, end] range
        if result > end:
            result -= result - end + self.random_float(0, end)
        if result < start:
            result += start - result + self.random_float(0, start)

        return round(result, precision)

    def random_str(self, length: int, alphabet: str) -> str:
        return "".join(random.choice(alphabet) for _ in range(length))

    def random_choice(self, sequence: Sequence[_T]) -> _T:
        return random.choice(sequence)

    def shuffle_list(self, elements: List[Any]) -> None:
        random.shuffle(elements)
