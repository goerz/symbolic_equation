"""Tests for `symbolic_equation` package."""

from pkg_resources import parse_version

import pytest
import sympy
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
    eq = eq1.apply(sympy.simplify, cont=True)
    assert str(eq) == '2*x - y = 1    (I)\n        = 1'


def test_apply_mtd_with_same_lhs(eq1_eq2):
    """Test that "apply_mtd" that does not change the lhs will not double-print
    the lhs."""
    eq1, _ = eq1_eq2
    eq = eq1.apply_mtd('simplify', cont=True)
    assert str(eq) == '2*x - y = 1    (I)\n        = 1'


def test_apply_to_lhs_print_unchanged(eq1_eq2):
    """Test that "apply_to_lhs" always prints the lhs, even if it did not
    change"""
    eq1, _ = eq1_eq2
    eq = eq1.apply_to_lhs(sympy.simplify, cont=True)
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
        .apply(lambda v: v - ((eq1 - eq2).rhs), cont=True)
        .apply_mtd('subs', {x: 1}, cont=True)
    )
    assert str(eq) == '    x - 2*y = -4\nx - 2*y + 4 = 0\n    5 - 2*y = 0'
    assert str(eq.copy()) == str(eq)
