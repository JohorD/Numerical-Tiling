# modules_py/styles_format.py

import warnings
from matplotlib import MatplotlibDeprecationWarning, rc
import matplotlib.pyplot as plt
import numpy as np

"""
Module for configuring the general style of figures and
formatting numbers in LaTeX scientific notation.
"""

# ------------------------------------------------------------
# Ignore deprecation warnings and other common warnings
# ------------------------------------------------------------

warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def configure_style():
    """
    Set the GENERAL style of Matplotlib
    """

    # Reset style
    plt.style.use('default')

    # Computer Modern + LaTeX
    rc('font', **{
        'size': 15,
        'family': 'serif',
        'serif': ['Computer Modern Roman']
    })
    rc('text', usetex=True)


def sci_notation(num, decimal_digits=2):
    """
    Converts a number into a string in LaTeX-style scientific notation.
    Example: 0.000123 -> "1.23 \\times 10^{-4}"
    """
    mantissa, exp = f"{num:.{decimal_digits}e}".split("e")
    exp = int(exp)
    return f"{mantissa} \\times 10^{{{exp}}}"

