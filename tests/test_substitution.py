import unittest
import blahblah
import district42.json_schema as schema
from substitution_testcase import SubstitutionTestCase


class TestSubstitution(SubstitutionTestCase):
  
  def test_null_type_substitution(self):
    self.assertSchemaCloned(schema.null, None)

  def test_boolean_type_substitution(self):
    self.assertSchemaCloned(schema.boolean, True)
    self.assertSchemaHasValue(schema.boolean, True)

  def test_number_type_substitution(self):
    self.assertSchemaCloned(schema.number, 42)
    self.assertSchemaHasValue(schema.number, 42)

    self.assertSchemaCloned(schema.number, 3.14)
    self.assertSchemaHasValue(schema.number, 3.14)

  def test_string_type_substitution(self):
    self.assertSchemaCloned(schema.string, 'banana')
    self.assertSchemaHasValue(schema.string, 'banana')

  def test_timestamp_type_substitution(self):
    self.assertSchemaCloned(schema.timestamp, '21-10-2015 04:29 pm')

  def test_array_type_substitution(self):
    self.assertSchemaCloned(schema.array, [1, 2, 3])
    self.assertIsInstance(schema.array % [1, 2, 3], schema.types.Array)

  def test_array_of_type_substitution(self):
    self.assertSchemaCloned(schema.array_of(schema.integer), [1, 2, 3])
    self.assertIsInstance(schema.array_of(schema.integer) % [1, 2, 3], schema.types.Array)

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
    self.assertSchemaHasValue(substituted['id'], keys['id'])
    self.assertIn('title', substituted)
    self.assertSchemaHasValue(substituted['title'], keys['title'])
    self.assertIn('is_deleted', substituted)
    self.assertIsInstance(substituted['created_at'], schema.types.Undefined)

  def test_any_type_substitution(self):
    self.assertSchemaCloned(schema.any, 'banana')
    self.assertIsInstance(schema.any.nullable % None, schema.types.Null)
    self.assertIsInstance(schema.any % True, schema.types.Boolean)
    self.assertIsInstance(schema.any % 42, schema.types.Number)
    self.assertIsInstance(schema.any % 3.14, schema.types.Number)
    self.assertIsInstance(schema.any % '', schema.types.String)

  def test_any_of_type_substitution(self):
    self.assertSchemaCloned(schema.any_of(schema.boolean(False), schema.array), False)

    integer_or_numeric = schema.any_of(schema.integer, schema.string.numeric)
    value = '1234'
    self.assertIsInstance(integer_or_numeric % value, schema.types.String)
    self.assertSchemaHasValue(integer_or_numeric % value, value)

  def test_one_of_type_substitution(self):
    self.assertSchemaCloned(schema.one_of(schema.boolean(False), schema.array), False)

    integer_or_numeric = schema.one_of(schema.integer, schema.string.numeric)
    value = '1234'
    self.assertIsInstance(integer_or_numeric % value, schema.types.String)
    self.assertSchemaHasValue(integer_or_numeric % value, value)

  def test_enum_type_substitution(self):
    self.assertSchemaCloned(schema.enum(1, 2, 3), 1)

    true_of_false = schema.enum('true', 'false')
    value = 'true'
    self.assertIsInstance(true_of_false % value, schema.types.String)
    self.assertSchemaHasValue(true_of_false % value, value)


if __name__ == '__main__':
  unittest.main()
