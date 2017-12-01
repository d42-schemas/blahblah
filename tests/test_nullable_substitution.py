import unittest
import warnings

import blahblah
from district42 import json_schema as schema

from .substitution_testcase import SubstitutionTestCase


class TestNullableSubstitution(SubstitutionTestCase):

  def setUp(self):
    warnings.simplefilter('ignore')

  def test_null_type_substitution(self):
    self.assertIsInstance(schema.null % None, schema.types.Null)
    self.assertIsInstance(schema.null % None % None, schema.types.Null)

  def test_nullable_valuable_type_substitution(self):
    self.assertSchemaCloned(schema.string.nullable, None)
    self.assertSchemaHasValue(schema.string.nullable % 'banana', 'banana')
    self.assertIsInstance(schema.string.nullable % None, schema.types.Null)
    self.assertIsInstance(schema.string('banana').nullable % None, schema.types.Null)
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.string % None
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.string.nullable % 'banana' % None

  def test_nullable_array_type_substitution(self):
    self.assertSchemaCloned(schema.array.nullable, None)
    self.assertSchemaHasValue(schema.array.nullable % [], [])
    self.assertIsInstance(schema.array.nullable % None, schema.types.Null)
    self.assertIsInstance(schema.array([]).nullable % None, schema.types.Null)
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.array % None
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.array([schema.integer]).nullable % [1] % None

  def test_nullable_array_of_type_substitution(self):
    self.assertSchemaCloned(schema.array_of(schema.integer).nullable, None)
    self.assertSchemaHasValue(schema.array_of(schema.integer).nullable % [1], [1])
    self.assertIsInstance(schema.array_of(schema.integer).nullable % None, schema.types.Null)
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.array_of(schema.integer) % None
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.array_of(schema.integer).nullable % [1] % None

  def test_nullable_object_type_substitution(self):
    self.assertSchemaCloned(schema.object.nullable, None)
    self.assertSchemaHasValue(schema.object.nullable % {}, {})
    self.assertIsInstance(schema.object.nullable % None, schema.types.Null)
    self.assertIsInstance(schema.object({}).nullable % None, schema.types.Null)
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.object % None
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.object.nullable % {} % None

  def test_nullable_any_type_substitution(self):
    self.assertIsInstance(schema.any.nullable % None, schema.types.Null)
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.any % None
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.any.nullable % 1 % None

  def test_nullable_any_of_type_substitution(self):
    self.assertIsInstance(
      schema.any_of(schema.string.numeric, schema.integer, schema.null) % None,
      schema.types.Null
    )
    self.assertIsInstance(
      schema.any_of(schema.string.numeric, schema.integer).nullable % None,
      schema.types.Null
    )
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.any_of(schema.string.numeric, schema.integer) % None
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.any_of(schema.string.numeric, schema.integer).nullable % '1' % None

  def test_nullable_one_of_type_substitution(self):
    self.assertIsInstance(
      schema.one_of(schema.string.numeric, schema.integer, schema.null) % None,
      schema.types.Null
    )
    self.assertIsInstance(
      schema.one_of(schema.string.numeric, schema.integer).nullable % None,
      schema.types.Null
    )
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.one_of(schema.string.numeric, schema.integer) % None
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.one_of(schema.string.numeric, schema.integer, schema.null) % 1 % None

  def test_nullable_enum_type_substitution(self):
    self.assertIsInstance(
      schema.enum(0, 1, None) % None,
      schema.types.Null
    )
    self.assertIsInstance(
      schema.enum(0, 1).nullable % None,
      schema.types.Null
    )
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.enum(0, 1) % None
    with self.assertRaises(blahblah.errors.SubstitutionError):
      schema.enum(False, True).nullable % True % None

  def test_undefined_type_substitution(self):
    self.assertIsInstance(schema.undefined % None, schema.types.Undefined)
