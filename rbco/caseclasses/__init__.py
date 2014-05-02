#coding=utf8
from itertools import izip
from collections import OrderedDict


class NoDefaultValue(object):
    pass

NO_DEFAULT_VALUE = NoDefaultValue()


def case_class(name, fields, default_values=None, doc=None):

    default_values = default_values or {}

    for field_name in default_values:
        if field_name not in fields:
            raise RuntimeError(
                'Field "{}" is in `default_values` but not in `fields`.'.format(field_name)
            )

    def __init__(self, *args, **kwargs):
        num_args = len(args) + len(kwargs)
        num_fields = len(self.__fields__)
        if num_args > num_fields:
            raise RuntimeError(
                '{} field values were provided but only {} exists.'.format(num_args, num_fields)
            )

        for field_name in kwargs:
            if field_name not in self.__fields__:
                raise AttributeError('Field {} does not exist.'.format(field_name))

        for (field_name, default_value) in self.__fields__.iteritems():
            setattr(self, field_name, default_value)

        for (field_name, value) in izip(fields, args):
            setattr(self, field_name, value)

        for (field_name, value) in kwargs.iteritems():
            setattr(self, field_name, value)

        for field_name in self.__fields__:
            if getattr(self, field_name) == NO_DEFAULT_VALUE:
                raise AttributeError('Field "{}" is required.'.format(field_name))

    def copy(self, **kwargs):
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
        return all(
            (getattr(self, field_name) == getattr(other, field_name))
            for field_name in self.__fields__
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    __fields__ = OrderedDict.fromkeys(fields, NO_DEFAULT_VALUE)
    __fields__.update(default_values)

    return type(
        name,
        (object,),
        {
            '__doc__': doc,
            '__slots__': __fields__.iterkeys(),
            '__fields__': __fields__,
            '__init__': __init__,
            '__repr__': __repr__,
            '__eq__': __eq__,
            '__ne__': __ne__,
            'copy': copy,
        }
    )


if __name__ == '__main__':

    Point = case_class(
        name='Point',
        fields=('x', 'y'),
        default_values={'y': 0},
        doc='Represent a point.',
    )

    p1 = Point(1, 2)
    p2 = Point(y=2, x=1)
    print p1, p2
    print p1 == p2
    print p1 != p2

    from pudb import set_trace; set_trace()

