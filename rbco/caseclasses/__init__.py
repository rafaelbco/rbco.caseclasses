#coding=utf8


class NoDefaultValue(object):
    pass

NO_DEFAULT_VALUE = NoDefaultValue()


def case_class(__name__, __doc__=None, **__fields__):

    def __init__(self, **kwargs):
        for (field_name, default_value) in self.__fields__.iteritems():
            value = kwargs.get(field_name, default_value)
            if value is NO_DEFAULT_VALUE:
                raise AttributeError('Field {} is required.'.format(field_name))

            setattr(self, field_name, value)

        for (field_name, value) in kwargs.iteritems():
            setattr(self, field_name, value)

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

    return type(
        __name__,
        (object,),
        {
            '__doc__': __doc__,
            '__slots__': __fields__.iterkeys(),
            '__fields__': dict(__fields__),
            '__init__': __init__,
            '__repr__': __repr__,
            '__eq__': __eq__,
            '__ne__': __ne__,
        }
    )


if __name__ == '__main__':

    MyClass = case_class(
        'MyClass',
        'Docstring.',
        a=1,
        b=None
    )

    o1 = MyClass()
    o2 = MyClass(b=2)

    print o1
    print o2
    print o1 == o2
    print o1 != o2

    from pudb import set_trace; set_trace()

    o1.b = 2
    print o1 == o2
    print o1 != o2
