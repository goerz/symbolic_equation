=================
symbolic_equation
=================

.. image:: https://img.shields.io/badge/github-goerz/symbolic_equation-blue.svg
   :alt: Source code on Github
   :target: https://github.com/goerz/symbolic_equation
.. image:: https://img.shields.io/pypi/v/symbolic_equation.svg
   :alt: SymbolicEquation on the Python Package Index
   :target: https://pypi.python.org/pypi/symbolic_equation
.. image:: https://img.shields.io/travis/goerz/symbolic_equation.svg
   :alt: Travis Continuous Integration
   :target: https://travis-ci.org/goerz/symbolic_equation
.. image:: https://img.shields.io/coveralls/github/goerz/symbolic_equation/master.svg
   :alt: Coveralls
   :target: https://coveralls.io/github/goerz/symbolic_equation?branch=master
.. image:: https://img.shields.io/badge/License-BSD-green.svg
   :alt: BSD License
   :target: https://opensource.org/licenses/BSD-3-Clause

A simple Python package providing the ``Eq`` class for manipulating symbolic
equations.

The ``Eq`` class defines an equation, and allows to apply arbitrary
manipulations to the left-hand-side and/or right-hand-side of that equation. It
optionally keeps track all of these manipulations, and displays them neatly as a
multi-line equation in an interactive interpreter session or a `Jupyter
notebook`_ (using a LaTeX representation). It is mainly intended for use with
SymPy_.

Development of the ``symbolic_equation`` package happens on `Github`_.


Installation
------------

To install the latest released version of ``symbolic_equation``, run this command in your terminal:

.. code-block:: console

    $ pip install symbolic_equation

This is the preferred method to install ``symbolic_equation``, as it will always install the most recent stable release.

If you don't have `pip`_ installed, the `Python installation guide`_, respectively the `Python Packaging User Guide`_  can guide
you through the process.

To install the latest development version of ``symbolic_equation`` from `Github`_.

.. code-block:: console

    $ pip install git+https://github.com/goerz/symbolic_equation.git@master#egg=symbolic_equation


Example
-------

.. code-block:: pycon

    >>> from symbolic_equation import Eq
    >>> from sympy import symbols
    >>> x, y = symbols('x y')
    >>> eq1 = Eq(2*x - y - 1, tag='I')
    >>> eq1
    2*x - y - 1 = 0    ('I')

    >>> eq2 = Eq(x + y - 5, tag='II')
    >>> eq2
    x + y - 5 = 0    ('II')

    >>> eq_y = (
    ...     (eq1 - 2 * eq2).set_tag("I - 2 II")
    ...     .apply(lambda v: v - 9, cont=True)
    ...     .apply(lambda v: v / (-3), cont=True, tag='y')
    ... )
    >>> eq_y
    9 - 3*y = 0     ('I - 2 II')
       -3*y = -9
          y = 3     ('y')

    >>> eq_x = (
    ...     eq1.apply_mtd_to_lhs('subs', eq_y.as_dict, tag=r'y in I')
    ...     .apply(lambda v: v / 2, cont=True)
    ...     .apply(lambda v: v + 2, cont=True, tag='x')
    ... )
    >>> eq_x
    2*x - 4 = 0    ('y in I')
      x - 2 = 0
          x = 2    ('x')

Reference
---------

