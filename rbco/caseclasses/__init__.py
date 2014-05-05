#coding=utf8
from funcsigs import Parameter
from funcsigs import signature


class CaseClassMixin(object):
    """
    Mixin to add "case class" behavior to a class.

    The subclass must implement a `__fields__` attribute, containing a sequence of field names.
    """

    __slots__ = tuple()

    def copy(self, **kwargs):
        """Copy constructor. Create a shallow copy of the instance.

        Example::

            a = Point(1, 2)
            b = b.copy(x=3)
            print a  # Point(x=1, y=2)
            print b  # Point(x=3, y=2)
        """
        d = dict(
            (field_name, getattr(self, field_name))
            for field_name in self.__fields__
        )
        d.update(kwargs)
        return self.__class__(**d)

    def __repr__(self):
        fields_repr = ', '.join(
            '{k}={v}'.format(k=k, v=repr(getattr(self, k)))
            for k
            in self.__fields__
        )
        return '{name}({fields_repr})'.format(
            name=type(self).__name__,
            fields_repr=fields_repr
        )

    def __eq__(self, other):
        try:
            return all(
                (getattr(self, field_name) == getattr(other, field_name))
                for field_name in self.__fields__
            )
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def case(original_class):
    """Decorator to create a "case class".

    An empty (no-op) constructor must be provided in the decorated class. The parameter
    specification of the constructor will provide the field names and its default values.

    Example::

        @case
        class Point(object):
            def __init__(self, x, y):
                pass

        print Point(1, 2)  # Point(x=1, y=2)

    Example using default values::

        @case
        class Person(object):
            def __init__(self, name, age=None, department='sales'):
                pass

        print Person('John', 30)
        # Person(name='John', age=30, department='sales')

        print Person('John', department='marketing')
        # Person(name='John', age=None, department='marketing')
    """
    init_signature = signature(original_class.__init__)
    init_parameters = init_signature.parameters.values()

    def __init__(self, *args, **kwargs):
        for p in init_parameters:
            if p.default is not Parameter.empty:
                setattr(self, p.name, p.default)

        bound_args = init_signature.bind(self, *args, **kwargs)
        for (field_name, value) in bound_args.arguments.iteritems():
            if field_name == 'self':
                continue
            setattr(self, field_name, value)

    __fields__ = [p.name for p in init_parameters if p.name != 'self']
    __dict__ = {
        '__fields__': __fields__,
        '__slots__': __fields__,
        '__doc__': original_class.__doc__,
        '__init__': __init__,
    }
    __dict__.update(
        (k, v)
        for (k, v) in original_class.__dict__.iteritems()
        if not (k.startswith('__') and k.endswith('__'))
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
