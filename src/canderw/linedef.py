import re
import string
from typing import NamedTuple, Any, Optional, Union, Tuple, Iterable


class FormatString(NamedTuple):
    """Represents a string that conforms to the [Format String Syntax][1] in the string module.

    [1]: https://docs.python.org/3/library/string.html#format-string-syntax
    """
    literal_text: Optional[str]
    field_name: Optional[str]
    format_spec: Optional[str]
    conversion: Optional[str]


def parse_format_str(formatter: string.Formatter = string.Formatter(), format_str: str = '') -> Iterable[FormatString]:
    """Generates FormatString named tuples."""
    yield from (FormatString(*t) for t in formatter.parse(format_str))


class FormatSpecBase(NamedTuple):
    """Represents a string that conforms to the [Format Specification Mini-Language][1] in the string module.

    [1]: https://docs.python.org/3/library/string.html#formatspec
    """
    fill: Optional[str]
    align: Optional[str]
    sign: Optional[str]
    alt: Optional[str]
    zero: Optional[int]
    width: Optional[int]
    comma: Optional[str]
    decimal: Optional[str]
    precision: Optional[int]
    type: str

    def join(self):
        return ''.join('{!s}'.format(s) for s in self if s is not None)

    def __format__(self, format_spec):
        try:
            return format(self.join(), format_spec)
        except (TypeError, ValueError):
            return super().__format__(format_spec)


# creating child class because __new__ cannot be directly overridden in NamedTuple child class (lame)
class FormatSpec(FormatSpecBase):
    __slots__ = ()

    def __new__(cls, fill, align, sign, alt, zero, width, comma, decimal, precision, type):
        to_int = lambda x: int(x) if x is not None else x
        zero = to_int(zero)
        width = to_int(width)
        precision = to_int(precision)
        return super().__new__(cls, fill, align, sign, alt, zero, width, comma, decimal, precision, type)


# Regexes for validating a string conforming to the format spec mini-language
# only mini-language types
regex_minilang = r'(([\s\S])?([<>=\^]))?([\+\-])?([#])?([0])?(\d)*([,])?((\.)(\d)*)?([sbcdoxXneEfFgGn%]|$)?'
minilang_parser = re.compile(regex_minilang)
# any type using a-zA-Z for the name
regex_custom = r'(([\s\S])?([<>=\^]))?([\+\- ])?([#])?([0])?(\d)*([,])?((\.)(\d)*)?([a-zA-Z]+|$)?'
custom_parser = re.compile(regex_custom)


def parse_spec(spec: str, strict: bool = True) -> FormatSpec:
    """Returns a FormatSpec object built from the provided spec conforming to the [format specification
    mini-language][1]. Raises ValueError if there is no match.

    strict optionally limits valid types to those specified in the format specification mini-language.

    [1]: https://docs.python.org/3/library/string.html#formatspec
    """
    parse_picker = {True: minilang_parser, False: custom_parser}
    parser = parse_picker[strict]
    match = parser.fullmatch(spec)
    try:
        # skip group numbers not interested in (1, 9)
        return FormatSpec(*match.group(2, 3, 4, 5, 6, 7, 8, 10, 11, 12))
    except AttributeError:
        raise ValueError('The provided format specification string {!r} does '
                         'not conform to the format specification mini-language.'
                         ''.format(spec)) from None


class Field(NamedTuple):
    """Represents a field with fixed width."""
    name: str
    spec: Union[FormatSpec, str]
    default: Any
    field_no: int


def make_fields(**field_defs: Tuple[Union[FormatSpec, str], Any]) -> Iterable[Field]:
    """Generate Field objects from named field definitions"""
    for i, (n, (s, d)) in enumerate(field_defs.items(), 1):
        if not isinstance(s, FormatSpec):
            # assume s contains only one format spec (error otherwise)
            fmat_str_obj, = parse_format_str(format_str=s)
            spec = parse_spec(spec=fmat_str_obj.format_spec, strict=False)
        else:
            spec = s
        yield Field(n, spec, d, i)


def make_line(**field_defs: Tuple[Union[FormatSpec, str], Any]) -> Tuple[Field, ...]:
    """Generate cid line definition from field definitions"""
    return tuple(make_fields(**field_defs))
