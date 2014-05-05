#coding=utf8
from .base import build_case_class
from funcsigs import Signature
from funcsigs import Parameter


def case_class(name, fields, default_values=None, doc=None):
    for field_name in default_values:
        if field_name not in fields:
            raise RuntimeError(
                'Field "{}" is in `default_values` but not in `fields`.'.format(field_name)
            )

    original_class = type(
        name,
        (object,),
        {
            '__doc__': doc,
        }
    )

    init_signature = Signature(
        [
            Parameter(name='self', kind=Parameter.POSITIONAL_OR_KEYWORD),
        ] +
        [
            Parameter(
                name=f,
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=default_values.get(f, Parameter.empty)
            )
            for f in fields
        ]
    )

    return build_case_class(original_class=original_class, init_signature=init_signature)


if __name__ == '__main__':

    Point = case_class(
        name='Point',
        fields=('x', 'y'),
        default_values={'y': 0},
        doc='Represent a point.',
    )

    p1 = Point(1, 2)
    p2 = Point(y=2, x=1)
    print p1, p2
    print p1 == p2
    print p1 != p2
