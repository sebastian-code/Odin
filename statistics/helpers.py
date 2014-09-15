from __future__ import division


def division_or_zero(dividend, numerator):
    try:
        result = dividend / numerator
    except ZeroDivisionError:
        result = 0
    return result
