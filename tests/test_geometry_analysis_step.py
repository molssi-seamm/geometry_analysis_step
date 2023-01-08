#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `geometry_analysis_step` package."""

import pytest  # noqa: F401
import geometry_analysis_step  # noqa: F401


def test_construction():
    """Just create an object and test its type."""
    result = geometry_analysis_step.GeometryAnalysis()
    assert (
        str(type(result))
        == "<class 'geometry_analysis_step.geometry_analysis.GeometryAnalysis'>"
    )
