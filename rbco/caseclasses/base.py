#coding=utf8


class CaseClassMixin(object):

    __slots__ = tuple()

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
        try:
            return all(
                (getattr(self, field_name) == getattr(other, field_name))
                for field_name in self.__fields__
            )
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class NoDefaultValue(object):
    pass


NO_DEFAULT_VALUE = NoDefaultValue()
