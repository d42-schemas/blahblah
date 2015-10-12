import unittest


class SubstitutionTestCase(unittest.TestCase):

  def assertSchemaCloned(self, schema, value):
    self.assertNotEqual(schema, schema % value)

  def assertSchemaHasValue(self, schema, value):
    type_schema = schema % value
    self.assertEqual(type_schema._params['value'], value)
