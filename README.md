# blahblah

Fake data generator for [district42](https://github.com/nikitanovosibirsk/district42) schema.

### Usage

```python
import district42.json_schema as schema
from blahblah import fake

fake(schema.string.numeric)
# '5694183762298043662'

fake(schema.array_of(schema.integer).length(1))
# [776641789]
```

### Installation

```sh
$ pip3 install blahblah
```

### Tests

```sh
$ python3 setup.py install
$ python3 -m unittest tests
```
