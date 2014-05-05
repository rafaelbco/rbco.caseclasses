#coding=utf8
from collections import OrderedDict
from .base import CaseClassMixin
from .base import NO_DEFAULT_VALUE
from funcsigs import signature, Parameter


def case(original_class):

    init_signature = signature(original_class.__init__)
    __fields__ = OrderedDict(
        (p.name, p.default if (p.default is not Parameter.empty) else NO_DEFAULT_VALUE)
        for p in init_signature.parameters.values()
        if p.name != 'self'
    )

    def __init__(self, *args, **kwargs):
        for (field_name, default_value) in self.__fields__.iteritems():
            setattr(self, field_name, default_value)

        bound_args = init_signature.bind(self, *args, **kwargs)
        for (field_name, value) in bound_args.arguments.iteritems():
            if field_name == 'self':
                continue
            setattr(self, field_name, value)

    __dict__ = {
        '__fields__': __fields__,
        '__slots__': __fields__.keys(),
        '__doc__': original_class.__doc__,
        '__init__': __init__,
    }
    __dict__.update(
        (k, v)
        for (k, v) in original_class.__dict__.iteritems()
        if not k.startswith('__')
    )

    if issubclass(original_class, CaseClassMixin):
        bases = original_class.__bases__
    else:
        bases = [b for b in original_class.__bases__ if b is not object]
        bases.append(CaseClassMixin)

    return type(
        original_class.__name__,
        tuple(bases),
        __dict__
    )

if __name__ == '__main__':

    @case
    class Point(object):
        """Represent a point."""
        def __init__(self, x, y=0):
            pass

        def sum(self):
            return self.x + self.y

    @case
    class ExtendedPoint(Point):
        def __init__(self, x, y=0, z=0):
            pass

    p1 = Point(1, 2)
    p2 = Point(y=2, x=1)
    print p1, p2
    print p1 == p2
    print p1 != p2
    print p1.sum()

    p3 = ExtendedPoint(10, 20, 30)
