"""Package providing the :class:`Eq` class for symbolic equations."""
from uniseg.graphemecluster import grapheme_clusters


__version__ = '0.2.0'


__all__ = ['Eq']


def _grapheme_len(text):
    """Number of graphemes in `text`

    This is the length of the `text` when printed::
        >>> s = 'Â'
        >>> len(s)
        2
        >>> _grapheme_len(s)
        1
    """
    return len(list(grapheme_clusters(text)))


def _ljust(text, width, fillchar=' '):
    """Left-justify text to a total of `width`

    The `width` is based on graphemes::

        >>> s = 'Â'
        >>> s.ljust(2)
        'Â'
        >>> _ljust(s, 2)
        'Â '
    """
    len_text = _grapheme_len(text)
    return text + fillchar * (width - len_text)


def _rjust(text, width, fillchar=' '):
    """Right-justify text for a total of `width` graphemes

    The `width` is based on graphemes::

        >>> s = 'Â'
        >>> s.rjust(2)
        'Â'
        >>> _rjust(s, 2)
        ' Â'
    """
    len_text = _grapheme_len(text)
    return fillchar * (width - len_text) + text


class Eq:
    """Symbolic equation.

    This class keeps track of the :attr:`lhs` and :attr:`rhs` of an equation
    across arbitrary manipulations.

    Args:
        lhs: the left-hand-side of the equation
        rhs: the right-hand-side of the equation. If None, defaults to zero.
        tag: a tag (equation number) to be shown when printing
             the equation

    Class Attributes:
        latex_renderer: If not None, a callable that must return a LaTeX
            representation (:class:`str`) of `lhs` and `rhs`.
    """

    latex_renderer = None

    def __init__(
        self,
        lhs,
        rhs=None,
        tag=None,
        _prev_lhs=None,
        _prev_rhs=None,
        _prev_tags=None,
    ):
        if rhs is None:
            try:
                import sympy

                rhs = sympy.sympify(0)
            except ImportError:
                rhs = 0
        self._lhs = lhs
        self._prev_lhs = _prev_lhs or []
        self._prev_rhs = _prev_rhs or []
        self._prev_tags = _prev_tags or []
        self._rhs = rhs
        try:
            self._tag = int(tag)
        except (ValueError, TypeError):
            self._tag = tag

    @property
    def lhs(self):
        """The left-hand-side of the equation."""
        lhs = self._lhs
        i = 0
        while lhs is None:
            i -= 1
            lhs = self._prev_lhs[i]
        return lhs

    @property
    def rhs(self):
        """The right-hand-side of the equation."""
        return self._rhs

    def tag(self, tag):
        """Set the tag for the last line in the equation."""
        return Eq(
            self._lhs,
            self._rhs,
            tag=tag,
            _prev_lhs=self._prev_lhs,
            _prev_rhs=self._prev_rhs,
            _prev_tags=self._prev_tags,
        )

    @property
    def as_dict(self):
        """Mapping of the lhs to the rhs.

        This allows to plug an equation into another expression.
        """
        return {self.lhs: self.rhs}

    def apply(self, func_or_mtd, *args, **kwargs):
        """Apply `func_or_mtd` to both sides of the equation.

        Returns a new equation where the left-hand-side and right-hand side
        are replaced by the application of `func_or_mtd`, depending on its
        type.

        * If `func_or_mtd` is a string, it must be the name of a method `mtd`,
          and equation is modified as

          ::

              lhs=lhs.mtd(*args, **kwargs)
              rhs=rhs.mtd(*args, **kwargs)

        * If `func_or_mtd` is a callable `func`, the equation is modified as

          ::

              lhs=func(lhs, *args, **kwargs)
              rhs=func(rhs, *args, **kwargs)
        """
        if isinstance(func_or_mtd, str):
            new_lhs = getattr(self.lhs, func_or_mtd)(*args, **kwargs)
            new_rhs = getattr(self.rhs, func_or_mtd)(*args, **kwargs)
        else:
            new_lhs = func_or_mtd(self.lhs, *args, **kwargs)
            new_rhs = func_or_mtd(self.rhs, *args, **kwargs)
        if new_lhs == self.lhs:
            new_lhs = None
        return self._append(new_lhs, new_rhs)

    def transform(self, func, *args, **kwargs):
        """Apply `func` to the entire equation.

        The lhs and the rhs of the equation is replaced with the lhs and rhs of
        the equation returned by ``func(self, *args, **kwargs)``.
        """
        new_eq = func(self, *args, **kwargs)
        new_lhs = new_eq.lhs
        new_rhs = new_eq.rhs
        if new_lhs == self.lhs:
            new_lhs = None
        return self._append(new_lhs, new_rhs)

    def apply_to_lhs(self, func_or_mtd, *args, **kwargs):
        """Apply `func_or_mtd` to the :attr:`lhs` of the equation only.

        Like :meth:`apply`, but modifying only the left-hand-side.
        """
        if isinstance(func_or_mtd, str):
            new_lhs = getattr(self.lhs, func_or_mtd)(*args, **kwargs)
        else:
            new_lhs = func_or_mtd(self.lhs, *args, **kwargs)
        return self._append(new_lhs, self.rhs)

    def apply_to_rhs(self, func_or_mtd, *args, **kwargs):
        """Apply `func_or_mtd` to the :attr:`rhs` of the equation only.

        Like :meth:`apply`, but modifying only the right-hand-side.
        """
        new_lhs = None
        if isinstance(func_or_mtd, str):
            new_rhs = getattr(self.rhs, func_or_mtd)(*args, **kwargs)
        else:
            new_rhs = func_or_mtd(self.rhs, *args, **kwargs)
        return self._append(new_lhs, new_rhs)

    def _append(self, new_lhs, new_rhs):
        new_prev_lhs = self._prev_lhs.copy()
        new_prev_lhs.append(self._lhs)
        new_prev_rhs = self._prev_rhs.copy()
        new_prev_rhs.append(self.rhs)
        new_prev_tags = self._prev_tags.copy()
        new_prev_tags.append(self._tag)
        return Eq(
            new_lhs,
            new_rhs,
            _prev_lhs=new_prev_lhs,
            _prev_rhs=new_prev_rhs,
            _prev_tags=new_prev_tags,
        )

    def amend(self, previous_lines=1):
        """Amend the previous lhs and rhs with the current ones.

        If `previous_lines` is greater than 1, overwrite the corresponding
        number of previous lines.

        This can be chained to e.g. an :meth:`apply` call to group multiple
        steps so that they don't show up a separate lines in the output.
        """
        if previous_lines <= 0:
            raise ValueError(
                "Invalid previous_lines=%r, must be >= 1" % previous_lines
            )
        new_prev_lhs = self._prev_lhs.copy()[:-previous_lines]
        new_prev_rhs = self._prev_rhs.copy()[:-previous_lines]
        new_prev_tags = self._prev_tags.copy()[:-previous_lines]
        return Eq(
            self._lhs,
            self.rhs,
            tag=self._tag,
            _prev_lhs=new_prev_lhs,
            _prev_rhs=new_prev_rhs,
            _prev_tags=new_prev_tags,
        )

    def reset(self):
        """Discard the equation history."""
        return Eq(self.lhs, self.rhs, tag=self._tag)

    def copy(self):
        """Return a copy of the equation, including its history."""
        return Eq(
            self._lhs,
            self._rhs,
            tag=self._tag,
            _prev_lhs=self._prev_lhs,
            _prev_rhs=self._prev_rhs,
            _prev_tags=self._prev_tags,
        )

    def __add__(self, other):
        """Add another equation, or a constant."""
        try:
            return Eq(lhs=(self.lhs + other.lhs), rhs=(self.rhs + other.rhs))
        except AttributeError:
            return Eq(lhs=(self.lhs + other), rhs=(self.rhs + other))

    __radd__ = __add__

    def __sub__(self, other):
        try:
            return Eq(lhs=(self.lhs - other.lhs), rhs=(self.rhs - other.rhs))
        except AttributeError:
            return Eq(lhs=(self.lhs - other), rhs=(self.rhs - other))

    def __rsub__(self, other):
        # we don't have to consier the case of `other` being an `Eq`, because
        # that would be handled by `__sub__`.
        return Eq(lhs=(other - self.lhs), rhs=(other - self.rhs))

    def __mul__(self, other):
        return Eq(lhs=(self.lhs * other), rhs=(self.rhs * other))

    def __rmul__(self, other):
        return Eq(lhs=(other * self.lhs), rhs=(other * self.rhs))

    def __truediv__(self, other):
        return Eq(lhs=(self.lhs / other), rhs=(self.rhs / other))

    def __eq__(self, other):
        """Compare to another equation, or a constant.

        This does not take into account any mathematical knowledge, it merely
        checks if the :attr:`lhs` and :attr:`rhs` are exactly equal. If
        comparing against a constant, the :attr:`rhs` must be exactly equal to
        that constant.
        """
        try:
            return self.lhs == other.lhs and self.rhs == other.rhs
        except AttributeError:
            return self.rhs == other

    def _render_str(self, renderer, *args, **kwargs):
        rendered_lhs = []
        rendered_rhs = []
        rendered_tags = []

        for i, rhs in enumerate(self._prev_rhs):
            lhs = self._prev_lhs[i]
            tag = self._prev_tags[i]
            if lhs is None:
                rendered_lhs.append('')
            else:
                rendered_lhs.append(renderer(lhs, *args, **kwargs))
            rendered_rhs.append(renderer(rhs, *args, **kwargs))
            if tag is None:
                rendered_tags.append('')
            else:
                rendered_tags.append(renderer(tag, *args, **kwargs))
        if self._lhs is None:
            rendered_lhs.append('')
        else:
            rendered_lhs.append(renderer(self._lhs, *args, **kwargs))
        rendered_rhs.append(renderer(self._rhs, *args, **kwargs))
        if self._tag is None:
            rendered_tags.append('')
        else:
            rendered_tags.append(renderer(self._tag, *args, **kwargs))
        len_lhs = max([_grapheme_len(s) for s in rendered_lhs])
        len_rhs = max([_grapheme_len(s) for s in rendered_rhs])
        len_tag = max([_grapheme_len(s) for s in rendered_tags]) + 2

        lines = []
        for (lhs, rhs, tag) in zip(rendered_lhs, rendered_rhs, rendered_tags):
            if len(tag) > 0:
                tag = "(" + tag + ")"
            lhs = _rjust(lhs, len_lhs)
            rhs = _ljust(rhs, len_rhs)
            tag = _ljust(tag, len_tag)
            lines.append((lhs + ' = ' + rhs + "    " + tag).rstrip())
        return "\n".join(lines)

    def __str__(self):
        return self._render_str(renderer=str)

    def __repr__(self):
        return self._render_str(renderer=repr)

    def _latex_render_expr(self, expr):
        if self.latex_renderer is not None:
            return self.latex_renderer(expr)
        else:
            try:
                return expr._latex()
            except AttributeError:
                try:
                    import sympy

                    return sympy.latex(expr)
                except ImportError:
                    raise ValueError("No latex_renderer available")

    def _repr_latex_(self):
        """LaTeX representation for Jupyter notebook."""
        has_history = len(self._prev_rhs) > 0
        if has_history:
            res = r'\begin{align}' + "\n"
            res += "  %s &= %s" % (
                self._latex_render_expr(self._prev_lhs[0]),
                self._latex_render_expr(self._prev_rhs[0]),
            )
            if self._prev_tags[0] is not None:
                res += r'\tag{%s}' % self._prev_tags[0]
            res += "\\\\\n"
            for i, rhs in enumerate(self._prev_rhs[1:]):
                lhs = self._prev_lhs[i + 1]
                if lhs is None:
                    res += "   &= %s" % self._latex_render_expr(rhs)
                else:
                    res += "  %s &= %s" % (
                        self._latex_render_expr(lhs),
                        self._latex_render_expr(rhs),
                    )
                if self._prev_tags[i + 1] is not None:
                    res += r'\tag{%s}' % self._prev_tags[i + 1]
                res += "\\\\\n"
            lhs = self._lhs
            if lhs is None:
                res += "   &= %s\n" % self._latex_render_expr(self.rhs)
            else:
                res += "  %s &= %s\n" % (
                    self._latex_render_expr(lhs),
                    self._latex_render_expr(self.rhs),
                )
            if self._tag is not None:
                res += r'\tag{%s}' % self._tag
            res += r'\end{align}' + "\n"
        else:
            res = r'\begin{equation}' + "\n"
            res += "  %s = %s\n" % (
                self._latex_render_expr(self.lhs),
                self._latex_render_expr(self.rhs),
            )
            try:
                if self._tag is not None:
                    res += r'\tag{%s}' % self._tag
            except AttributeError:
                pass
            res += r'\end{equation}' + "\n"
        return res

    def _sympy_(self):
        """Convert to a :class:`sympy.Eq`."""
        from sympy import Eq as SympyEq

        return SympyEq(self.lhs, self.rhs)
