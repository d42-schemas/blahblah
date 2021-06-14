from typing import Any, Callable
from unittest.mock import Mock

import pytest
from district42 import Schema

from blahblah import Generator, Random

__all__ = ("generate", "generator", "random_",)


@pytest.fixture()
def random_() -> Mock:
    return Mock(Random, wraps=Random())


@pytest.fixture()
def generator(random_: Mock) -> Generator:
    return Generator(random_)


@pytest.fixture()
def generate(generator: Generator) -> Callable[[Schema], Any]:
    def _generate(sch: Schema) -> Any:
        return sch.__accept__(generator)
    return _generate
