#coding=utf8
from collections import OrderedDict
from funcsigs import Parameter
from funcsigs import signature
from funcsigs import Signature


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


def build_case_class(original_class, init_signature=None):
    if init_signature is None:
        init_signature = signature(original_class.__init__)

    __fields__ = OrderedDict(
        (p.name, p.default if (p.default is not Parameter.empty) else NO_DEFAULT_VALUE)
        for p in init_signature.parameters.values()
        if p.name != 'self'
    )

    def __init__(self, *args, **kwargs):
        for (field_name, default_value) in self.__fields__.iteritems():
            setattr(self, field_name, default_value)

        bound_args = init_signature.bind(self, *args, **kwargs)
        for (field_name, value) in bound_args.arguments.iteritems():
            if field_name == 'self':
                continue
            setattr(self, field_name, value)

    __dict__ = {
        '__fields__': __fields__,
        '__slots__': __fields__.keys(),
        '__doc__': original_class.__doc__,
        '__init__': __init__,
    }
    __dict__.update(
        (k, v)
        for (k, v) in original_class.__dict__.iteritems()
        if not k.startswith('__')
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


def init_signature_from_args(*args, **kwargs):
    return Signature(
        [
            Parameter(name='self', kind=Parameter.POSITIONAL_OR_KEYWORD),
        ] +
        [
            Parameter(name=a, kind=Parameter.POSITIONAL_OR_KEYWORD)
            for a in args
        ] +
        [
            Parameter(name=k, kind=Parameter.POSITIONAL_OR_KEYWORD, default=v)
            for (k, v) in kwargs.iteritems()
        ]
    )
