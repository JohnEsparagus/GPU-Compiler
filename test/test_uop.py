"""Week 1 spec for your UOp class. You write uop.py; these tests tell you when it's right.

Interface contract (the only names I assume):
    from uop import UOp, Ops, dtypes
    UOp(op, src: tuple, arg)       # positional, src is a tuple
    UOp.dtype, UOp.shape           # recursive properties, computed from src
    Ops.CONST, Ops.ADD, Ops.MUL, Ops.CMPLT, Ops.STACK, Ops.INDEX
    dtypes.bool, dtypes.i32, dtypes.f32, dtypes.void

Deliberately NOT tested yet (your design decisions, write them down first):
    - bounds: inclusive or half-open? what does MOD do on negatives?
    - cost: what unit?
"""
import pytest
from uop import UOp, Ops, dtypes


def c(v):
    return UOp(Ops.CONST, (), v)


# ---- CONST: dtype comes from the arg -------------------------------------
def test_const_dtypes():
    assert c(3).dtype == dtypes.i32
    assert c(3.0).dtype == dtypes.f32
    assert c(True).dtype == dtypes.bool   # gotcha: bool is a subclass of int in Python


def test_const_is_rank_0():
    assert c(3).shape == ()


# ---- hash consing --------------------------------------------------------
def test_same_inputs_same_object():
    assert UOp(Ops.ADD, (c(1), c(2)), None) is UOp(Ops.ADD, (c(1), c(2)), None)


def test_different_arg_different_object():
    assert c(1) is not c(2)


def test_src_order_matters():
    a, b = c(1), c(2)
    assert UOp(Ops.ADD, (a, b), None) is not UOp(Ops.ADD, (b, a), None)


def test_int_and_float_consts_are_distinct():
    # 1 == 1.0 and hash(1) == hash(1.0) in Python. Your table must not merge them.
    assert c(1) is not c(1.0)
    assert c(1).dtype != c(1.0).dtype


def test_bool_and_int_consts_are_distinct():
    assert c(True) is not c(1)
def test_stuff():
    print(c(True))
    assert c(True) is not c(1)

def test_shared_subgraph_is_one_node():
    x = UOp(Ops.ADD, (c(1), c(2)), None)
    m = UOp(Ops.MUL, (x, UOp(Ops.ADD, (c(1), c(2)), None)), None)
    assert m.src[0] is m.src[1]


# ---- immutability --------------------------------------------------------
def test_cannot_mutate_fields():
    u = c(1)
    for field in ("op", "src", "arg"):
        with pytest.raises(AttributeError):
            setattr(u, field, None)


def test_src_is_a_tuple():
    assert isinstance(UOp(Ops.ADD, (c(1), c(2)), None).src, tuple)


# ---- recursive properties: dtype -----------------------------------------
def test_alu_dtype_follows_sources():
    assert UOp(Ops.ADD, (c(1), c(2)), None).dtype == dtypes.i32
    assert UOp(Ops.MUL, (c(1.0), c(2.0)), None).dtype == dtypes.f32


def test_cmplt_returns_bool():
    assert UOp(Ops.CMPLT, (c(1), c(2)), None).dtype == dtypes.bool


def test_mismatched_dtypes_rejected():
    with pytest.raises(Exception):
        UOp(Ops.ADD, (c(1), c(2.0)), None)


# ---- recursive properties: shape -----------------------------------------
def test_alu_on_rank_0_is_rank_0():
    assert UOp(Ops.ADD, (c(1), c(2)), None).shape == ()


def test_stack_adds_leading_axis():
    assert UOp(Ops.STACK, (c(1), c(2), c(3)), None).shape == (3,)


def test_stack_requires_same_shapes():
    s = UOp(Ops.STACK, (c(1), c(2)), None)
    with pytest.raises(Exception):
        UOp(Ops.STACK, (s, c(3)), None)


def test_index_pops_leading_axis():
    s = UOp(Ops.STACK, (c(1), c(2), c(3)), None)
    assert UOp(Ops.INDEX, (s, c(0)), None).shape == ()