# -*- coding: utf-8 -*-
"""Write a progress bar to sys.stdout."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

from sys import stdout


class ProgressBar(object):
    """Write a progress bar to sys.stdout.

    Instantiate ProgressBar with the expected total number of
    iterations and then call the inc() method at the end of
    each iteration.

    Example:
        data = [i for i in range(100)]
        report_progress = ProgressBar(len(data))
        for something in data:
            # Do processing.
            report_progress.inc()

    """
    def __init__(
            self, total, approx_percentage=10, start_msg=None, end_msg=None
    ):
        """Initialize with a total size and the
        reporting interval as a percentage.

        Args:
            total (int): The total number of iterations expected.
            approx_percentage (int): The approximate intervals, as a
                percent, for updating the progress bar. The default
                is ten percent.
            start_msg (Unicode): An optional message to write when starting.
            end_msg (Unicode): An optional message to write when complete.

        """
        self._start_msg = start_msg
        self._end_msg = end_msg
        if total < 1:
            raise ValueError(
                "The total number of items to count should be"
                "greater than 1."
            )
        self._total = int(total)

        if 0 < approx_percentage < 50:
            real_percentage = round(
                approx_percentage / 100.0 * self._total
            )
        else:
            print("Bad value given for report_on_percentage. "
                  "Defaulting to 10%.")
            real_percentage = round(self._total * .10)

        if real_percentage == 0:
            real_percentage = 1

        self._report_on_intervals = {
            i
            for i in range(1, self._total + 1)
            if i % real_percentage == 0
            }
        self._indicator_length = len(self._report_on_intervals)
        self._current_count = float(1)
        self._completed = 0
        self._remaining = len(self._report_on_intervals)
        self._status_bar = (
            "Percent: [{}] 0%".format(
                "-" * self._indicator_length,
                )
        )

    def _write(self):
        """Write the status bar to standard out."""
        stdout.write(self._status_bar)
        stdout.flush()
        if self._remaining == 0:
            print("")
            if self._end_msg:
                print(self._end_msg)
        return None

    def _report(self):
        """Update the status bar and then _write()."""
        self._completed += 1
        self._remaining = self._indicator_length - self._completed
        indicator = (
            "{}{}".format("#" * self._completed, "-" * self._remaining)
        )
        numerical_complete = int(float(self._current_count / self._total) * 100)
        self._status_bar = (
            "\rPercent: [{}] {}%".format(
                indicator,
                numerical_complete
            )
        )
        self._write()
        return None

    def inc(self):
        """Increment the count by 1 and automatically update the status
        bar if the count is in the given reporting interval."""
        if self._current_count == 1:
            if self._start_msg:
                print(self._start_msg)
            # Write progress bar for the first time.
            self._write()

        if self._current_count in self._report_on_intervals:
            self._report()
        self._current_count += 1

        return None
