"""Tests for `symbolic_equation` package."""

import pytest
import sympy
from pkg_resources import parse_version
from sympy import symbols, sympify

import symbolic_equation
from symbolic_equation import Eq


def test_valid_version():
    """Check that the package defines a valid __version__"""
    assert parse_version(symbolic_equation.__version__) >= parse_version(
        "0.1.0-dev"
    )


@pytest.fixture
def eq1_eq2():
    """Two exemplary equations"""
    x, y = symbols('x y')
    eq1 = Eq(2 * x - y, sympify(1), tag='I')
    eq2 = Eq(x + y, sympify(5), tag='II')
    return eq1, eq2


def test_apply_with_same_lhs(eq1_eq2):
    """Test that "apply" that does not change the lhs will not double-print the
    lhs."""
    eq1, _ = eq1_eq2
    eq = eq1.apply(sympy.simplify)
    assert str(eq) == '2*x - y = 1    (I)\n        = 1'


def test_apply_mtd_with_same_lhs(eq1_eq2):
    """Test that "apply" of method that does not change the lhs will not
    double-print the lhs."""
    eq1, _ = eq1_eq2
    eq = eq1.apply('simplify')
    assert str(eq) == '2*x - y = 1    (I)\n        = 1'


def test_apply_to_lhs_print_unchanged(eq1_eq2):
    """Test that "apply_to_lhs" always prints the lhs, even if it did not
    change"""
    eq1, _ = eq1_eq2
    eq = eq1.apply_to_lhs(sympy.simplify)
    assert str(eq) == '2*x - y = 1    (I)\n2*x - y = 1'


def test_add_equations(eq1_eq2):
    """Test adding two equations"""
    eq1, eq2 = eq1_eq2
    eq = eq1 + eq2
    assert eq.lhs == 3 * symbols('x')
    assert eq.rhs == 6


def test_add_const(eq1_eq2):
    """Test adding a constant to an equation"""
    eq1, _ = eq1_eq2
    eq = eq1 + 1
    assert eq.lhs == eq1.lhs + 1
    assert eq.rhs == eq1.rhs + 1
    assert eq1 + 1 == 1 + eq1


def test_subtract_equations(eq1_eq2):
    """Test adding two equations"""
    eq1, eq2 = eq1_eq2
    eq = eq1 - eq2
    x, y = symbols('x y')
    assert eq.lhs == x - 2 * y
    assert eq.rhs == -4


def test_subtract_const(eq1_eq2):
    """Test subtracing a constant to an equation"""
    eq1, _ = eq1_eq2
    eq = eq1 - 1
    assert eq.lhs == eq1.lhs - 1
    assert eq.rhs == eq1.rhs - 1
    assert eq == -1 * (1 - eq1)


def test_mul(eq1_eq2):
    """Test multiplication of equation with constant"""
    eq1, _ = eq1_eq2
    assert 2 * eq1 == eq1 * 2


def test_equality(eq1_eq2):
    """Test equality of equations with other equations and constants"""
    eq1, eq2 = eq1_eq2
    assert eq1 == eq1
    assert eq1 != eq2
    assert eq1 == 1
    assert eq1 != 0


def test_copy_preserves_history(eq1_eq2):
    """Test that copying preserves the history"""
    eq1, eq2 = eq1_eq2
    x = symbols('x')
    eq = (
        (eq1 - eq2)
        .apply(lambda v: v - ((eq1 - eq2).rhs))
        .apply('subs', {x: 1})
    )
    assert str(eq) == '    x - 2*y = -4\nx - 2*y + 4 = 0\n    5 - 2*y = 0'
    assert str(eq.copy()) == str(eq)


def test_amend(eq1_eq2):
    """Test amending previous lines"""
    eq1, eq2 = eq1_eq2
    x = symbols('x')
    z = symbols('z')
    eq_y = (
        (eq1 - 2 * eq2)
        .tag("I - 2 II")
        .apply(lambda v: v - 9)
        .apply(lambda v: v / (-3))
    )
    eq_x = eq1.apply_to_lhs('subs', eq_y.as_dict).reset().tag(r'y in I')

    # fmt: off
    eq_x_sol = (
        eq_x
        .apply(lambda v: v + 3)
        .apply(lambda v: v / 2).amend().tag('x')
    )
    # fmt: on
    assert eq_x_sol.lhs == x
    assert eq_x_sol.rhs == 2
    assert str(eq_x_sol) == '2*x - 3 = 1    (y in I)\n      x = 2    (x)'

    # fmt: off
    eq_z = (
        eq_x
        .apply_to_lhs('subs', {x: z + 1})
        .apply_to_lhs('subs', {z: 1}).amend()
    )
    # fmt: on
    assert eq_z.lhs == eq_z.rhs == 1
    assert str(eq_z) == '2*x - 3 = 1    (y in I)\n      1 = 1'

    # fmt: off
    eq_z = (
        Eq(eq_x.rhs, eq_x.lhs)
        .apply_to_rhs('subs', {x: z + 1})
        .apply_to_rhs('subs', {z: 1}).amend()
    )
    # fmt: on
    assert eq_z.lhs == eq_z.rhs == 1
    assert str(eq_z) == '1 = 2*x - 3\n  = 1'


def test_reset_idempotence(eq1_eq2):
    """Test that 'reset' on a single-line equation preserves the equation."""
    eq1, _ = eq1_eq2
    assert eq1.reset() == eq1
    assert eq1.reset()._tag == eq1._tag


def test_amend_idempotence(eq1_eq2):
    """Test that 'amend' on a single-line equation preserves the equation."""
    eq1, _ = eq1_eq2
    assert eq1.amend() == eq1
    assert eq1.amend()._tag == eq1._tag
