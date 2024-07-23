from datetime import date

from baby_steps import given, then, when
from district42 import schema

from ..._fixtures import *  # noqa: F401, F403


def test_date_generation(*, generate, random_):
    with given:
        sch = schema.date

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, date)
        assert random_.mock_calls == []


def test_date_value_generation(*, generate, random_):
    with given:
        d = date.today()
        sch = schema.date(d)

    with when:
        res = generate(sch)

    with then:
        assert res == d
        assert random_.mock_calls == []
