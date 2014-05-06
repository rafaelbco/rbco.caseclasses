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

    @case
    class Person(object):
        def __init__(self, name, age=None, gender=None):
            pass

        def present(self):
            print "I'm {}, {} years old and my gender is '{}'.".format(
                self.name,
                self.age,
                self.gender
            )

    @case
    class Employee(Person):
        def __init__(self, name, age=None, gender=None, department=None):
            pass

    @case
    class ImprovedEmployee(Employee):
        def present(self):
            super(ImprovedEmployee, self).present()
            print 'I work in the {} department.'.format(self.department)

    from pudb import set_trace; set_trace()

    ie = ImprovedEmployee(name='Mary', department='marketing')
    ie.present()