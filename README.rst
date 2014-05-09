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


Compatibility
=============

Currently only Python 2.7 is supported.


Instalation
===========

The usual::

    pip install rbco.caseclasses

Or::

    easy_install rbco.caseclasses


Basic Usage
===========

Let's start by creating a simple case class::

    >>> from rbco.caseclasses import case
    >>>
    >>> @case
    ... class Person(object):
    ...     """Represent a person."""
    ...     def __init__(self, name, age=None, gender=None): pass

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

The docstring of the class is preserved::

    >>> Person.__doc__
    'Represent a person.'

The signature of the constructor is not preserved. The resulting ``__init__`` method signature
is a generic one, taking only ``*args`` and ``**kwargs``::

    >>> from inspect import getargspec
    >>> getargspec(Person.__init__)
    ArgSpec(args=['self'], varargs='args', keywords='kwargs', defaults=None)

However the docstring contains the original signature::

    >>> Person.__init__.__doc__
    'Original signature: (self, name, age=None, gender=None)'

It's not possible to create a case class without a constructor::

    >>> from rbco.caseclasses import case
    >>>
    >>> @case
    ... class Foo(object): pass
    Traceback (most recent call last):
    ...
    RuntimeError: Case class must define a constructor.


Mutability and __slots__
========================

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

This is because of the `__slots__`_ declaration::

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


.. _`custom members`:

Custom members
==============

Case classes are very much like regular classes. It's possible to define any kind of custom
members.

The most common case should be adding a custom instance method::

    >>> import math
    >>> @case
    ... class Point(object):
    ...     def __init__(self, x, y): pass
    ...
    ...     def distance(self, other):
    ...         return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    >>> p1 = Point(0, 0)
    >>> p2 = Point(10, 0)
    >>> p1.distance(p2)
    10.0

Other kinds of class members are supported as well::

    >>> @case
    ... class Example(object):
    ...     class_attribute = 'some value'
    ...
    ...     def __init__(self, field1): pass
    ...
    ...     @staticmethod
    ...     def static_method():
    ...         print 'This is an static method.'
    ...
    ...     @classmethod
    ...     def class_method(cls):
    ...         print 'This is a class method of the class {}.'.format(cls.__name__)
    ...
    >>> e = Example('example')
    >>> Example.class_attribute
    'some value'
    >>> e.class_attribute
    'some value'
    >>> Example.static_method()
    This is an static method.
    >>> Example.class_method()
    This is a class method of the class Example.


Inheritance
===========

Let's create a base case class and a derived one::

    >>> @case
    ... class Person(object):
    ...     def __init__(self, name, age=None, gender=None): pass
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
    ...     def __init__(self, name, age=None, gender=None, department=None): pass

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
    ...     def __init__(self, bar): pass
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

It's not possible to override the ``__init__`` method, because it's replaced when the ``@case``
decorator is applied. If a custom constructor is needed using the CaseClassMixin_ can be
a solution.


.. _CaseClassMixin:

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
    ...     def __init__(self, field1, *args):
    ...         self.field1 = field1 + '_modified'
    ...         self.field2 = list(args)
    ...
    >>> Foo('bar', 1, 2)
    Foo(field1='bar_modified', field2=[1, 2])


Limitations
===========

- The constructor of a case class cannot be customized because it's replaced when the ``@case``
  decorator is applied. See the section about CaseClassMixin_ for an alternative.

- It's not possible to assign to unknow fields because of the ``__slots__`` declaration.

- The constructor cannot take ``*args`` or ``**kwargs``::

    >>> @case
    ... class Foo(object):
    ...     def __init__(self, **kwargs): pass
    Traceback (most recent call last):
    ...
    RuntimeError: Case class constructor cannot take *args or **kwargs.

  See the section about CaseClassMixin_ for an alternative.


.. _motivation:

Motivation, design decisions and other implementations
======================================================

Comparison with MacroPy
-----------------------

The idea for this project came from MacroPy_. It provides an implementation of case classes using
syntactic macros, which results in a very elegant way to define the case classes.
The motivation was to provide similar functionality without resorting to syntactic macros nor
string evaluation (`the approach took by namedtuple`__). In other words: to provide the best
implementation possible without using much magic.

__ `namedtuple source code`_

