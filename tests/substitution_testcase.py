import unittest


class SubstitutionTestCase(unittest.TestCase):

  def assertSchemaCloned(self, schema, value):
    self.assertNotEqual(schema, schema % value)

  def assertValuableHasValue(self, valuable, value):
    self.assertIsInstance(valuable._params['value'], type(value))
    self.assertEqual(valuable._params['value'], value)

  def assertArrayHasItems(self, array, items):
    self.assertGreaterEqual(len(array._params['items']), len(items))
    for idx, item in enumerate(array._params['items']):
      self.assertSchemaHasValue(item, items[idx])

  def assertObjectHasKeys(self, object, keys):
    self.assertGreaterEqual(len(object._params['keys']), len(keys))
    for key, val in object._params['keys'].items():
      if key in keys:
        self.assertSchemaHasValue(val, keys[key])

  def assertSchemaHasValue(self, substituted, value):
    if 'value' in substituted._params:
      return self.assertValuableHasValue(substituted, value)
    elif 'items' in substituted._params:
      return self.assertArrayHasItems(substituted, value)
    elif 'keys' in substituted._params:
      return self.assertObjectHasKeys(substituted, value)
