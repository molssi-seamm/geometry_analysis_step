# -*- coding: utf-8 -*-
"""
Control parameters for the Geometry Analysis step in a SEAMM flowchart
"""

import logging
import seamm
import pprint  # noqa: F401

logger = logging.getLogger(__name__)


class GeometryAnalysisParameters(seamm.Parameters):
    """
    The control parameters for Geometry Analysis.

    You need to replace the "time" entry in dictionary below these comments with the
    definitions of parameters to control this step. The keys are parameters for the
    current plugin,the values are dictionaries as outlined below.

    Examples
    --------
    ::

        parameters = {
            "time": {
                "default": 100.0,
                "kind": "float",
                "default_units": "ps",
                "enumeration": tuple(),
                "format_string": ".1f",
                "description": "Simulation time:",
                "help_text": ("The time to simulate in the dynamics run.")
            },
        }

    parameters : {str: {str: str}}
        A dictionary containing the parameters for the current step.
        Each key of the dictionary is a dictionary that contains the
        the following keys:

    parameters["default"] :
        The default value of the parameter, used to reset it.

    parameters["kind"] : enum()
        Specifies the kind of a variable. One of  "integer", "float", "string",
        "boolean", or "enum"

        While the "kind" of a variable might be a numeric value, it may still have
        enumerated custom values meaningful to the user. For instance, if the parameter
        is a convergence criterion for an optimizer, custom values like "normal",
        "precise", etc, might be adequate. In addition, any parameter can be set to a
        variable of expression, indicated by having "$" as the first character in the
        field. For example, $OPTIMIZER_CONV.

    parameters["default_units"] : str
        The default units, used for resetting the value.

    parameters["enumeration"]: tuple
        A tuple of enumerated values.

    parameters["format_string"]: str
        A format string for "pretty" output.

    parameters["description"]: str
        A short string used as a prompt in the GUI.

    parameters["help_text"]: str
        A longer string to display as help for the user.

    See Also
    --------
    GeometryAnalysis, TkGeometryAnalysis, GeometryAnalysis,
    GeometryAnalysisParameters, Geometry AnalysisStep
    """

    parameters = {
        "target": {
            "default": "all",
            "kind": "enum",
            "enumeration": (
                "all",
                "bonds",
                "angles",
                "dihedrals",
                "bonds and angles",
                "specified terms",
            ),
            "format_string": "",
            "description": "Target:",
            "help_text": "What geometric parameters to calculate.",
        },
        "specification": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "Bonds, angles,...:",
            "help_text": (
                "A string listing of bonds, angle, torsions, and out of planes "
                "separated by commas and/or blanks. The atoms are numbered from 1."
            ),
        },
        "table output": {
            "default": "none",
            "kind": "enum",
            "enumeration": (
                "none",
                "to a single table",
                "each term to separate tables",
            ),
            "format_string": "",
            "description": "Table output:",
            "help_text": "Whether and how to output to tables.",
        },
        "id column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("Molecule ID",),
            "format_string": "",
            "description": "id column:",
            "help_text": "Column to id the molecule.",
        },
        "ids": {
            "default": "<system.name>",
            "kind": "string",
            "default_units": "",
            "enumeration": (
                "<system.name>",
                "<configuration.name>",
            ),
            "format_string": "",
            "description": "Molecule id:",
            "help_text": "The name to use as molecule id.",
        },
        "only first id": {
            "default": "yes",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("yes", "no"),
            "format_string": "",
            "description": "First id, then blanks:",
            "help_text": "Whether to put just the first id followed by empty cells.",
        },
        "term type column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("Type of term",),
            "format_string": "",
            "description": "Type of term",
            "help_text": "The type of term: bond, angle, dihedral, oop.",
        },
        "indx1 column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("Indx1",),
            "format_string": "",
            "description": "Atom1 index",
            "help_text": "The column for the first atom index.",
        },
        "indx2 column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("Indx2",),
            "format_string": "",
            "description": "Atom2 index",
            "help_text": "The column for the second atom index.",
        },
        "indx3 column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("Indx3",),
            "format_string": "",
            "description": "Atom3 index",
            "help_text": "The column for the third atom index.",
        },
        "indx4 column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("Indx4",),
            "format_string": "",
            "description": "Atom4 index",
            "help_text": "The column for the fourth atom index.",
        },
        "el1 column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("El1",),
            "format_string": "",
            "description": "Atom1 element",
            "help_text": "The column for the first atom symbol.",
        },
        "el2 column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("El2",),
            "format_string": "",
            "description": "Atom2 element",
            "help_text": "The column for the second atom symbol.",
        },
        "el3 column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("El3",),
            "format_string": "",
            "description": "Atom3 element",
            "help_text": "The column for the third atom symbol.",
        },
        "el4 column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("El4",),
            "format_string": "",
            "description": "",
            "help_text": "The column for the fourth atom symbol.",
        },
        "atom indices column": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": ("atom indices)",),
            "format_string": "",
            "description": "Term using indices",
            "help_text": "The column for the atom indices, e.g. 1-3.",
        },
        "term column": {
            "default": "Term",
            "kind": "string",
            "default_units": "",
            "enumeration": ("Term",),
            "format_string": "",
            "description": "Term using elements",
            "help_text": "The column for the term using elements, e.g. C-H.",
        },
        "value column": {
            "default": "Value (Å or º)",
            "kind": "string",
            "default_units": "",
            "enumeration": ("Value (Å or º)",),
            "format_string": "",
            "description": "Value of term",
            "help_text": "The column for the value of the term.",
        },
        "table": {
            "default": "valence terms",
            "kind": "string",
            "default_units": "",
            "enumeration": ("valence terms",),
            "format_string": "",
            "description": "Table:",
            "help_text": "The table to output valence terms.",
        },
        "bond table": {
            "default": "bonds",
            "kind": "string",
            "default_units": "",
            "enumeration": ("bonds",),
            "format_string": "",
            "description": "Bond table:",
            "help_text": "The table to output bonds.",
        },
        "angle table": {
            "default": "angles",
            "kind": "string",
            "default_units": "",
            "enumeration": ("angles",),
            "format_string": "",
            "description": "Angle table:",
            "help_text": "The table to output angles.",
        },
        "dihedral table": {
            "default": "dihedrals",
            "kind": "string",
            "default_units": "",
            "enumeration": ("dihedrals",),
            "format_string": "",
            "description": "Dihedral table:",
            "help_text": "The table to output dihedrals.",
        },
        "out-of-plane table": {
            "default": "out-of-planes",
            "kind": "string",
            "default_units": "",
            "enumeration": ("out-of-planes",),
            "format_string": "",
            "description": "Out-Of-Plane table:",
            "help_text": "The table to output out-of-planes.",
        },
        # Results handling ... uncomment if needed
        "results": {
            "default": {},
            "kind": "dictionary",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "results",
            "help_text": "The results to save to variables or in tables.",
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the parameters, by default with the parameters defined above

        Parameters
        ----------
        defaults: dict
            A dictionary of parameters to initialize. The parameters
            above are used first and any given will override/add to them.
        data: dict
            A dictionary of keys and a subdictionary with value and units
            for updating the current, default values.

        Returns
        -------
        None
        """

        logger.debug("GeometryAnalysisParameters.__init__")

        super().__init__(
            defaults={**GeometryAnalysisParameters.parameters, **defaults}, data=data
        )
