#coding=utf8


def case_class(name, **fields):

    class C(object):

        def __init__(self, **kwargs):
            for (field_name, default_value) in self.__fields__.iteritems():
                setattr(self, field_name, default_value)

            for (field_name, value) in kwargs.iteritems():
                if field_name not in self.__fields__:
                    raise AttributeError('Unknown field: {}'.format(field_name))
                setattr(self, field_name, value)

        def __repr__(self):
            # TODO: Read __repr__ formal spec
            fields_repr = ', '.join(
                '{k}={v}'.format(k=k, v=repr(getattr(self, k)))
                for k
                in self.__fields__
            )
            return '{name}({fields_repr})'.format(
                name=type(self).__name__,
                fields_repr=fields_repr
            )

    C.__name__ = name
    C.__fields__ = dict(fields)

    return C


if __name__ == '__main__':

    MyClass = case_class(
        'MyClass',
        a=1,
        b=None
    )

    o = MyClass()

    print o

    o.b = """'Blah'\""""

    print o

    o = MyClass(a=1, b='\'Blah\'"')

    from pudb import set_trace; set_trace()

