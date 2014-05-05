#coding=utf8
from .base import build_case_class
from funcsigs import Parameter
from funcsigs import Signature
from functools import partial


def case(*args, **kwargs):

    init_signature = Signature(
        [
            Parameter(name='self', kind=Parameter.POSITIONAL_OR_KEYWORD),
        ] +
        [
            Parameter(name=a, kind=Parameter.POSITIONAL_OR_KEYWORD)
            for a in args
        ] +
        [
            Parameter(name=k, kind=Parameter.POSITIONAL_OR_KEYWORD, default=v)
            for (k, v) in kwargs.iteritems()
        ]
    )

    return partial(build_case_class, init_signature=init_signature)

if __name__ == '__main__':

    @case('x', y=0)
    class Point(object):
        """Represent a point."""

        def sum(self):
            return self.x + self.y

    @case('x', y=0, z=0)
    class ExtendedPoint(Point):
        pass

    p1 = Point(1, 2)
    p2 = Point(y=2, x=1)
    print p1, p2
    print p1 == p2
    print p1 != p2
    print p1.sum()

    p3 = ExtendedPoint(10, 20, 30)
