Installation
============

Requirements
------------

CoBrA requires Python 3.7 or later and the following dependencies:

* numpy
* matplotlib
* seaborn
* networkx
* scikit-learn

Installing from PyPI
-------------------

The easiest way to install CoBrA is using pip:

.. code-block:: bash

   pip install cobra-brain

Installing from Source
--------------------

You can also install CoBrA directly from the GitHub repository:

.. code-block:: bash

   git clone https://github.com/siddlokray/cobra.git
   cd cobra
   pip install -e .

Development Installation
----------------------

If you want to contribute to CoBrA, install it in development mode:

.. code-block:: bash

   git clone https://github.com/siddlokray/cobra.git
   cd cobra
   pip install -e ".[dev]"

This will install CoBrA along with additional development dependencies.