.. code-block:: pycon

   >>> help(Eq)  # doctest: +NORMALIZE_WHITESPACE
   Help on class Eq in module symbolic_equation:
   <BLANKLINE>
   class Eq(builtins.object)
    |  Eq(lhs, rhs=None, tag=None, _prev_lhs=None, _prev_rhs=None, _prev_tags=None)
    |
    |  Symbolic equation.
    |
    |  This class keeps track of the :attr:`lhs` and :attr:`rhs` of an equation
    |  across arbitrary manipulations.
    |
    |  Args:
    |      lhs: the left-hand-side of the equation
    |      rhs: the right-hand-side of the equation. If None, defaults to zero.
    |      tag: a tag (equation number) to be shown when printing
    |           the equation
    |
    |  Class Attributes:
    |      latex_renderer: If not None, a callable that must return a LaTeX
    |          representation (:class:`str`) of `lhs` and `rhs`.
    |
    |  Methods defined here:
    |
    |  __add__(self, other)
    |      Add another equation, or a constant.
    |
    |  __eq__(self, other)
    |      Compare to another equation, or a constant.
    |
    |      This does not take into account any mathematical knowledge, it merely
    |      checks if the :attr:`lhs` and :attr:`rhs` are exactly equal. If
    |      comparing against a constant, the :attr:`rhs` must be exactly equal to
    |      that constant.
    |
    |  __init__(self, lhs, rhs=None, tag=None, _prev_lhs=None, _prev_rhs=None, _prev_tags=None)
    |      Initialize self.  See help(type(self)) for accurate signature.
    |
    |  __mul__(self, other)
    |
    |  __radd__ = __add__(self, other)
    |
    |  __repr__(self)
    |      Return repr(self).
    |
    |  __rmul__(self, other)
    |
    |  __rsub__(self, other)
    |
    |  __str__(self)
    |      Return str(self).
    |
    |  __sub__(self, other)
    |
    |  __truediv__(self, other)
    |
    |  apply(self, func, *args, cont=False, tag=None, **kwargs)
    |      Apply `func` to both sides of the equation.
    |
    |      Returns a new equation where the left-hand-side and right-hand side
    |      are replaced by the application of `func`::
    |
    |          lhs=func(lhs, *args, **kwargs)
    |          rhs=func(rhs, *args, **kwargs)
    |
    |      If ``cont=True``, the resulting equation will keep a history of its
    |      previous state (resulting in multiple lines of equations when printed).
    |
    |      The resulting equation with have the given `tag`.
    |
    |  apply_mtd(self, mtd, *args, cont=False, tag=None, **kwargs)
    |      Call the method `mtd` on both sides of the equation.
    |
    |      That is, the left-hand-side and right-hand-side are replaced by::
    |
    |          lhs=lhs.<mtd>(*args, **kwargs)
    |          rhs=rhs.<mtd>(*args, **kwargs)
    |
    |      The `cont` and `tag` parameters are as in :meth:`apply`.
    |
    |  apply_mtd_to_lhs(self, mtd, *args, cont=False, tag=None, **kwargs)
    |      Call the method `mtd` on the :attr:`lhs` of the equation only.
    |
    |      Like :meth:`apply_mtd`, but modifying only the left-hand-side.
    |
    |  apply_mtd_to_rhs(self, mtd, *args, cont=False, tag=None, **kwargs)
    |      Call the method `mtd` on the :attr:`rhs` of the equation.
    |
    |      Like :meth:`apply_mtd`, but modifying only the right-hand-side.
    |
    |  apply_to_lhs(self, func, *args, cont=False, tag=None, **kwargs)
    |      Apply `func` to the :attr:`lhs` of the equation only.
    |
    |      Like :meth:`apply`, but modifying only the left-hand-side.
    |
    |  apply_to_rhs(self, func, *args, cont=False, tag=None, **kwargs)
    |      Apply `func` to the :attr:`rhs` of the equation only.
    |
    |      Like :meth:`apply`, but modifying only the right-hand-side.
    |
    |  copy(self)
    |      Return a copy of the equation
    |
    |  set_tag(self, tag)
    |      Return a copy of the equation with a new `tag`.
    |
    |  ----------------------------------------------------------------------
    |  Data descriptors defined here:
    |
    |  __dict__
    |      dictionary for instance variables (if defined)
    |
    |  __weakref__
    |      list of weak references to the object (if defined)
    |
    |  as_dict
    |      Mapping of the lhs to the rhs.
    |
    |      This allows to plug an equation into another expression.
    |
    |  lhs
    |      The left-hand-side of the equation.
    |
    |  rhs
    |      The right-hand-side of the equation.
    |
    |  tag
    |      A tag (equation number) to be shown when printing the equation, or
    |      None
    |
    |  ----------------------------------------------------------------------
    |  Data and other attributes defined here:
    |
    |  __hash__ = None
    |
    |  latex_renderer = None
   <BLANKLINE>



Use in the Jupyter notebook
---------------------------

In a `Jupyter notebook`_, equations will be rendered in LaTeX.
See `examples.ipynb`_.

The rendering presumes that both the ``lhs`` and the ``rhs`` have a LaTeX
representation. If the ``Eq`` class has a ``latex_renderer`` attribute defined,
that renderer will be used to obtain the LaTeX representation of the ``lhs``
and ``rhs``. Otherwise:

* If the ``lhs`` or ``rhs`` object has a ``_latex`` method, that method will be
  called; or lastly,
* The ``lhs`` and ``rhs`` will be passed to ``sympy.latex``.


Relation to SymPy's Eq class
----------------------------

The SymPy package also provides an `Eq class`_ that represents equality between
two SymPy expressions. The class provided by SymPy and the class provided by
this package are not interchangeable: SymPy's ``Eq`` does not track
modifications or print out as multiline equations. While the
``symbolic_equation.Eq`` class is not a SymPy expression, it can be converted
to a ``sympy.Eq`` instance via the ``sympy.sympify`` function.

.. _examples.ipynb: https://nbviewer.jupyter.org/github/goerz/symbolic_equation/blob/master/examples.ipynb
.. _Github: https://github.com/goerz/symbolic_equation
.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Python Packaging User Guide: https://packaging.python.org/tutorials/installing-packages/
.. _Eq class: https://docs.sympy.org/latest/modules/core.html?highlight=eq#sympy.core.relational.Equality
.. _SymPy: https://www.sympy.org/
.. _Jupyter notebook: https://jupyter.org
