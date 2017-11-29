from copy import deepcopy

import delorean
import district42.json_schema

from .errors import SubstitutionError


class Substitutor(district42.json_schema.AbstractVisitor):

  def __visit_nullable(self, schema):
    if 'nullable' in schema._params:
      return district42.json_schema.null
    raise SubstitutionError('{} is not nullable'.format(schema))

  def __visit_valuable(self, schema, value):
    if value is None:
      return self.__visit_nullable(schema)
    clone = deepcopy(schema)
    clone._params['value'] = value
    return clone

  def __is_required(self, schema):
    return 'required' not in schema._params or schema._params['required']

  def visit_null(self, schema, *args):
    return deepcopy(schema)

  def visit_boolean(self, schema, value):
    return self.__visit_valuable(schema, value)

  def visit_number(self, schema, value):
    return self.__visit_valuable(schema, value)

  def visit_string(self, schema, value):
    return self.__visit_valuable(schema, value)

  def visit_timestamp(self, schema, value):
    return self.__visit_valuable(schema, delorean.parse(value))

  def visit_array(self, schema, items):
    if items is None:
      return self.__visit_nullable(schema)

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

    array_items = []

    for item in items:
      array_items += [schema._params['items_schema'] % item]

    return district42.json_schema.array(array_items)

  def visit_object(self, schema, keys):
    if keys is None:
      return self.__visit_nullable(schema)

    if 'keys' in schema._params:
      clone = district42.json_schema.object(deepcopy(schema._params['keys']))
      for key in clone._params['keys']:
        if key not in keys: continue
        if not self.__is_required(clone._params['keys'][key]):
          clone._params['keys'][key]._params['required'] = True
        clone._params['keys'][key] %= keys[key]
      return clone

    object_keys = {}
    for key, val in keys.items():
      object_keys[key] = district42.json_schema.from_native(val)
    return district42.json_schema.object(object_keys)

  def visit_any(self, schema, value):
    if value is None:
      return self.__visit_nullable(schema)
    return district42.json_schema.from_native(value)

  def visit_any_of(self, schema, value):
    substituted = district42.json_schema.from_native(value)
    error = district42.helpers.check_type(substituted, [type(x) for x in schema._params['options']])
    if error:
      raise SubstitutionError(error)
    return substituted

  def visit_one_of(self, schema, value):
    substituted = district42.json_schema.from_native(value)
    error = district42.helpers.check_type(substituted, [type(x) for x in schema._params['options']])
    if error:
      raise SubstitutionError(error)
    return substituted

  def visit_enum(self, schema, value):
    if value not in schema._params['enumerators']:
      raise SubstitutionError('"{}" is not present in the original enumeration'.format(value))
    return district42.json_schema.from_native(value)

  def visit_undefined(self, schema, ignored_value):
    return deepcopy(schema)
