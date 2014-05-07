.. contents::

Overview
========

The goal of this project is to provide a compact syntax to define simple "struct-like" (or "record-
like", "bean-like") classes. The resulting classes are very similar to namedtuple_, but mutable,
with a nicer syntax, more flexibility and more features.

Here's a summary of the features:

- It's possible to define default values for fields.
- Useful ``__repr__`` and ``__str__`` implementations.
- Structural equality, i.e, useful ``__eq__`` and ``__ne__`` implementations.
- ``copy`` method (copy-constructor).
- Conversion from/to dictionary and tuple.
- `__slots__`_ declaration to improve performance and prevent assignment on unknown fields.
- It's possible to define custom methods.
- Supports inheritance.

See also the motivation_ section for other implementations of the concept, specially MacroPy_
which was the inspiration for this project and uses a very different approach.


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


Structural equality
===================

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


Copy-constructor
================

A copy-constructor is provided::

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


Conversion from/to dictionary and tuple
=======================================

Conversion from/to dictionary is easy. The ``as_dict`` method return an ``OrderedDict``::

    >>> p1 = Person('Mary', 33)
    >>> p1
    Person(name='Mary', age=33, gender=None)
    >>> p1.as_dict()
    OrderedDict([('name', 'Mary'), ('age', 33), ('gender', None)])
    >>> Person(**p1.as_dict())
    Person(name='Mary', age=33, gender=None)

Conversion from/to tuple is also possible::

    >>> p1 = Person('John', 30)
    >>> p1
    Person(name='John', age=30, gender=None)
    >>> p1.as_tuple()
    ('John', 30, None)
    >>> Person(*p1.as_tuple())
    Person(name='John', age=30, gender=None)


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

Methods from the base class are inherited::

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

Overriding a base class method works as expected::

    >>> @case
    ... class ImprovedEmployee(Employee):
    ...     def present(self):
    ...         super(ImprovedEmployee, self).present()
    ...         print 'I work at the {} department.'.format(self.department)
    ...
    >>> ie = ImprovedEmployee(name='Mary', department='marketing', age=33, gender='f')
    >>> ie.present()
    I'm Mary, 33 years old and my gender is 'f'.
    I work at the marketing department.


Overriding case class behavior
==============================

It's possible to override the standard case class methods (``__repr__``, ``__eq__``, etc).
For example::

    >>> @case
    ... class Foo(object):
    ...     def __init__(self, bar):
    ...         pass
    ...
    ...     def __eq__(self, other):
    ...         return True  # All `Foo`s are equal.
    ...
    >>> Foo('bar') == Foo('baz')
    True

It's even possible to call the original version on the subclass method::

    >>> @case
    ... class Foo(object):
    ...     def __init__(self, bar):
    ...         pass
    ...
    ...     def __repr__(self):
    ...         return 'This is my string representation: ' + super(Foo, self).__repr__()
    ...
    >>> Foo('bar')
    This is my string representation: Foo(bar='bar')

.. IMPORTANT::
   It's not possible to override the ``__init__`` method, because it's replaced when the ``@case``
   decorator is applied. If a custom constructor is needed using the CaseClassMixin__ can be
   a solution.

__ mixin_


.. _mixin:
Using ``CaseClassMixin`` for more flexibility
=============================================

The classes created by the ``@case`` decorator inherits from ``CaseClassMixin``.

    >>> from rbco.caseclasses import CaseClassMixin
    >>> issubclass(Person, CaseClassMixin)
    True

The ``CaseClassMixin`` provides all the "case class" behavior, except for the constructor.
To use ``CaseClassMixin`` directly the only requirement the subclass must match is to provide a
``__fields__`` attribute, containing a sequence of field names.

This can be useful if greater flexibility is required. In the following example we create a case
class with a custom constructor::

    >>> class Foo(CaseClassMixin):
    ...     __fields__ = ('field1', 'field2')
    ...
    ...     def __init__(self, field1, field2=None):
    ...         self.field1 = field1 + '_modified'
    ...         self.field2 = field2 or [1, 2]
    ...
    >>> Foo('bar')
    Foo(field1='bar_modified', field2=[1, 2])


Limitations
===========

- The constructor of a case class cannot be customized because it's replaced when the ``@case``
  decorator is applied.

- It's not possible to assign to unknow fields because of the ``__slots__`` declaration.


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
