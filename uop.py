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
    __slots__ = ("op", "src", "type", "arg", "dtype", "shape", "__weakref__")    
    _table = weakref.WeakValueDictionary()
    def __setattr__(self, k, v): raise AttributeError("immutable")
    #immutable forever

    def __new__(cls, op, src, arg):
        key = (op, src, type(arg), arg)

        #before creating remove duplicate
        if cls._table.get(key) is not None:
            return cls._table.get(key)
            
        self = object.__new__(cls)
        object.__setattr__(self, "op", op)    #
        object.__setattr__(self, "src", src)
        object.__setattr__(self, "type", type(arg))
        object.__setattr__(self, "arg", arg)
        cls._table[key] = self
        cls.dtype = cls._infer_dtype(self,op, arg, src)
        cls.shape = cls._infer_shape(self,op, src)
        return self
    
    def _infer_shape(self, op, src):
        if not src:
            return ()
        if op == 1 or op == 2:
            if all(src[0].shape == i.shape for i in src):
                return src[0].shape  
        if op == 3:
            if not isinstance(src, list):
                return ()
            elif not src:
                return ()
            return (len(src),) + self._infer_shape(3,src[0])            
        if op == 4:
            return self._infer_shape(3, src[0])[1:]
        raise TypeError(f"Unsupported type: {type(arg)}")

    def _infer_dtype(self, op, arg, src) -> dtypes:
        if op == 5:
            if arg is None:
                return dtypes.void
            if isinstance(arg, bool):
                return dtypes.bool
            if isinstance(arg, int):
                return dtypes.i32
            if isinstance(arg, float):
                return dtypes.f32
        if op == 6:
            if all(src[0].dtype == i.dtype for i in src):
                return dtypes.bool
        if op  == 1 or op == 2:
            if all(src[0].dtype == i.dtype for i in src):
                return src[0].dtype

        raise TypeError(f"Unsupported type: {type(arg)}")

    

    
    