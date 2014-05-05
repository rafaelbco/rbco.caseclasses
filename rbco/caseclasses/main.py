#coding=utf8
from . import case

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
    print p3
