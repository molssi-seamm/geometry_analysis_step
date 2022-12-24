# -*- coding: utf-8 -*-

"""
geometry_analysis_step
A SEAMM plug-in for analysis of the geometry of particularly small molecules
"""

# Bring up the classes so that they appear to be directly in
# the geometry_analysis_step package.

from .geometry_analysis import GeometryAnalysis  # noqa: F401, E501
from .geometry_analysis_parameters import GeometryAnalysisParameters  # noqa: F401, E501
from .geometry_analysis_step import GeometryAnalysisStep  # noqa: F401, E501
from .tk_geometry_analysis import TkGeometryAnalysis  # noqa: F401, E501

from .metadata import metadata  # noqa: F401

# Handle versioneer
from ._version import get_versions

__author__ = "Paul Saxe"
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
