from typing import Any, Callable
from unittest.mock import Mock

import pytest
from district42.types import Schema

from blahblah import Generator, Random, RegexGenerator

__all__ = ("generate", "generator", "random_", "regex_generator",)


@pytest.fixture()
def random_() -> Random:
    return Mock(Random, wraps=Random())


@pytest.fixture()
def regex_generator(random_: Random) -> RegexGenerator:
    return RegexGenerator(random_)


@pytest.fixture()
def generator(random_: Random, regex_generator: RegexGenerator) -> Generator:
    return Generator(random_, regex_generator)


@pytest.fixture()
def generate(generator: Generator) -> Callable[[Schema], Any]:
    def _generate(sch: Schema) -> Any:
        return sch.__accept__(generator)
    return _generate
