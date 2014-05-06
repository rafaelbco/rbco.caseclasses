Overview
========

The goal of this project is to provide a compact syntax to define simple "struct-like" (or "record-
like", "bean-like") classes. The resulting classes are very similar to namedtuple_, but mutable.

Here's a summary of the features:

- Useful ``__repr__`` and ``__str__`` implementations.
- Structural equality, i.e, useful ``__eq__`` and ``__ne__`` implementations.
- ``copy`` method (copy-constructor).
- `__slots__`_ declaration to improve performance and prevent assignment on unknown fields.
- It's possible to define custom methods.
- Supports inheritance.

See also the motivation_ section for other implementations of the concept, specially MacroPy_
which is a very different approach and the inspiration for this project.


Basic Usage
===========

Let's start by creating a simple case class::

    >>> from rbco.caseclasses import case
    >>>
    >>> @case
    ... class Person(object):
    ...     def __init__(self, name, age=None, gender=None):
    ...         pass


The declared ``__init__`` is just a stub. The parameters defines which fields the class will have
and its default values. The ``__init__`` method is replaced by a new one, which takes care of
assigning the values of the fields.

The constructor works as expected, according to the provided ``__init__`` stub::

    >>> Person('John')
    Person(name='John', age=None, gender=None)
    >>> Person('John', 30, 'm')
    Person(name='John', age=30, gender='m')
    >>> Person(name='John', age=30, gender='m')
    Person(name='John', age=30, gender='m')
    >>> Person('John', gender='m')
    Person(name='John', age=None, gender='m')

Note that in the string representation the fields are in the same order as defined in the
constructor.

Instances are mutable::

    >>> p = Person('John')
    >>> p
    Person(name='John', age=None, gender=None)
    >>> p.name = 'Bob'
    >>> p.age = 35
    >>> p
    Person(name='Bob', age=35, gender=None)

However it's not possible to assign to unknown attributes::

    >>> p.department = 'sales'
    Traceback (most recent call last):
    ...
    AttributeError: 'Person' object has no attribute 'department'

This is because of the ``__slots__`` declaration::

    >>> p.__slots__
    ['name', 'age', 'gender']

Structural equality is supported::

    >>> p1 = Person('John', 30)
    >>> p2 = Person('Bob', 25)
    >>> p1 == p2
    False
    >>> p1 != p2
    True
    >>> p2.name = 'John'
    >>> p2.age = 30
    >>> p1 == p2
    True
    >>> p1 != p2
    False
    >>> p2.gender = 'm'
    >>> p1 == p2
    False

A copy constructor is provided::

    >>> p1 = Person('John', 30)
    >>> copy_of_p1 = p1.copy()
    >>> p1
    Person(name='John', age=30, gender=None)
    >>> copy_of_p1
    Person(name='John', age=30, gender=None)
    >>> p1 is copy_of_p1
    False
    >>> p2 = p1.copy(name='Bob', gender='m')
    >>> p2
    Person(name='Bob', age=30, gender='m')


Custom methods
==============

Case classes are very much like regular classes. It's possible to define custom methods in the
standard way::

    >>> import math
    >>> @case
    ... class Point(object):
    ...     def __init__(self, x, y):
    ...         pass
    ...
    ...     def distance(self, other):
    ...         return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    >>> p1 = Point(0, 0)
    >>> p2 = Point(10, 0)
    >>> p1.distance(p2)
    10.0


Inheritance
===========

Let's create a base case class and a derived one::

    >>> @case
    ... class Person(object):
    ...     def __init__(self, name, age=None, gender=None):
    ...         pass
    ...
    ...     def present(self):
    ...         print "I'm {}, {} years old and my gender is '{}'.".format(
    ...             self.name,
    ...             self.age,
    ...             self.gender
    ...         )
    ...
    >>> @case
    ... class Employee(Person):
    ...     def __init__(self, name, age=None, gender=None, department=None):
    ...         pass

It's necessary to repeat the fields of the base class, but you would have to do that anyway if
you were implementing the case classes manually.

Methods from the base class are inherited and works as expected::

    >>> p = Person('John', 30, 'm')
    >>> p.present()
    I'm John, 30 years old and my gender is 'm'.
    >>> e = Employee('Mary', 33, 'f', 'sales')
    >>> e.present()
    I'm Mary, 33 years old and my gender is 'f'.

Instances of ``Person`` and ``Employee`` will always be considered different, since employees
have an extra field::

    >>> p = Person('John')
    >>> e = Employee('John')
    >>> p == e
    False

Of course the subclass can override a method on the base class::

    >>> @case
    ... class ImprovedEmployee(Employee):
    ...     def present(self):
    ...         super(ImprovedEmployee, self).present()
    ...         print 'I work in the {} department.'.format(self.department)
    ...
    >>> ie = ImprovedEmployee(name='Mary', department='marketing')
    >>> ie.present()
    I'm Mary, None years old and my gender is 'None'.
    I work in the marketing department.


Limitations
===========

Case class constructor cannot take *args or **kwargs.


.. _motivation:

Motivation and other implementations
====================================


https://github.com/lihaoyi/macropy#case-classes

http://www.codecommit.com/blog/scala/case-classes-are-cool

https://gist.github.com/wickman/857930

http://stackoverflow.com/questions/1264833/python-class-factory-to-produce-simple-struct-like-classes

http://hwiechers.blogspot.com.br/2010/08/case-classes-in-python.html


.. Referências:
.. _namedtuple:
.. _`__slots__`:
.. _MacroPy: https://github.com/lihaoyi/macropy#case-classes