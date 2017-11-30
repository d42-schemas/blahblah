import unittest
import warnings

import blahblah
from district42 import json_schema as schema

from .substitution_testcase import SubstitutionTestCase


class TestSubstitution(SubstitutionTestCase):

  def test_null_type_substitution(self):
    self.assertSchemaCloned(schema.null, None)
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.null % 'banana'

  def test_boolean_type_substitution(self):
    self.assertSchemaCloned(schema.boolean, True)
    self.assertSchemaHasValue(schema.boolean % True, True)
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.boolean % 'banana'

  def test_number_type_substitution(self):
    with warnings.catch_warnings():
      warnings.simplefilter('ignore')
      self.assertSchemaCloned(schema.number, 42)
      self.assertSchemaHasValue(schema.number % 42, 42)
      self.assertSchemaCloned(schema.number, 3.14)
      self.assertSchemaHasValue(schema.number % 3.14, 3.14)
      with self.assertRaises(blahblah.errors.SubstitutionError):
        schema.number % 'banana'

  def test_integer_type_substitution(self):
    self.assertSchemaCloned(schema.integer, 42)
    self.assertSchemaHasValue(schema.integer % 42, 42)
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.integer % 'banana'

  def test_float_type_substitution(self):
    self.assertSchemaCloned(schema.float, 3.14)
    self.assertSchemaHasValue(schema.float % 3.14, 3.14)
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.float % 'banana'

  def test_string_type_substitution(self):
    self.assertSchemaCloned(schema.string, 'banana')
    self.assertSchemaHasValue(schema.string % 'banana', 'banana')
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.string.numeric % 1

  def test_timestamp_type_substitution(self):
    self.assertSchemaCloned(schema.timestamp, '21-10-2015 04:29 pm')
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.timestamp % True

  def test_array_type_substitution(self):
    self.assertSchemaCloned(schema.array, [1, 2, 3])
    self.assertIsInstance(schema.array % [1, 2, 3], schema.types.Array)

    array_value = [None, 0, 3.14, 'banana', [], {}]
    self.assertSchemaHasValue(schema.array % array_value, array_value)

  def test_array_type_object_substitution(self):
    object_schema = schema.object({'id': schema.integer})

    array1_schema = schema.array([object_schema])
    array1_value = [{'id': 1}]
    self.assertSchemaHasValue(array1_schema % array1_value, array1_value)

    array2_schema = schema.array([object_schema, object_schema])
    array2_value = [{'id': 1}, {'id': 2}]
    self.assertSchemaHasValue(array2_schema % array2_value, array2_value)

    with self.assertRaises(IndexError):
      array2_schema % array1_value

    array2_value_extra = [{'id': 1}, {'id': 2}, {'id': 3}]
    self.assertSchemaHasValue(array2_schema % array2_value_extra, array2_value_extra[:2])

  def test_array_of_type_substitution(self):
    self.assertSchemaCloned(schema.array.of(schema.integer), [1, 2, 3])
    self.assertIsInstance(schema.array.of(schema.integer) % [1, 2, 3], schema.types.Array)
    self.assertSchemaHasValue(schema.array.of(schema.integer) % [1, 2, 3], [1, 2, 3])

    with warnings.catch_warnings():
      warnings.simplefilter('ignore')
      self.assertSchemaCloned(schema.array_of(schema.integer), [1, 2, 3])
      self.assertIsInstance(schema.array_of(schema.integer) % [1, 2, 3], schema.types.Array)
      self.assertSchemaHasValue(schema.array_of(schema.integer) % [1, 2, 3], [1, 2, 3])

  def test_array_of_object_type_substitution(self):
    object_schema = schema.object({
      'id': schema.integer,
      'is_deleted': schema.boolean,
    })
    array_value = [{'id': 1}, {'id': 2, 'is_deleted': False}]
    self.assertSchemaHasValue(schema.array.of(object_schema) % array_value, array_value)

  def test_object_type_substitution(self):
    self.assertSchemaCloned(schema.object({'id': schema.integer}), {'id': 42})

    object_schema = schema.object({
      'id':         schema.integer,
      'title?':     schema.string,
      'is_deleted': schema.boolean,
      'created_at': schema.undefined
    })
    keys = {
      'id': 42,
      'title': 'Banana Title'
    }
    self.assertSchemaCloned(object_schema, keys)
    substituted = object_schema % keys
    self.assertSchemaHasValue(substituted, keys)
    self.assertIn('title', substituted)
    self.assertIn('is_deleted', substituted)
    self.assertIsInstance(substituted['created_at'], schema.types.Undefined)

    object_value = {'id': 1, 'is_deleted': False}
    self.assertSchemaHasValue(schema.object % object_value, object_value)

    self.assertNotIn('new_key', object_schema % {'new_key': 'banana'})

    self.assertEqual(
      len((schema.object % object_value)._params),
      len((schema.object.empty % object_value)._params)
    )

  def test_any_type_substitution(self):
    self.assertSchemaCloned(schema.any, 'banana')
    self.assertIsInstance(schema.any % True, schema.types.Boolean)
    self.assertIsInstance(schema.any % 42, schema.types.Number)
    self.assertIsInstance(schema.any % 3.14, schema.types.Number)
    self.assertIsInstance(schema.any % '', schema.types.String)

  def test_any_of_type_substitution(self):
    self.assertSchemaCloned(schema.any_of(schema.boolean, schema.array), False)

    integer_or_numeric = schema.any_of(schema.integer, schema.string.numeric)
    value = '1234'
    self.assertSchemaHasValue(integer_or_numeric % value, value)

    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.one_of(schema.boolean, schema.integer) % 'banana'

  def test_one_of_type_substitution(self):
    self.assertSchemaCloned(schema.one_of(schema.boolean, schema.array), False)

    integer_or_numeric = schema.one_of(schema.integer, schema.string.numeric)
    value = '1234'
    self.assertSchemaHasValue(integer_or_numeric % value, value)

    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.one_of(schema.boolean, schema.integer) % 'banana'

  def test_enum_type_substitution(self):
    self.assertSchemaCloned(schema.enum(1, 2, 3), 1)

    true_or_false = schema.enum('true', 'false')
    value = 'true'
    self.assertSchemaHasValue(true_or_false % value, value)

    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.enum(1, 2) % 3

  def test_undefined_type_substitution(self):
    self.assertSchemaCloned(schema.undefined, None)
