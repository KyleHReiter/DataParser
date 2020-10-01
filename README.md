# Data Parser

### Overview:

This module was developed to facilitate parsing of large data sets in the following string format.

`<seg>|<field>|<field>...||<seg>|<field>...||<seg>...`

String format rule(s):
- A final segment seperator (||) is optional.
- Segment names can repeat.
- Segment field names can repeat.

### Requirements:

[Python 3.7.x](https://www.python.org/downloads/)

After installation of Python install the following modules by running the command below:
`python -m pip install -r requirements.txt`

### Installation:
If a local pip server has loaded this module:

`python -m pip install data_parser`

If a local pip server is unavailable copy `data_parser.py` into `site-packages` under your python instance or a location on your `PYTHON_PATH`.

### Usage:
Import data parser module and create an instance of `DataParser`. 
```python
# Import data parser module.
from data_parser import DataParser

# Create instance of data parser.
DATA_PARSER = DataParser()

# Iterate segments.
for segment in DATA_PARSER.digest(raw_text).segments_iter():
    print_segment(segment.compose())
```

### Command Line Interface (CLI):

Parse data CLI exists use help switch to see options.

`python parse_data.py -h`

### Developer Notes:
### Check:

`python -m pylint src/data_parser.py`

`python -m flake8 src/data_parser.py`

### Test:

`python -m unittest test/data_parser_test.py`
