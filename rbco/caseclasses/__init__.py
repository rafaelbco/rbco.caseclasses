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

    return type(
        __name__,
        (object,),
        {
            '__doc__': __doc__,
            '__slots__': __fields__.iterkeys(),
            '__fields__': dict(__fields__),
            '__init__': __init__,
            '__repr__': __repr__,
        }
    )


if __name__ == '__main__':

    MyClass = case_class(
        'MyClass',
        'Docstring.',
        a=1,
        b=None
    )

    o = MyClass()

    print o

    o.b = """'Blah'\""""

    print o

    o = MyClass(a=1, b='\'Blah\'"')

    from pudb import set_trace; set_trace()

