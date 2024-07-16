from datetime import date

from baby_steps import given, then, when
from district42 import schema

from ..._fixtures import *  # noqa: F401, F403


def test_date_generation(*, generate, random_):
    with given:
        sch = schema.date_type

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, date)
        assert random_.mock_calls == []


def test_date_value_generation(*, generate, random_):
    with given:
        dt = date.today()
        sch = schema.date_type(dt)

    with when:
        res = generate(sch)

    with then:
        assert res == dt
        assert random_.mock_calls == []
