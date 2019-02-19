from copy import deepcopy

import delorean
import district42.json_schema
from district42.errors import DeclarationError
from district42.helpers import roll_out

from .errors import SubstitutionError


class Substitutor(district42.json_schema.AbstractVisitor):

  def __visit_nullable(self, schema):
    if 'nullable' in schema._params:
      return district42.json_schema.null
    raise SubstitutionError('{} is not nullable'.format(schema))

  def __visit_valuable(self, schema, value):
    try:
      return type(schema)().val(value)
    except DeclarationError as e:
      raise SubstitutionError(e) from e

  def __is_required(self, schema):
    return 'required' not in schema._params or schema._params['required']

  def visit_null(self, schema, value):
    if value is not None:
      raise SubstitutionError('"{}" is not null'.format(value))
    return deepcopy(schema)

  def visit_boolean(self, schema, value):
    if value is None:
      return self.__visit_nullable(schema)
    return self.__visit_valuable(schema, value)

  def visit_number(self, schema, value):
    if value is None:
      return self.__visit_nullable(schema)
    return self.__visit_valuable(schema, value)

  def visit_string(self, schema, value):
    if value is None:
      return self.__visit_nullable(schema)
    return self.__visit_valuable(schema, value)

  def visit_timestamp(self, schema, value):
    if value is None:
      return self.__visit_nullable(schema)
    return self.__visit_valuable(schema, value)

  def visit_array(self, schema, items):
    if items is None:
      return self.__visit_nullable(schema)

    error = district42.helpers.check_type(items, [list])
    if error:
      raise SubstitutionError(error)

    array_items = []
    if 'items' in schema._params:
      for idx, item in enumerate(schema._params['items']):
        array_items += [item % items[idx]]
    else:
      for item in items:
        array_items += [district42.json_schema.from_native(item)]

    return district42.json_schema.array(array_items)

  def visit_array_of(self, schema, items):
    if items is None:
      return self.__visit_nullable(schema)

    error = district42.helpers.check_type(items, [list])
    if error:
      raise SubstitutionError(error)

    array_items = []
    for item in items:
      array_items += [schema._params['items_schema'] % item]

    return district42.json_schema.array(array_items)

  def visit_object(self, schema, keys):
    if keys is None:
      return self.__visit_nullable(schema)

    error = district42.helpers.check_type(keys, [dict])
    if error:
      raise SubstitutionError(error)

    rolled_keys = roll_out(keys)
    if 'keys' in schema._params:
      clone = district42.json_schema.object(deepcopy(schema._params['keys']))
      for key in clone._params['keys']:
        if key not in rolled_keys: continue
        if not self.__is_required(clone._params['keys'][key]):
          clone._params['keys'][key]._params['required'] = True
        clone._params['keys'][key] %= rolled_keys[key]
      return clone.strict if 'strict' in schema._params else clone

    object_keys = {}
    for key, val in rolled_keys.items():
      object_keys[key] = district42.json_schema.from_native(val)
    substituted = district42.json_schema.object(object_keys)
    return substituted.strict if 'strict' in schema._params else substituted

  def visit_any(self, schema, value):
    if value is None:
      return self.__visit_nullable(schema)
    try:
      return district42.json_schema.from_native(value)
    except DeclarationError as e:
      raise SubstitutionError(e) from e

  def visit_any_of(self, schema, value):
    substituted = district42.json_schema.from_native(value)
    expected_types = self.__get_expected_types(schema._params['options'])

    error = district42.helpers.check_type(substituted, expected_types)
    if error:
      if value is None:
        return self.__visit_nullable(schema)
      raise SubstitutionError(error)

    return substituted

  def __get_expected_types(self, options):
    expected_types = []
    for option in options:
      expected_types += [type(option)]
      # schema.one_of(schema.array.of(schema.integer), schema.null) % [1]
      if isinstance(option, district42.json_schema.types.ArrayOf):
        expected_types += [district42.json_schema.types.Array]
    return expected_types

  def visit_one_of(self, schema, value):
    substituted = district42.json_schema.from_native(value)
    expected_types = self.__get_expected_types(schema._params['options'])

    error = district42.helpers.check_type(substituted, expected_types)
    if error:
      if value is None:
        return self.__visit_nullable(schema)
      raise SubstitutionError(error)

    return substituted

  def visit_enum(self, schema, value):
    for enumerator in schema._params['enumerators']:
      if type(enumerator) == type(value) and enumerator == value:
        return district42.json_schema.from_native(value)

    if value is None:
      return self.__visit_nullable(schema)

    raise SubstitutionError('"{}" is not present in the original enumeration'.format(value))

  def visit_undefined(self, schema, ignored_value):
    return deepcopy(schema)
