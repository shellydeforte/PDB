# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

from sys import version_info

PYTHON2 = version_info[0] == 2


def create_delimiter(delimiter):
    """Return pandas delimiter based on Python version.

    With Python 2, pandas expects a string (not Unicode) delimiter
    and throws and error when passing a string with
    from __future__ import unicode_literal. Therefore the
    Unicode must be encoded before passing to pandas.

    With Python 3, pandas extracts a string (which is
    Unicode in version 3) and complains
    (TypeError: "delimiter" must be string, not unicode) if
    the delimiter has been encoded—as we must do when using
    pandas with unicode_literal in Python 2.

    Pandas issue #6035.

    """
    if PYTHON2:
        # Module should use __future__.unicode_literals
        assert isinstance(delimiter, unicode)
        delimiter = delimiter.encode('utf-8')
        assert isinstance(delimiter, str)
    else:
        assert isinstance(delimiter, str)
    return delimiter