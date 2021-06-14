import string
from typing import Any, Dict, List

from district42 import SchemaVisitor
from district42.types import (
    AnySchema,
    BoolSchema,
    ConstSchema,
    DictSchema,
    FloatSchema,
    IntSchema,
    ListSchema,
    NoneSchema,
    StrSchema,
)
from district42.utils import is_ellipsis
from niltype import Nil

from ._consts import (
    FLOAT_MAX,
    FLOAT_MIN,
    INT_MAX,
    INT_MIN,
    LIST_LEN_MAX,
    LIST_LEN_MIN,
    STR_LEN_MAX,
    STR_LEN_MIN,
)
from ._random import Random

__all__ = ("Generator",)


class Generator(SchemaVisitor[Any]):
    def __init__(self, random: Random) -> None:
        self._random = random

    def visit_none(self, schema: NoneSchema, **kwargs: Any) -> None:
        return None

    def visit_bool(self, schema: BoolSchema, **kwargs: Any) -> bool:
        if schema.props.value is not Nil:
            return schema.props.value
        return self._random.random_choice((True, False))

    def visit_int(self, schema: IntSchema, **kwargs: Any) -> int:
        if schema.props.value is not Nil:
            return schema.props.value

        min_value = schema.props.min if (schema.props.min is not Nil) else INT_MIN
        max_value = schema.props.max if (schema.props.max is not Nil) else INT_MAX
        return self._random.random_int(min_value, max_value)

    def visit_float(self, schema: FloatSchema, **kwargs: Any) -> float:
        if schema.props.value is not Nil:
            return schema.props.value

        min_value = schema.props.min if (schema.props.min is not Nil) else FLOAT_MIN
        max_value = schema.props.max if (schema.props.max is not Nil) else FLOAT_MAX
        return self._random.random_float(min_value, max_value)

    def visit_str(self, schema: StrSchema, **kwargs: Any) -> str:
        if schema.props.value is not Nil:
            return schema.props.value

        if schema.props.len is not Nil:
            length = schema.props.len
        else:
            min_length = schema.props.min_len if (schema.props.min_len is not Nil) else STR_LEN_MIN
            max_length = schema.props.max_len if (schema.props.max_len is not Nil) else STR_LEN_MAX
            length = self._random.random_int(min_length, max_length)

        if schema.props.alphabet is not Nil:
            alphabet = schema.props.alphabet
        else:
            alphabet = string.printable

        return self._random.random_str(length, alphabet)

    def visit_list(self, schema: ListSchema, **kwargs: Any) -> List[Any]:
        if schema.props.elements is not Nil:
            elements = []
            for elem in schema.props.elements:
                if is_ellipsis(elem):
                    continue
                elements.append(elem.__accept__(self, **kwargs))
            return elements

        is_length_specified = False
        if schema.props.len is not Nil:
            length = schema.props.len
            is_length_specified = True
        else:
            min_length = LIST_LEN_MIN
            if schema.props.min_len is not Nil:
                min_length = schema.props.min_len
                is_length_specified = True
            max_length = LIST_LEN_MAX
            if schema.props.max_len is not Nil:
                max_length = schema.props.max_len
                is_length_specified = True
            length = self._random.random_int(min_length, max_length)

        if schema.props.type is not Nil:
            return [schema.props.type.__accept__(self, **kwargs) for _ in range(length)]

        if is_length_specified:
            return [[] for _ in range(length)]
        return []

    def visit_dict(self, schema: DictSchema, **kwargs: Any) -> Dict[Any, Any]:
        generated: Dict[Any, Any] = {}
        if schema.props.keys is Nil:
            return generated

        for key, val in schema.props.keys.items():
            if key is ...:
                continue
            generated[key] = val.__accept__(self, **kwargs)

        return generated

    def visit_any(self, schema: AnySchema, **kwargs: Any) -> Any:
        if schema.props.types is Nil:
            return None
        chosen = self._random.random_choice(schema.props.types)
        return chosen.__accept__(self, **kwargs)

    def visit_const(self, schema: ConstSchema, **kwargs: Any) -> Any:
        if schema.props.value is Nil:
            return None
        return schema.props.value