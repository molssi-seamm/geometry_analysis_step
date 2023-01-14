===============================
SEAMM Geometry Analysis Plug-in
===============================

.. image:: https://img.shields.io/github/issues-pr-raw/molssi-seamm/geometry_analysis_step
   :target: https://github.com/molssi-seamm/geometry_analysis_step/pulls
   :alt: GitHub pull requests

.. image:: https://github.com/molssi-seamm/geometry_analysis_step/workflows/CI/badge.svg
   :target: https://github.com/molssi-seamm/geometry_analysis_step/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/molssi-seamm/geometry_analysis_step/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/molssi-seamm/geometry_analysis_step
   :alt: Code Coverage

.. image:: https://github.com/molssi-seamm/quickmin_step/workflows/CodeQL/badge.svg
   :target: https://github.com/molssi-seamm/quickmin_step/security/code-scanning
   :alt: Code Quality

.. image:: https://github.com/molssi-seamm/geometry_analysis_step/workflows/Documentation/badge.svg
   :target: https://molssi-seamm.github.io/geometry_analysis_step/index.html
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/geometry_analysis_step.svg
   :target: https://pypi.python.org/pypi/geometry_analysis_step
   :alt: PyPi VERSION

A SEAMM plug-in for analysis of the geometry of particularly small molecules

* Free software: BSD-3-Clause
* Documentation: https://molssi-seamm.github.io/geometry_analysis_step/index.html
* Code: https://github.com/molssi-seamm/geometry_analysis_step

Features
--------

The Geometric Analysis plug-in provides the following functionality:

   #. Generating lists of all valence terms -- bonds, angles, dihedrals, and
      out-of-planes -- plus their value for the current structure. This functionality
      relies on the description of the bonds in the structure.
   #. Creating lists of terms and their values as specified in the input. Note that in
      this case the atoms do not need to be connected by bonds in the structure.
   #. Printing the tables of results to the output.
   #. Outputing the data to one or more tables.
   #. Storing the data in the internal SEAMM database.

Acknowledgements
----------------

This package was created with the `molssi-seamm/cookiecutter-seamm-plugin`_ tool, which
is based on the excellent Cookiecutter_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`molssi-seamm/cookiecutter-seamm-plugin`: https://github.com/molssi-seamm/cookiecutter-seamm-plugin

Developed by the Molecular Sciences Software Institute (MolSSI_),
which receives funding from the `National Science Foundation`_ under
award CHE-2136142.

.. _MolSSI: https://molssi.org
.. _`National Science Foundation`: https://www.nsf.gov
