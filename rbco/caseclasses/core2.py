#coding=utf8
from .base import CaseClassMixin
from .base import NO_DEFAULT_VALUE
from collections import OrderedDict
from funcsigs import signature, Parameter


def case_class(name, init_func, doc=None):

    init_signature = signature(init_func)
    init_parameters = init_signature.parameters.values()

    def __init__(self, *args, **kwargs):
        for p in init_parameters:
            if p.default is not Parameter.empty:
                setattr(self, p.name, p.default)

        bound_args = init_signature.bind(*args, **kwargs)
        for (field_name, value) in bound_args.arguments.iteritems():
            setattr(self, field_name, value)

    __fields__ = OrderedDict(
        (p.name, p.default if (p.default is not Parameter.empty) else NO_DEFAULT_VALUE)
        for p in init_parameters
    )

    return type(
        name,
        (CaseClassMixin,),
        {
            '__doc__': doc,
            '__slots__': __fields__.keys(),
            '__fields__': __fields__,
            '__init__': __init__,
        }
    )


if __name__ == '__main__':

    Point = case_class(
        name='Point',
        init_func=lambda x, y=0: None,
        doc='Represent a point.'
    )

    p1 = Point(1, 2)
    p2 = Point(y=2, x=1)
    print p1, p2
    print p1 == p2
    print p1 != p2
