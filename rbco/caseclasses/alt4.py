#coding=utf8
from funcsigs import signature
from .base import build_case_class


def case_class(name, init_func, doc=None):
    original_class = type(
        name,
        (object,),
        {
            '__doc__': doc,
        }
    )
    return build_case_class(original_class=original_class, init_signature=signature(init_func))


if __name__ == '__main__':

    Point = case_class(
        name='Point',
        init_func=lambda self, x, y=0: None,
        doc='Represent a point.'
    )

    p1 = Point(1, 2)
    p2 = Point(y=2, x=1)
    print p1, p2
    print p1 == p2
    print p1 != p2
