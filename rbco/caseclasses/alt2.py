#coding=utf8
from .base import build_case_class
from .base import init_signature_from_args


def case_class(__name__, *args, **kwargs):
    __doc__ = kwargs.pop('__doc__', None)
    original_class = type(
        __name__,
        (object,),
        {
            '__doc__': __doc__,
        }
    )

    return build_case_class(
        original_class=original_class,
        init_signature=init_signature_from_args(*args, **kwargs)
    )


if __name__ == '__main__':

    Point = case_class(
        'Point',
        'x',
        y=0,
        __doc__='Represent a point.',
    )

    p1 = Point(1, 2)
    p2 = Point(y=2, x=1)
    print p1, p2
    print p1 == p2
    print p1 != p2
