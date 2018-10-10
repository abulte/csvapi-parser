# csvapi parser

CSV parser, intended for use with [csvapi](https://github.com/opendatateam/csvapi).

This is based on, and depends on, the [Agate library](https://agate.readthedocs.io).

Provided a path to a CSV, it will:
- try to guess the encoding with [cchardet](https://github.com/PyYoshi/cChardet) — encoding can be forced if needed;
- try to guess the CSV _dialect_ (delimiter and such) by using a custom sniffing method;
- return an `agate.Table` object or raise an `Exception`.

## Usage

```python
from csv_parser import parse

table = parse('/path/to/csv')

# force the encoding
table = parse('/path/to/csv', encoding='utf-8')
```
