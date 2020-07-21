# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %matplotlib inline

# # A tutorial
#
# This is a Jupyter notebook.

import numpy as np
import matplotlib.pyplot as plt

# ## Plotting
#
# It has a plot:

x = np.linspace(0, 10, 5000)
plt.plot(x, np.sin(x))
plt.xlabel("x")
plt.ylabel("y");


