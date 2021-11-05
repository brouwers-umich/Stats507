# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import random

# **Stan Brouwers** *brouwers@umich.edu*

# # Pandas, write to LaTeX
#
# - Pandas function.
# - Can write dataframe to LaTeX table.
# - Helpful when writing reports.
# - Easy to call.
#

# # A first example
#
# - Multiple ways to call the function.
# - Selecting certain parts of a dataframe also possible.
# - Column names and indices are used to label rows and columns.

# Generate some data.
data = pd.DataFrame([[random.randint(1,10) for columns in range(5)] for rows in range(5)])
print(data.to_latex())

# # Another example
#
# - Table can be written to a file. (buf input)
# - Subset of columns can be chosen.
#     - Using list of column names.

data.to_latex(buf='./test.doc')
# Only printing certain columns
print(data.to_latex(columns=[0, 4]))
