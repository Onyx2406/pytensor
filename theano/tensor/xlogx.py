import numpy as np

from theano import scalar as ts
from theano.tensor.elemwise import Elemwise


class XlogX(ts.UnaryScalarOp):
    """
    Compute X * log(X), with special case 0 log(0) = 0.

    """

    @staticmethod
    def st_impl(x):
        if x == 0.0:
            return 0.0
        return x * np.log(x)

    def impl(self, x):
        return XlogX.st_impl(x)

    def grad(self, inputs, grads):
        (x,) = inputs
        (gz,) = grads
        return [gz * (1 + ts.log(x))]

    def c_code(self, node, name, inputs, outputs, sub):
        (x,) = inputs
        (z,) = outputs
        if node.inputs[0].type in [ts.float32, ts.float64]:
            return f"""{z} =
                {x} == 0.0
                ? 0.0
                : {x} * log({x});"""
        raise NotImplementedError("only floatingpoint is implemented")


scalar_xlogx = XlogX(ts.upgrade_to_float, name="scalar_xlogx")
xlogx = Elemwise(scalar_xlogx, name="xlogx")


class XlogY0(ts.BinaryScalarOp):
    """
    Compute X * log(Y), with special case 0 log(0) = 0.

    """

    @staticmethod
    def st_impl(x, y):
        if x == 0.0:
            return 0.0
        return x * np.log(y)

    def impl(self, x, y):
        return XlogY0.st_impl(x, y)

    def grad(self, inputs, grads):
        x, y = inputs
        (gz,) = grads
        return [gz * ts.log(y), gz * x / y]

    def c_code(self, node, name, inputs, outputs, sub):
        x, y = inputs
        (z,) = outputs
        if node.inputs[0].type in [ts.float32, ts.float64]:
            return f"""{z} =
                {x} == 0.0
                ? 0.0
                : {x} * log({y});"""
        raise NotImplementedError("only floatingpoint is implemented")


scalar_xlogy0 = XlogY0(ts.upgrade_to_float, name="scalar_xlogy0")
xlogy0 = Elemwise(scalar_xlogy0, name="xlogy0")
