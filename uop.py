from enum import IntEnum, Enum
import weakref
'''    from uop import UOp, Ops, dtypes
    UOp(op, src: tuple, arg)       # positional, src is a tuple
    UOp.dtype, UOp.shape           # recursive properties, computed from src
    Ops.CONST, Ops.ADD, Ops.MUL, Ops.CMPLT, Ops.STACK, Ops.INDEX
    dtypes.bool, dtypes.i32, dtypes.f32, dtypes.void
'''
class Ops(IntEnum):
    ADD = 1
    MUL = 2
    STACK = 3
    INDEX = 4
    CONST = 5
    CMPLT = 6
    

class dtypes:
    def __init__(self, name:str):
        self.name = name 
    def __repr__(self):
        return f"dtypes.{self.name}"
    
dtypes.bool = dtypes("bool")
dtypes.i32 = dtypes("i32")
dtypes.f32 = dtypes("f32")
dtypes.void = dtypes("void")


class UOp:
    __slots__ = ("op", "src", "arg", "dtype", "shape", "__weakref__")    
    _table = weakref.WeakKeyDictionary()
    def __setattr__(self, k, v): raise AttributeError("immutable")
    #immutable forever

    def __new__(cls, op, src, arg):
        #before creating remove duplicate
        key = (op, src, arg)
        for i in cls._table:
            if key == i:
                cls._table[key]
        self = object.__new__(cls)
        object.__setattr__(self, op, src, arg)
        self.dtype = self._infer_dtype(arg)
        return self
    
    def _infer_dtype(self, arg) -> dtypes:
        if arg is None:
            return dtypes.void
        if isinstance(arg, bool):
            return dtypes.bool
        if isinstance(arg, int):
            return dtypes.i32
        if isinstance(arg, float):
            return dtypes.f32
        raise TypeError(f"Unsupported type: {type(arg)}")

    

    
    