The comparison to MacroPy_ can be summarized as follows:

    Advantages:

    - No magic.
    - Allows any kind of `custom members`_, including instance methods.
    - Since case classes are just regular classes, any kind of inheritance is allowed.

    Disadvantages:

    - MacroPy syntax is much nicer. The ``__init__`` stub thing can be considered kind of ugly
      in comparison.
    - Do not support custom initialization logic. This can be achieved by using CaseClassMixin_ but
      additional work will have to be done by the programmer.
    - Do not support ``*args`` and ``**kwargs`` in the constructor. Again, this can be achieved by
      using CaseClassMixin_ at the expense of doing more work.


Other implementations
---------------------

Other implementations of the "case class" concept (or similar) in Python exists:

- The constructor stub mechanism idea was stole from `this implementation`__ by hwiechers.

__ `hwiechers`_

- A simple implementation by Brian Wickman can be found in `this Gist`__.

__ `wickman gist`_

- `This discussion`__ on stackoverflow has some implementation ideas.

__ `stackoverflow discussion`_


Discarded implementation ideas
------------------------------

Some implementation ideas were considered but discarded afterwards. Here some of them are
discussed.

Functional syntax
^^^^^^^^^^^^^^^^^

This means using a function to generate the class. This would be something like this::

    Person = case_class('Person', 'name', age=None, gender=None)

The first problem with this idea is that there's no way to preserve the order of the fields.
The ``case_class`` function would have to be defined like this::

    def case_class(__name__, *args, **kwargs):
        ...

``**kwargs`` is a unordered dictionary, so the order of the fields is lost.

To overcome this the following syntax could be used::

    Person = case_class('Person', 'name', 'age', 'gender', age=None, gender=None)

I thinks this syntax is not elegant enough. I don't like the repetition of field names and to have
field names represented as both strings and parameter names.

Perhaps something like this would work too::

    Person = case_class('Person', ['name', 'age', 'gender'], {'age': None, 'gender': None})

But again I think the syntax is not elegant.

Also, some functionalities would be difficult to support using this syntax, namely:

- *Custom members*. This would mean complicate the signature of the ``case_class`` function or
  add the custom members after the class is created. Like this::

    Person = case_class('Person', ...)

    def present(self):
        print ...

    Person.present = present

  Not very elegant.

- *Inheritance*. This would require a new parameter to the ``case_class`` function, to allow to
  pass in a base class.


Fields specification as parameters to the class decorator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This would end the necessity to define an empty constructor. The syntax would be like this::

    @case(name, age=None, gender=None)
    class Person(object):
        'Represent a person.'

The same problem faced by the function syntax arises: field ordering is not preserved, since
the ``case`` function would have to accept a ``**kwargs`` argument, which is an unordered dict.

Alternate syntaxes, similar to the ones presented for the functional syntax, could overcome the
field ordering problem. However I think the solution using a ``__init__`` stub to define the
fields is more elegant.


Fields specification as class attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The syntax would be like this::

    @case
    class Person(object):
        name = NO_DEFAULT_VALUE
        age = None
        gender = None

Again, there's no way to preserve the order of the fields. The ``case`` function would have to
retrieve the class attributes from ``Person.__dic__``, which is unordered.

Maybe something like this would work::

    @case
    class Person(object):
        __fields__ = (
            ('name', NO_DEFAULT_VALUE),
            ('age', None),
            ('gender', None)
        )

However I think the solution using a ``__init__`` stub to define the fields is more elegant.

Contributing
============

Please fork this project and submit a pull request if you would like to contribute.
Thanks in advance !


.. Referências:
.. _namedtuple: https://docs.python.org/2/library/collections.html#collections.namedtuple
.. _`__slots__`: https://docs.python.org/2/reference/datamodel.html?highlight=__slots__#__slots__
.. _MacroPy: https://github.com/lihaoyi/macropy#case-classes
.. _`namedtuple source code`: https://github.com/python/cpython/blob/2.7/Lib/collections.py
.. _`wickman gist`: https://gist.github.com/wickman/857930
.. _`stackoverflow discussion`: http://stackoverflow.com/questions/1264833/python-class-factory-to-produce-simple-struct-like-classes
.. _`hwiechers`: http://hwiechers.blogspot.com.br/2010/08/case-classes-in-python.html