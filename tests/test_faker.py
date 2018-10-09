import unittest
import warnings

from blahblah import fake, SubstitutionError
from district42 import json_schema as schema


class TestFaker(unittest.TestCase):

  primitive_types = [bool, int, float, str]

  def test_null_type_generator(self):
    # type
    data = fake(schema.null)
    self.assertIsNone(data)

    # overriding
    data = fake(schema.null, None)
    self.assertIsNone(data)

  def test_boolean_type_generator(self):
    # type
    data = fake(schema.boolean)
    self.assertIn(data, [True, False])

    # overriding
    data = fake(schema.boolean(False), True)
    self.assertTrue(data)

    with self.assertRaises(SubstitutionError):
      fake(schema.boolean(False), 0)

    # example
    data = fake(schema.boolean.example(True))
    self.assertTrue(data)

  def test_number_type_generator(self):
    with warnings.catch_warnings():
      warnings.simplefilter('ignore')
      # type
      data = fake(schema.number)
      self.assertIn(type(data), [int, float])
      # value
      data = fake(schema.number(42))
      self.assertEqual(data, 42)
      data = fake(schema.number(3.14))
      self.assertEqual(data, 3.14)

  def test_integer_type_generator(self):
    # type
    data = fake(schema.integer)
    self.assertIsInstance(data, int)

    # value
    data = fake(schema.integer(42))
    self.assertEqual(data, 42)

    # overriding
    data = fake(schema.integer(1), 42)
    self.assertEqual(data, 42)

    with self.assertRaises(SubstitutionError):
      fake(schema.integer(1), '42')

    # example
    data = fake(schema.integer.example(0))
    self.assertEqual(data, 0)

    # min
    data = fake(schema.integer.min(0))
    self.assertGreaterEqual(data, 0)

    # max
    data = fake(schema.integer.max(0))
    self.assertLessEqual(data, 0)

    # between
    data = fake(schema.integer.between(0, 1))
    self.assertTrue(0 <= data <= 1)

    # positive
    data = fake(schema.integer.positive)
    self.assertGreater(data, 0)

    data = fake(schema.integer.non_positive)
    self.assertLessEqual(data, 0)

    # negative
    data = fake(schema.integer.negative)
    self.assertLess(data, 0)

    data = fake(schema.integer.non_negative)
    self.assertGreaterEqual(data, 0)

    # unsigned
    data = fake(schema.integer.unsigned)
    self.assertGreaterEqual(data, 0)

    # zero
    data = fake(schema.integer.zero)
    self.assertEqual(data, 0)

    # multiple
    data = fake(schema.integer.multiple(3))
    self.assertEqual(data % 3, 0)

    data = fake(schema.integer.multiple(11))
    self.assertEqual(data % 11, 0)

  def test_float_type_generator(self):
    # type
    data = fake(schema.float)
    self.assertIsInstance(data, float)

    # value
    data = fake(schema.float(3.14))
    self.assertEqual(data, 3.14)

    # overriding
    data = fake(schema.float(1.0), 3.14)
    self.assertEqual(data, 3.14)

    with self.assertRaises(SubstitutionError):
      fake(schema.float(1.0), '3.14')

    # example
    data = fake(schema.float.example(3.14))
    self.assertEqual(data, 3.14)

    # min
    data = fake(schema.float.min(0.0))
    self.assertGreaterEqual(data, 0.0)

    # max
    data = fake(schema.float.max(0.0))
    self.assertLessEqual(data, 0.0)

    # between
    data = fake(schema.float.between(0.0, 1.0))
    self.assertTrue(0.0 <= data <= 1.0)

    # positive
    data = fake(schema.float.positive)
    self.assertGreater(data, 0.0)

    data = fake(schema.float.non_positive)
    self.assertLessEqual(data, 0.0)

    # negative
    data = fake(schema.float.negative)
    self.assertLess(data, 0.0)

    data = fake(schema.float.non_negative)
    self.assertGreaterEqual(data, 0.0)

    # zero
    data = fake(schema.float.zero)
    self.assertEqual(data, 0.0)

  def test_string_type_generator(self):
    import string

    # type
    data = fake(schema.string)
    self.assertIsInstance(data, str)
    self.assertGreaterEqual(len(data), 0)
    self.assertTrue(all(x in string.printable for x in data))

    # value
    data = fake(schema.string('banana'))
    self.assertEqual(data, 'banana')

    # overriding
    data = fake(schema.string('cucumber'), 'banana')
    self.assertEqual(data, 'banana')

    with self.assertRaises(SubstitutionError):
      fake(schema.string('cucumber'), [])

    # example
    data = fake(schema.string.example(''))
    self.assertEqual(data, '')

    # pattern
    regex = r'[abc]+'
    data = fake(schema.string.pattern(regex))
    self.assertRegex(data, regex)

    # contains
    data = fake(schema.string.contains('banana'))
    self.assertIn('banana', data)

    # numeric
    data = fake(schema.string.numeric)
    self.assertIsInstance(data, str)
    self.assertRegex(data, r'^\-?[0-9]+$')

    # numeric min
    data = fake(schema.string.numeric(2147483647 - 1))
    self.assertIsInstance(data, str)
    self.assertIn(data, ('2147483646', '2147483647'))

    # numeric min max
    data = fake(schema.string.numeric(0, 1))
    self.assertIsInstance(data, str)
    self.assertIn(data, ('0', '1'))

    # alphabetic
    data = fake(schema.string.alphabetic)
    self.assertRegex(data, r'^[a-zA-Z]*$')

    # alphabetic length
    data = fake(schema.string.alphabetic.length(10))
    self.assertEqual(len(data), 10)

    # alphabetic lowercase
    data = fake(schema.string.alphabetic.lowercase)
    self.assertRegex(data, r'^[a-z]*$')

    # alphabetic lowercase length
    data = fake(schema.string.alphabetic.lowercase.length(10))
    self.assertEqual(len(data), 10)

    # alphabetic uppercase
    data = fake(schema.string.alphabetic.uppercase)
    self.assertRegex(data, r'^[A-Z]*$')

    # alphabetic uppercase length
    data = fake(schema.string.alphabetic.uppercase.length(10))
    self.assertEqual(len(data), 10)

    # alpha_num
    data = fake(schema.string.alpha_num)
    self.assertRegex(data, r'^[a-zA-Z0-9]*$')

    # alpha_num length
    data = fake(schema.string.alpha_num.length(10))
    self.assertEqual(len(data), 10)

    # alpha_num lowercase
    data = fake(schema.string.alpha_num.lowercase)
    self.assertRegex(data, r'^[a-z0-9]*$')

    # alpha_num lowercase length
    data = fake(schema.string.alpha_num.lowercase.length(10))
    self.assertEqual(len(data), 10)

    # alpha_num uppercase
    data = fake(schema.string.alpha_num.uppercase)
    self.assertRegex(data, r'^[A-Z0-9]*$')

    # alpha_num uppercase length
    data = fake(schema.string.alpha_num.uppercase.length(10))
    self.assertEqual(len(data), 10)

    # length
    data = fake(schema.string.length(0))
    self.assertEqual(len(data), 0)

    data = fake(schema.string.length(1))
    self.assertEqual(len(data), 1)

    data = fake(schema.string.length(1, 2))
    self.assertTrue(1 <= len(data) <= 2)

    data = fake(schema.string.min_length(1))
    self.assertGreaterEqual(len(data), 1)

    data = fake(schema.string.max_length(1))
    self.assertLessEqual(len(data), 1)

    # empty
    data = fake(schema.string.empty)
    self.assertEqual(data, '')

    data = fake(schema.string.non_empty)
    self.assertGreaterEqual(len(data), 1)

  def test_timestamp_type_generator(self):
    # type
    data = fake(schema.timestamp)
    self.assertIsInstance(data, str)

    # overriding
    data = fake(schema.timestamp, '21-10-2015 04:29 pm')
    self.assertEqual(data, '2015-10-21 16:29:00')

    with self.assertRaises(SubstitutionError):
      fake(schema.timestamp, 1)

    # example
    data = fake(schema.timestamp.example('01/01/2015'))
    self.assertEqual(data, '01/01/2015')

    # value
    data = fake(schema.timestamp('21-10-2015 04:29 pm'))
    self.assertEqual(data, '2015-10-21 16:29:00')

  def test_array_type_generator(self):
    # type
    data = fake(schema.array)
    self.assertIsInstance(data, list)
    self.assertTrue(all(type(x) in self.primitive_types for x in data))

    # overriding
    array = [0, 1]
    data = fake(schema.array([schema.integer, schema.integer]), array)
    self.assertEqual(data, array)

    with self.assertRaises(SubstitutionError):
      fake(schema.array([schema.integer, schema.integer]), ['1', '2'])

    # example
    examples = (['true', 'false'], ['false', 'true'])
    data = fake(schema.array.examples(*examples))
    self.assertIn(data, examples)

    # items
    data = fake(schema.array([schema.integer(0), schema.integer(1)]))
    self.assertEqual(data, [0, 1])

    # contains
    data = fake(schema.array.contains(schema.integer(42)))
    self.assertGreaterEqual(data.count(42), 1)

    data = fake(schema.array.contains(schema.string('banana')).length(1))
    self.assertEqual(data, ['banana'])

    # contains_one
    data = fake(schema.array.contains_one(schema.integer(42)))
    self.assertIn(42, data)

    data = fake(schema.array.contains_one(schema.string('banana')).length(1))
    self.assertEqual(data, ['banana'])
    
    # contains_many
    data = fake(schema.array.contains_many(schema.integer(42)))
    self.assertGreaterEqual(data.count(42), 2)

    data = fake(schema.array.contains_many(schema.string('banana')).length(2))
    self.assertEqual(data, ['banana', 'banana'])

    # contains_all
    values = [True, False]
    data = fake(schema.array.contains_all(schema.from_native(value) for value in values).length(3))
    self.assertEqual(len(data), 3)
    self.assertIn(True, data)
    self.assertIn(False, data)

    # unique
    data = fake(schema.array([schema.boolean, schema.boolean]).unique)
    self.assertIn(True, data)
    self.assertIn(False, data)

    data = fake(schema.array.unique)
    self.assertEqual(len(set(data)), len(data))

    # length
    data = fake(schema.array.length(1))
    self.assertEqual(len(data), 1)

    data = fake(schema.array.length(1, 2))
    self.assertTrue(1 <= len(data) <= 2)

    data = fake(schema.array.min_length(1))
    self.assertGreaterEqual(len(data), 1)

    data = fake(schema.array.max_length(1))
    self.assertLessEqual(len(data), 1)

    # empty
    data = fake(schema.array.empty)
    self.assertEqual(data, [])

    data = fake(schema.array.non_empty)
    self.assertGreaterEqual(len(data), 1)

  def test_array_of_type_generator(self):
    # type
    data = fake(schema.array.of(schema.integer))
    self.assertIsInstance(data, list)
    self.assertTrue(all(isinstance(x, int) for x in data))

    # overriding
    data = fake(schema.array.of(schema.integer), [0])
    self.assertEqual(data, [0])

    with self.assertRaises(SubstitutionError):
      fake(schema.array.of(schema.integer), '[0]')

    # example
    example = ['banana', 'cucumber']
    data = fake(schema.array.of(schema.string).example(example))
    self.assertEqual(data, example)

    # items_schema
    data = fake(schema.array.of(schema.string('banana')))
    self.assertTrue(all(x == 'banana' for x in data))

    # unique
    data = fake(schema.array.of(schema.integer.between(0, 1)).length(2).unique)
    self.assertEqual([0, 1], sorted(data))
    
    # length
    data = fake(schema.array.of(schema.array).length(5))
    self.assertEqual(len(data), 5)

    data = fake(schema.array.of(schema.array).length(0, 2))
    self.assertTrue(0 <= len(data) <= 2)

    data = fake(schema.array.of(schema.string).min_length(1))
    self.assertGreaterEqual(len(data), 1)

    data = fake(schema.array.of(schema.string).max_length(1))
    self.assertLessEqual(len(data), 1)

  def test_object_type_generator(self):
    # type
    data = fake(schema.object)
    self.assertIsInstance(data, dict)
    self.assertTrue(all(type(data[key]) in self.primitive_types for key in data))

    # overriding
    dictionary = {'id': 1}
    data = fake(schema.object({'id': schema.integer}), dictionary)
    self.assertEqual(data, dictionary)

    data = fake(schema.object({'id?': schema.integer, 'name': schema.string}), {'id': 1})
    self.assertEqual(data['id'], 1)
    self.assertIn('name', data)
    self.assertIsInstance(data['name'], str)

    data = fake(schema.object({'id?': schema.integer, 'name': schema.string}), {'id'})
    self.assertIn('id', data)
    self.assertIsInstance(data['id'], int)
    self.assertIn('name', data)
    self.assertIsInstance(data['name'], str)

    data = fake(schema.object({'id?': schema.integer, 'name': schema.string}), {'id', 'name'})
    self.assertIn('id', data)
    self.assertIsInstance(data['id'], int)
    self.assertIn('name', data)
    self.assertIsInstance(data['name'], str)

    with self.assertRaises(NotImplementedError):
      fake(schema.object({'id?': schema.undefined, 'name': schema.string}), {'id'})

    with self.assertRaises(SubstitutionError):
      fake(schema.object({'id': schema.integer}), {'id': '1'})

    # example
    example = {'id': 1, 'title': 'Title', 'rating': 5.0}
    data = fake(schema.object.example(example))
    self.assertEqual(data, example)

    # keys
    data = fake(schema.object({
      'id':     schema.integer.positive,
      'title':  schema.string,
      'author': schema.object({
                  'id':   schema.integer.positive,
                  'name': schema.string
                })
    }))
    self.assertIsInstance(data, dict)
    self.assertIn('id', data)
    self.assertIsInstance(data['id'], int)
    self.assertIn('title', data)
    self.assertIsInstance(data['title'], str)
    self.assertIn('author', data)
    self.assertIsInstance(data['author'], dict)
    self.assertIn('id', data['author'])
    self.assertIsInstance(data['author']['id'], int)
    self.assertIn('name', data['author'])
    self.assertIsInstance(data['author']['name'], str)

    # length
    data = fake(schema.object({'id': schema.string.numeric}).length(5))
    self.assertEqual(len(data), 5)

    data = fake(schema.object.length(0))
    self.assertEqual(len(data), 0)

    data = fake(schema.object.length(0, 1))
    self.assertTrue(0 <= len(data) <= 1)

    # empty
    data = fake(schema.object.empty)
    self.assertEqual(data, {})

    data = fake(schema.object.non_empty)
    self.assertGreaterEqual(len(data), 1)

  def test_any_type_generator(self):
    # type
    data = fake(schema.any)
    self.assertIn(type(data), self.primitive_types)

    # overriding
    data = fake(schema.any, '42')
    self.assertEqual(data, '42')

    with self.assertRaises(SubstitutionError):
      fake(schema.any, unittest.TestCase)

  def test_any_of_type_generator(self):
    # options
    data = fake(schema.any_of(schema.integer(1), schema.integer(2)))
    self.assertIn(data, (1, 2))

    # overriding
    data = fake(schema.any_of(schema.integer, schema.string.numeric), '1')
    self.assertEqual(data, '1')

    with self.assertRaises(SubstitutionError):
      fake(schema.any_of(schema.integer, schema.string.numeric), True)

  def test_one_of_type_generator(self):
    # options
    data = fake(schema.one_of(schema.boolean, schema.integer(1), schema.integer(0)))
    self.assertIn(data, (True, False, 1, 0))

    # overriding
    data = fake(schema.one_of(schema.string('true'), schema.string('false')), 'true')
    self.assertEqual(data, 'true')

    with self.assertRaises(SubstitutionError):
      fake(schema.one_of(schema.string('true'), schema.string('false')), True)

  def test_enum_type_generator(self):
    # enumerators
    enumerators = (1, 2, 3)
    data = fake(schema.enum(*enumerators))
    self.assertIn(data, enumerators)

    enumerators = ('banana', 'cucumber')
    data = fake(schema.enum(*enumerators))
    self.assertIn(data, enumerators)

    # overriding
    data = fake(schema.enum('true', 'false', True, False), 'true')
    self.assertEqual(data, 'true')

    with self.assertRaises(SubstitutionError):
      fake(schema.enum('true', 'false', True, False), '1')

  def test_undefined_type_generator(self):
    with self.assertRaises(NotImplementedError):
      fake(schema.undefined)
