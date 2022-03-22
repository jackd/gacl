import functools
import operator

import gin

register = functools.partial(gin.register, module="operator")

for op in (
    operator.abs,
    operator.add,
    operator.and_,
    # operator.attrgetter,
    operator.concat,
    operator.contains,
    operator.countOf,
    operator.delitem,
    operator.eq,
    operator.floordiv,
    operator.ge,
    operator.getitem,
    operator.gt,
    operator.iadd,
    operator.iand,
    operator.iconcat,
    operator.ifloordiv,
    operator.ilshift,
    operator.imatmul,
    operator.imod,
    operator.imul,
    operator.index,
    operator.indexOf,
    operator.inv,
    operator.invert,
    operator.ior,
    operator.ipow,
    operator.irshift,
    operator.is_,
    operator.is_not,
    operator.isub,
    # operator.itemgetter,
    operator.itruediv,
    operator.ixor,
    operator.le,
    operator.length_hint,
    operator.lshift,
    operator.lt,
    operator.matmul,
    # operator.methodcaller,
    operator.mod,
    # operator.mul,
    operator.ne,
    operator.neg,
    operator.not_,
    operator.or_,
    operator.pos,
    operator.pow,
    operator.rshift,
    operator.setitem,
    operator.sub,
    # operator.truediv,
    operator.truth,
    operator.xor,
):
    gin.register(op, module="operator")


@register
def truediv(a, b):
    return operator.truediv(a, b)


@register
def mul(a, b):
    return operator.mul(a, b)
