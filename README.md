# Typext
New methods for some builtin types like int, str, dict, list, ...

# Description
This module adds some useful methods to builtin types. 

Thanks to https://github.com/clarete/forbiddenfruit for make this possible.

## Reqirements
* **frobiddenfruit**

## Usage
```python
from typext import install

install()

# conversion
a = 100
a.cstr()

>>> "100"

# iterables
l = [1, 2, 3]
l.empty()

>>> False
```
