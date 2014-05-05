#coding=utf8
from funcsigs import Parameter
from funcsigs import signature


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


def case(original_class):
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
