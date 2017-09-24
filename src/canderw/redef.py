import re
from .format_specs import d5, s8, s60, d2, d3
from .linedef import make_line

fwidth_field_format = r'(?=.{{{width}}}(?P<_skip{field_no}>.*))(?P<{label}>{pattern})(?P=_skip{field_no})'

int_right = r' *[+-]?\d+'
int_nonzero_right = r' *[+-]?[1-9]\d*'
int_blank_right = r'( *[+-]?\d+)| *'

dict(width=5, field_no=1, label='Level', pattern=int_right)

A1 = make_line(
    # ANALYS or DESIGN
    Mode=(s8, 'ANALYS'),
    # 1, 2, or 3
    Level=(d2, 3),
    Method=(d2, 1),
    NGroups=(d3, 1),
    Heading=(s60, 'CID from candemaker: Rick Teachey, rickteachey@cbceng.com'),
    Iterations=(d5, -99),
    CulvertID=(d5, 0),
    ProcessID=(d5, 0),
    SubdomainID=(d5, 0),
)
