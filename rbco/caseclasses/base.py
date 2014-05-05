#coding=utf8
from collections import OrderedDict
from funcsigs import Parameter
from funcsigs import signature



def build_init_signature(args):
    return Signature(
        [
            Parameter(name='self', kind=Parameter.POSITIONAL_OR_KEYWORD),
        ] +
        [
            Parameter(name=k, default=v, kind=Parameter.POSITIONAL_OR_KEYWORD)
            for (k, v) in args
        ]
    )
