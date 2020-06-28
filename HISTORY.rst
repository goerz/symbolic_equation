=======
History
=======

0.2.0 (2020-06-28)
------------------

* Removed: ``apply_mtd``, ``apply_mtd_to_lhs``, ``apply_mtd_to_rhs`` methods. The functionality is now included in ``apply``, ``apply_to_lhs``, ``apply_to_rhs``, which can now receive a function or a method name
* Added: ``amend`` and ``reset`` methods for controlling which lines are included in the history of an equation ("grouping")
* Changed: The ``set_tag`` method was renamed to ``tag``
* Removed: ``cont`` and ``tag`` arguments. The ``cont`` behavior (preserving the equation history) is now on by default, and the old ``cont=False`` can be achieved with ``reset``.
* Removed: ``tag`` property (``tag`` is now a method for setting the equation tag).
* Added: ``transform`` method for transforming the equation as a whole.

0.1.0-dev (2019-05-26)
----------------------

* Initial release
