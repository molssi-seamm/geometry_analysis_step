"""This file contains metadata describing the results from GeometryAnalysis"""

metadata = {}

"""Properties that GeometryAnalysis produces.
`metadata["results"]` describes the results that this step can produce. It is a
dictionary where the keys are the internal names of the results within this step, and
the values are a dictionary describing the result. For example::

    metadata["results"] = {
        "total_energy": {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The total energy",
            "dimensionality": "scalar",
            "methods": [
                "ccsd",
                "ccsd(t)",
                "dft",
                "hf",
            ],
            "property": "total energy#GeometryAnalysis#{model}",
            "type": "float",
            "units": "E_h",
        },
    }

Fields
______

calculation : [str]
    Optional metadata describing what subtype of the step produces this result.
    The subtypes are completely arbitrary, but often they are types of calculations
    which is why this is name `calculation`. To use this, the step or a substep
    define `self._calculation` as a value. That value is used to select only the
    results with that value in this field.

description : str
    A human-readable description of the result.

dimensionality : str
    The dimensions of the data. The value can be "scalar" or an array definition
    of the form "[dim1, dim2,...]". Symmetric tringular matrices are denoted
    "triangular[n,n]". The dimensions can be integers, other scalar
    results, or standard parameters such as `n_atoms`. For example, '[3]',
    [3, n_atoms], or "triangular[n_aos, n_aos]".

methods : str
    Optional metadata like the `calculation` data. `methods` provides a second
    level of filtering, often used for the Hamiltionian for *ab initio* calculations
    where some properties may or may not be calculated depending on the type of
    theory.

property : str
    An optional definition of the property for storing this result. Must be one of
    the standard properties defined either in SEAMM or in this steps property
    metadata in `data/properties.csv`.

type : str
    The type of the data: string, integer, or float.

units : str
    Optional units for the result. If present, the value should be in these units.
"""
metadata["results"] = {
    "bond_lengths": {
        "description": "The bond lengths",
        "dimensionality": "[n_bonds]",
        "type": "float",
        "units": "Å",
    },
    "bond_orders": {
        "description": "The bond orders",
        "dimensionality": "[n_bonds]",
        "type": "float",
        "units": "",
    },
    "bond_index_i": {
        "description": "The bond index i",
        "dimensionality": "[n_bonds]",
        "type": "integer",
        "units": "",
    },
    "bond_index_j": {
        "description": "The bond index j",
        "dimensionality": "[n_bonds]",
        "type": "integer",
        "units": "",
    },
    "angles": {
        "description": "The angles",
        "dimensionality": "[n_angles]",
        "type": "float",
        "units": "degree",
    },
    "angle_bond_orders_ij": {
        "description": "The bond orders of i, j",
        "dimensionality": "[n_angles]",
        "type": "float",
        "units": "",
    },
    "angle_bond_orders_jk": {
        "description": "The bond orders of j, k",
        "dimensionality": "[n_angles]",
        "type": "float",
        "units": "",
    },
    "angle_index_i": {
        "description": "The angle index i",
        "dimensionality": "[n_angles]",
        "type": "integer",
        "units": "",
    },
    "angle_index_j": {
        "description": "The angle index j",
        "dimensionality": "[n_angles]",
        "type": "integer",
        "units": "",
    },
    "angle_index_k": {
        "description": "The angle index k",
        "dimensionality": "[n_angles]",
        "type": "integer",
        "units": "",
    },
    "dihedrals": {
        "description": "The dihedrals",
        "dimensionality": "[n_dihedrals]",
        "type": "float",
        "units": "degree",
    },
    "dihedral_bond_orders_ij": {
        "description": "The bond orders of i, j",
        "dimensionality": "[n_dihedrals]",
        "type": "float",
        "units": "",
    },
    "dihedral_bond_orders_jk": {
        "description": "The bond orders of j, k",
        "dimensionality": "[n_dihedrals]",
        "type": "float",
        "units": "",
    },
    "dihedral_bond_orders_kl": {
        "description": "The bond orders of k, l",
        "dimensionality": "[n_dihedrals]",
        "type": "float",
        "units": "",
    },
    "dihedral_index_i": {
        "description": "The dihedral index i",
        "dimensionality": "[n_dihedrals]",
        "type": "integer",
        "units": "",
    },
    "dihedral_index_j": {
        "description": "The dihedral index j",
        "dimensionality": "[n_dihedrals]",
        "type": "integer",
        "units": "",
    },
    "dihedral_index_k": {
        "description": "The dihedral index k",
        "dimensionality": "[n_dihedrals]",
        "type": "integer",
        "units": "",
    },
    "dihedral_index_l": {
        "description": "The dihedral index l",
        "dimensionality": "[n_dihedrals]",
        "type": "integer",
        "units": "",
    },
    "oops": {
        "description": "The oops",
        "dimensionality": "[n_oops]",
        "type": "float",
        "units": "degree",
    },
    "oop_bond_orders_ij": {
        "description": "The bond orders of i, j",
        "dimensionality": "[n_oops]",
        "type": "float",
        "units": "",
    },
    "oop_bond_orders_jk": {
        "description": "The bond orders of j, k",
        "dimensionality": "[n_oops]",
        "type": "float",
        "units": "",
    },
    "oop_bond_orders_kl": {
        "description": "The bond orders of k, l",
        "dimensionality": "[n_oops]",
        "type": "float",
        "units": "",
    },
    "oop_index_i": {
        "description": "The oop index i",
        "dimensionality": "[n_oops]",
        "type": "integer",
        "units": "",
    },
    "oop_index_j": {
        "description": "The oop index j",
        "dimensionality": "[n_oops]",
        "type": "integer",
        "units": "",
    },
    "oop_index_k": {
        "description": "The oop index k",
        "dimensionality": "[n_oops]",
        "type": "integer",
        "units": "",
    },
    "oop_index_l": {
        "description": "The oop index l",
        "dimensionality": "[n_oops]",
        "type": "integer",
        "units": "",
    },
}
