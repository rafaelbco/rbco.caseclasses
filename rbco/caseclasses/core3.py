#coding=utf8
from collections import OrderedDict
from .base import CaseClassMixin
from .base import NO_DEFAULT_VALUE
from funcsigs import signature, Parameter


def case(original_class):

    init_signature = signature(original_class.__init__)
    init_parameters = init_signature.parameters.values()

    def __init__(self, *args, **kwargs):
        for p in init_parameters:
            if p.default is not Parameter.empty:
                setattr(self, p.name, p.default)

        bound_args = init_signature.bind(self, *args, **kwargs)
        for (field_name, value) in bound_args.arguments.iteritems():
            setattr(self, field_name, value)

    __fields__ = OrderedDict(
        (p.name, p.default if (p.default is not Parameter.empty) else NO_DEFAULT_VALUE)
        for p in init_parameters
        if p.name != 'self'
    )

    return type(
        original_class.__name__,
        (original_class, CaseClassMixin),
        {
            '__slots__': __fields__.keys(),
            '__fields__': __fields__,
            '__init__': __init__,
        }
    )

if __name__ == '__main__':

    @case
    class Point(object):
        def __init__(self, x, y=0):
            pass

        def sum(self):
            return self.x + self.y

    p1 = Point(1, 2)
    p2 = Point(y=2, x=1)
    print p1, p2
    print p1 == p2
    print p1 != p2
    print p1.sum()
