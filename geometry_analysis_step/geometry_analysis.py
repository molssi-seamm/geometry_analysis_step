# -*- coding: utf-8 -*-

"""Non-graphical part of the Geometry Analysis step in a SEAMM flowchart
"""

import logging
from pathlib import Path
import pkg_resources
import pprint  # noqa: F401

import numpy as np
import pandas
from tabulate import tabulate

import geometry_analysis_step
import molsystem
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# In addition to the normal logger, two logger-like printing facilities are
# defined: "job" and "printer". "job" send output to the main job.out file for
# the job, and should be used very sparingly, typically to echo what this step
# will do in the initial summary of the job.
#
# "printer" sends output to the file "step.out" in this steps working
# directory, and is used for all normal output from this step.

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("Geometry Analysis")

# Add this module's properties to the standard properties
path = Path(pkg_resources.resource_filename(__name__, "data/"))
csv_file = path / "properties.csv"
if path.exists():
    molsystem.add_properties_from_file(csv_file)


def distance(p1, p2):
    """The distance between two points."""
    return np.linalg.norm(p1 - p2)


def angle(p1, p2, p3):
    """The angle in degrees given the three points."""
    r21 = p1 - p2
    r23 = p3 - p2
    u21 = r21 / np.linalg.norm(r21)
    u23 = r23 / np.linalg.norm(r23)
    return np.degrees(np.arccos(np.clip(np.dot(u21, u23), -1.0, 1.0)))


def dihedral(p1, p2, p3, p4):
    """Praxeolitic formula
    1 sqrt, 1 cross product
    https://stackoverflow.com/questions/20305272/dihedral-torsion-angle-from-four-points-in-cartesian-coordinates-in-python
    """
    b0 = -1.0 * (p2 - p1)
    b1 = p3 - p2
    b2 = p4 - p3

    # normalize b1 so that it does not influence magnitude of vector
    # rejections that come next
    b1 /= np.linalg.norm(b1)

    # vector rejections
    # v = projection of b0 onto plane perpendicular to b1
    #   = b0 minus component that aligns with b1
    # w = projection of b2 onto plane perpendicular to b1
    #   = b2 minus component that aligns with b1
    v = b0 - np.dot(b0, b1) * b1
    w = b2 - np.dot(b2, b1) * b1

    # angle between v and w in a plane is the torsion angle
    # v and w may not be normalized but that's fine since tan is y/x
    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)
    return np.degrees(np.arctan2(y, x))


def oop(p1, p2, p3, p4):
    """The Wilson out-of-plane angle."""
    r21 = p1 - p2
    r23 = p3 - p2
    r24 = p4 - p2
    u21 = r21 / np.linalg.norm(r21)
    u23 = r23 / np.linalg.norm(r23)
    u24 = r24 / np.linalg.norm(r24)

    # The order is such that all angles have the same sign if not
    # near zero, so averaging near zero makes sense
    c34 = np.cross(u24, u23)
    c34 = c34 / np.linalg.norm(c34)
    c14 = np.cross(u21, u24)
    c14 = c14 / np.linalg.norm(c14)
    c13 = np.cross(u21, u23)
    c13 = c13 / np.linalg.norm(c13)

    chi1 = np.rad2deg(np.arcsin(np.clip(np.dot(u21, c34), -1.0, 1.0)))
    chi3 = np.rad2deg(np.arcsin(np.clip(np.dot(u23, c14), -1.0, 1.0)))
    chi4 = np.rad2deg(np.arcsin(np.clip(np.dot(u24, c13), -1.0, 1.0)))

    return abs(chi1 + chi3 + chi4)


class GeometryAnalysis(seamm.Node):
    """
    The non-graphical part of a Geometry Analysis step in a flowchart.

    Attributes
    ----------
    parser : configargparse.ArgParser
        The parser object.

    options : tuple
        It contains a two item tuple containing the populated namespace and the
        list of remaining argument strings.

    subflowchart : seamm.Flowchart
        A SEAMM Flowchart object that represents a subflowchart, if needed.

    parameters : GeometryAnalysisParameters
        The control parameters for Geometry Analysis.

    See Also
    --------
    TkGeometryAnalysis,
    GeometryAnalysis, GeometryAnalysisParameters
    """

    def __init__(
        self, flowchart=None, title="Geometry Analysis", extension=None, logger=logger
    ):
        """A step for Geometry Analysis in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters
        ----------
        flowchart: seamm.Flowchart
            The non-graphical flowchart that contains this step.

        title: str
            The name displayed in the flowchart.
        extension: None
            Not yet implemented
        logger : Logger = logger
            The logger to use and pass to parent classes

        Returns
        -------
        None
        """
        logger.debug(f"Creating Geometry Analysis {self}")

        super().__init__(
            flowchart=flowchart,
            title="Geometry Analysis",
            extension=extension,
            module=__name__,
            logger=logger,
        )  # yapf: disable

        self._metadata = geometry_analysis_step.metadata
        self.parameters = geometry_analysis_step.GeometryAnalysisParameters()

    @property
    def version(self):
        """The semantic version of this module."""
        return geometry_analysis_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return geometry_analysis_step.__git_revision__

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Parameters
        ----------
        P: dict
            An optional dictionary of the current values of the control
            parameters.
        Returns
        -------
        str
            A description of the current step.
        """
        if not P:
            P = self.parameters.values_to_dict()

        text = (
            "Tabulate the bond lengths, angles, dihedral angles, and Wilson "
            "out-of-plane angles for the system."
        )

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def run(self):
        """Run a Geometry Analysis step.

        Parameters
        ----------
        None

        Returns
        -------
        seamm.Node
            The next node object in the flowchart.
        """
        bondorder_text = ("-0-", "-", "=", "#", "-4-", "-5-")

        next_node = super().run(printer)
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Make directory
        directory = Path(self.directory)
        directory.mkdir(parents=True, exist_ok=True)

        root_path = Path(self.flowchart.root_directory).expanduser()

        # Get the current system and configuration (ignoring the system...)
        system, configuration = self.get_system_configuration(None)

        # Get the control parameters
        specified = False
        if "specified" in P["target"]:
            specified = True
            specification = P["specification"]
            target_terms = specification.replace(",", " ").split()
            target = {}
            bonds = target["bonds"] = []
            angles = target["angles"] = []
            dihedrals = target["dihedrals"] = []
            oops = target["oops"] = []
            for term in target_terms:
                if term[0:3] == "oop":
                    try:
                        i, j, k, l = term[3:].split("-")  # noqa: E741
                        oops.append((int(i), int(j), int(k), int(l)))
                    except Exception:
                        logger.warning(f"Cannot interpret out-of-plane '{term}'")
                else:
                    tmp = term.split("-")
                    if len(tmp) == 2:
                        i, j = tmp
                        bonds.append((int(i), int(j)))
                    elif len(tmp) == 3:
                        i, j, k = tmp
                        angles.append((int(i), int(j), int(k)))
                    elif len(tmp) == 4:
                        i, j, k, l = tmp  # noqa: E741
                        dihedrals.append((int(i), int(j), int(k), int(l)))
                    else:
                        logger.warning(f"Cannot interpret specified term '{term}'")

        # Set up tables and columns
        column_name = {}
        column_default = {}
        default = {"string": "", "integer": 0, "float": np.nan}
        for key in P:
            if "column" in key:
                name = key.replace(" column", "")
                column_name[name] = None if P[key].strip() == "" else P[key].strip()
                column_default[name] = default[self.parameters[key]["kind"]]

        id_text = None
        if column_name["id"] is not None:
            id_text = P["ids"]
            if "<system.name>" in id_text:
                id_text = id_text.replace("<system.name>", system.name)
            elif "<configuration.name>" in id_text:
                id_text = id_text.replace("<configuration.name>", configuration.name)

        table_output = P["table output"]
        if "single" in table_output:
            name = P["table"].strip()
            bond_table_name = angle_table_name = dihedral_table_name = name
            oop_table_name = name
            # get_table creates the table if needed. We reget the table later in case
            # it has been changed (by concatenating which replaces it.)
            table = None if name == "" else self.get_table(name)
            if table is not None:
                handle = self.get_variable(name)
                if "filename" not in handle:
                    handle["filename"] = str(
                        root_path / f"{name}.csv".replace(" ", "_")
                    )
                bond_handle = angle_handle = dihedral_handle = oop_handle = handle
                for name in (
                    "id",
                    "term type",
                    "indx1",
                    "indx2",
                    "indx3",
                    "indx4",
                    "el1",
                    "el2",
                    "el3",
                    "el4",
                    "atom indices",
                    "term",
                    "value",
                ):
                    column = column_name[name]
                    if column is not None and column not in table.columns:
                        handle["defaults"][column] = column_default[name]
                        table[column] = column_default[name]
        elif "separate" in table_output:
            bond_table_name = P["bond table"].strip()
            if bond_table_name == "":
                bond_table = None
                bond_handle = None
            else:
                # get_table creates the table if needed. We reget the table later in
                # case it has been changed (by concatenating which replaces it.)
                bond_table = self.get_table(bond_table_name)
                bond_handle = self.get_variable(bond_table_name)
                if "filename" not in bond_handle:
                    bond_handle["filename"] = str(
                        root_path / f"{bond_table_name}.csv".replace(" ", "_")
                    )
                for name in (
                    "id",
                    "term type",
                    "indx1",
                    "indx2",
                    "el1",
                    "el2",
                    "atom indices",
                    "term",
                    "value",
                ):
                    column = column_name[name]
                    if column is not None and column not in bond_table.columns:
                        bond_handle["defaults"][column] = column_default[name]
                        bond_table[column] = column_default[name]

            angle_table_name = P["angle table"].strip()
            if angle_table_name == "":
                angle_table = None
                angle_handle = None
            else:
                # get_table creates the table if needed. We reget the table later in
                # case it has been changed (by concatenating which replaces it.)
                angle_table = self.get_table(angle_table_name)
                angle_handle = self.get_variable(angle_table_name)
                if "filename" not in angle_handle:
                    angle_handle["filename"] = str(
                        root_path / f"{angle_table_name}.csv".replace(" ", "_")
                    )
                for name in (
                    "id",
                    "term type",
                    "indx1",
                    "indx2",
                    "indx3",
                    "el1",
                    "el2",
                    "el3",
                    "atom indices",
                    "term",
                    "value",
                ):
                    column = column_name[name]
                    if column is not None and column not in angle_table.columns:
                        angle_handle["defaults"][column] = column_default[name]
                        angle_table[column] = column_default[name]

            dihedral_table_name = P["dihedral table"].strip()
            if dihedral_table_name == "":
                dihedral_table = None
                dihedral_handle = None
            else:
                # get_table creates the table if needed. We reget the table later in
                # case it has been changed (by concatenating which replaces it.)
                dihedral_table = self.get_table(dihedral_table_name)
                dihedral_handle = self.get_variable(dihedral_table_name)
                if "filename" not in dihedral_handle:
                    dihedral_handle["filename"] = str(
                        root_path / f"{dihedral_table_name}.csv".replace(" ", "_")
                    )
                for name in (
                    "id",
                    "term type",
                    "indx1",
                    "indx2",
                    "indx3",
                    "indx4",
                    "el1",
                    "el2",
                    "el3",
                    "el4",
                    "atom indices",
                    "term",
                    "value",
                ):
                    column = column_name[name]
                    if column is not None and column not in dihedral_table.columns:
                        dihedral_handle["defaults"][column] = column_default[name]
                        dihedral_table[column] = column_default[name]

            oop_table_name = P["out-of-plane table"].strip()
            if oop_table_name == "":
                oop_table = None
                oop_handle = None
            else:
                # get_table creates the table if needed. We reget the table later in
                # case it has been changed (by concatenating which replaces it.)
                oop_table = self.get_table(oop_table_name)
                oop_handle = self.get_variable(oop_table_name)
                if "filename" not in oop_handle:
                    oop_handle["filename"] = str(root_path / f"{oop_table_name}.csv")
                for name in (
                    "id",
                    "term type",
                    "indx1",
                    "indx2",
                    "indx3",
                    "indx4",
                    "el1",
                    "el2",
                    "el3",
                    "el4",
                    "atom indices",
                    "term",
                    "value",
                ):
                    column = column_name[name]
                    if column is not None and column not in oop_table.columns:
                        oop_handle["defaults"][column] = column_default[name]
                        oop_table[column] = column_default[name]
        else:
            table_output = None
            bond_table = angle_table = dihedral_table = oop_table = None
            bond_handle = angle_handle = dihedral_handle = oop_handle = None

        # Print what we are doing
        printer.important(__(self.description_text(P), indent=self.indent))

        # Print some info about the configuration
        n_atoms = configuration.n_atoms
        text = f"Number of atoms: {n_atoms}\n"

        XYZ = configuration.atoms.get_coordinates(as_array=True)

        # Convert atom id to index 0, 1, ...
        index = {at: i for i, at in enumerate(configuration.atoms.ids)}

        # Get the bond information and elements
        symbol = configuration.atoms.symbols

        bonds = configuration.bonds.get_as_dict()
        iat = [index[i] + 1 for i in bonds["i"]]
        jat = [index[j] + 1 for j in bonds["j"]]

        # ... and the bond orders for printing
        bondorders = {}
        for i, j, order in zip(iat, jat, bonds["bondorder"]):
            txt = bondorder_text[order]
            bondorders[(i, j)] = txt
            bondorders[(j, i)] = txt

        # And atoms bonded to each atom
        neighbors = [set() for i in range(n_atoms + 1)]
        for i, j in zip(iat, jat):
            neighbors[i].add(j)
            neighbors[j].add(i)

        n_bonds = len(iat)
        n_angles = 0
        n_dihedrals = 0
        n_oops = 0
        have_first_id = False

        #
        # Bond terms
        #

        # The atom indices for the bonds sorted so el1 < el2
        _is = []
        _js = []
        el1s = []
        el2s = []
        if specified:
            for i, j in target["bonds"]:
                el1 = symbol[i - 1]
                el2 = symbol[j - 1]
                if el1 < el2:
                    _is.append(i)
                    _js.append(j)
                    el1s.append(el1)
                    el2s.append(el2)
                else:
                    _is.append(j)
                    _js.append(i)
                    el1s.append(el2)
                    el2s.append(el1)
        else:
            for i, j in zip(iat, jat):
                el1 = symbol[i - 1]
                el2 = symbol[j - 1]
                if el1 < el2:
                    _is.append(i)
                    _js.append(j)
                    el1s.append(el1)
                    el2s.append(el2)
                else:
                    _is.append(j)
                    _js.append(i)
                    el1s.append(el2)
                    el2s.append(el1)
        b12s = [
            bondorders[(i, j)] if (i, j) in bondorders else "."
            for i, j in zip(_is, _js)
        ]
        indices = [f"{i}-{j}" for i, j in zip(_is, _js)]
        terms = [f"{el1}{b12}{el2}" for el1, el2, b12 in zip(el1s, el2s, b12s)]
        values = [f"{distance(XYZ[i - 1], XYZ[j - 1]):.4f}" for i, j in zip(_is, _js)]
        n_bonds = len(values)

        if n_bonds == 0:
            text += "\nThere are no bonds in this system.\n"
        else:
            if bond_handle is not None:
                bond_table = bond_handle["table"]
                rows = {}

                column = column_name["id"]
                if column is not None:
                    if P["only first id"]:
                        rows[column] = [
                            id_text if i == 0 else "" for i in range(n_bonds)
                        ]
                        have_first_id = True
                    else:
                        rows[column] = [id_text for i in range(n_bonds)]

                column = column_name["term type"]
                if column is not None:
                    rows[column] = ["bond" for i in _is]

                column = column_name["indx1"]
                if column is not None:
                    rows[column] = _is

                column = column_name["indx2"]
                if column is not None:
                    rows[column] = _js

                column = column_name["el1"]
                if column is not None:
                    rows[column] = el1s

                column = column_name["el2"]
                if column is not None:
                    rows[column] = el2s

                column = column_name["atom indices"]
                if column is not None:
                    rows[column] = indices

                column = column_name["term"]
                if column is not None:
                    rows[column] = terms

                column = column_name["value"]
                if column is not None:
                    rows[column] = values

                rows = pandas.DataFrame.from_dict(rows)
                bond_table = pandas.concat([bond_table, rows], ignore_index=True)
                bond_handle["table"] = bond_table
                bond_handle["current index"] = bond_table.shape[0] - 1

                # Save!
                self._save_table(bond_handle)

            if True:
                tab = {
                    "Atoms": indices,
                    "Bond": terms,
                    "Value (Å)": values,
                }
                tmp = tabulate(
                    tab,
                    headers="keys",
                    tablefmt="pretty",
                    disable_numparse=True,
                    colalign=("center", "center", "right"),
                )
                length = len(tmp.splitlines()[0])
                text += "\n"
                text += "Bonds".center(length)
                text += "\n"
                text += tmp
                text += "\n"

        #
        # Angle terms
        #

        # The atom indices for the angles sorted so el1 < el3
        _is = []
        _js = []
        _ks = []
        el1s = []
        el2s = []
        el3s = []
        if specified:
            for i, j, k in target["angles"]:
                el2 = symbol[j - 1]
                el1 = symbol[i - 1]
                el3 = symbol[k - 1]
                _js.append(j)
                el2s.append(el2)
                if el1 < el3:
                    _is.append(i)
                    _ks.append(k)
                    el1s.append(el1)
                    el3s.append(el3)
                else:
                    _is.append(k)
                    _ks.append(i)
                    el1s.append(el3)
                    el3s.append(el1)
        else:
            for j in range(n_atoms):
                el2 = symbol[j - 1]
                tmp = sorted(neighbors[j])
                for c, i in enumerate(tmp):
                    el1 = symbol[i - 1]
                    for k in tmp[c + 1 :]:
                        el3 = symbol[k - 1]
                        _js.append(j)
                        el2s.append(el2)
                        if el1 < el3:
                            _is.append(i)
                            _ks.append(k)
                            el1s.append(el1)
                            el3s.append(el3)
                        else:
                            _is.append(k)
                            _ks.append(i)
                            el1s.append(el3)
                            el3s.append(el1)
        b12s = [
            bondorders[(i, j)] if (i, j) in bondorders else "."
            for i, j in zip(_is, _js)
        ]
        b23s = [
            bondorders[(j, k)] if (j, k) in bondorders else "."
            for j, k in zip(_js, _ks)
        ]
        indices = [f"{i}-{j}-{k}" for i, j, k in zip(_is, _js, _ks)]
        terms = [
            f"{el1}{b12}{el2}{b23}{el3}"
            for el1, el2, el3, b12, b23 in zip(el1s, el2s, el3s, b12s, b23s)
        ]
        values = [
            f"{angle(XYZ[i - 1], XYZ[j - 1], XYZ[k - 1]):.2f}"
            for i, j, k in zip(_is, _js, _ks)
        ]
        n_angles = len(values)

        if n_angles == 0:
            text += "\nThere are no angles in this system.\n"
        else:
            if angle_handle is not None:
                angle_table = angle_handle["table"]
                rows = {}

                column = column_name["id"]
                if column is not None:
                    if P["only first id"]:
                        if "single" in P["table output"] and have_first_id:
                            rows[column] = ["" for i in range(n_angles)]
                        else:
                            rows[column] = [
                                id_text if i == 0 else "" for i in range(n_angles)
                            ]
                            have_first_id = True
                    else:
                        rows[column] = [id_text for i in range(n_angles)]

                column = column_name["term type"]
                if column is not None:
                    rows[column] = ["angle" for i in _is]

                column = column_name["indx1"]
                if column is not None:
                    rows[column] = _is

                column = column_name["indx2"]
                if column is not None:
                    rows[column] = _js

                column = column_name["indx3"]
                if column is not None:
                    rows[column] = _ks

                column = column_name["el1"]
                if column is not None:
                    rows[column] = el1s

                column = column_name["el2"]
                if column is not None:
                    rows[column] = el2s

                column = column_name["el3"]
                if column is not None:
                    rows[column] = el3s

                column = column_name["atom indices"]
                if column is not None:
                    rows[column] = indices

                column = column_name["term"]
                if column is not None:
                    rows[column] = terms

                column = column_name["value"]
                if column is not None:
                    rows[column] = values

                rows = pandas.DataFrame.from_dict(rows)
                angle_table = pandas.concat([angle_table, rows], ignore_index=True)
                angle_handle["table"] = angle_table
                angle_handle["current index"] = angle_table.shape[0] - 1

                # Save!
                self._save_table(angle_handle)

            if True:
                tab = {
                    "Atoms": indices,
                    "Angle": terms,
                    "Value (º)": values,
                }
                tmp = tabulate(
                    tab,
                    headers="keys",
                    tablefmt="pretty",
                    disable_numparse=True,
                    colalign=("center", "center", "right"),
                )
                length = len(tmp.splitlines()[0])
                text += "\n"
                text += "Angles".center(length)
                text += "\n"
                text += tmp
                text += "\n"

        #
        # Dihedral terms
        #

        # The atom indices for the dihedrals sorted so el2 <= el3
        # and el1 < el4 if el2 == el3
        _is = []
        _js = []
        _ks = []
        _ls = []
        el1s = []
        el2s = []
        el3s = []
        el4s = []
        if specified:
            for i, j, k, l in target["dihedrals"]:
                el1 = symbol[i - 1]
                el2 = symbol[j - 1]
                el3 = symbol[k - 1]
                el4 = symbol[l - 1]
                if el2 == el3:
                    if el1 < el4:
                        ii, jj, kk, ll = i, j, k, l
                        e1, e2, e3, e4 = el1, el2, el3, el4
                    else:
                        ii, jj, kk, ll = l, k, j, i
                        e1, e2, e3, e4 = el4, el3, el2, el1
                elif el2 < el3:
                    ii, jj, kk, ll = i, j, k, l
                    e1, e2, e3, e4 = el1, el2, el3, el4
                else:
                    ii, jj, kk, ll = l, k, j, i
                    e1, e2, e3, e4 = el4, el3, el2, el1
                _is.append(ii)
                _js.append(jj)
                _ks.append(kk)
                _ls.append(ll)
                el1s.append(e1)
                el2s.append(e2)
                el3s.append(e3)
                el4s.append(e4)
        else:
            for j, k in zip(iat, jat):
                el2 = symbol[j - 1]
                el3 = symbol[k - 1]
                for i in sorted(neighbors[j]):
                    if i == k:
                        continue
                    el1 = symbol[i - 1]
                    for l in sorted(neighbors[k]):  # noqa: E741
                        if l == j:  # noqa: E741
                            continue
                        el4 = symbol[l - 1]
                        if el2 == el3:
                            if el1 < el4:
                                ii, jj, kk, ll = i, j, k, l
                                e1, e2, e3, e4 = el1, el2, el3, el4
                            else:
                                ii, jj, kk, ll = l, k, j, i
                                e1, e2, e3, e4 = el4, el3, el2, el1
                        elif el2 < el3:
                            ii, jj, kk, ll = i, j, k, l
                            e1, e2, e3, e4 = el1, el2, el3, el4
                        else:
                            ii, jj, kk, ll = l, k, j, i
                            e1, e2, e3, e4 = el4, el3, el2, el1
                        _is.append(ii)
                        _js.append(jj)
                        _ks.append(kk)
                        _ls.append(ll)
                        el1s.append(e1)
                        el2s.append(e2)
                        el3s.append(e3)
                        el4s.append(e4)
        b12s = [
            bondorders[(i, j)] if (i, j) in bondorders else "."
            for i, j in zip(_is, _js)
        ]
        b23s = [
            bondorders[(j, k)] if (j, k) in bondorders else "."
            for j, k in zip(_js, _ks)
        ]
        b34s = [
            bondorders[(k, l)] if (k, l) in bondorders else "."
            for k, l in zip(_ks, _ls)
        ]
        indices = [f"{i}-{j}-{k}-{l}" for i, j, k, l in zip(_is, _js, _ks, _ls)]
        terms = [
            f"{el1}{b12}{el2}{b23}{el3}{b34}{el4}"
            for el1, el2, el3, el4, b12, b23, b34 in zip(
                el1s, el2s, el3s, el4s, b12s, b23s, b34s
            )
        ]
        values = [
            f"{dihedral(XYZ[i - 1], XYZ[j - 1], XYZ[k - 1], XYZ[l - 1]):.2f}"
            for i, j, k, l in zip(_is, _js, _ks, _ls)
        ]
        descriptions = []
        for phi in values:
            phi = float(phi)
            if phi >= -30 and phi <= 30:
                descriptions.append("C  = synperiplaner")
            elif phi > 30 and phi <= 90:
                descriptions.append("G+ = +synclinal")
            elif phi > 90 and phi <= 150:
                descriptions.append("A+ = +anticlinal")
            elif phi > 150 or phi < -150:
                descriptions.append("T  = antiperiplaner")
            elif phi >= 150 and phi < -90:
                descriptions.append("A- = -anticlinal")
            elif phi <= 90 and phi < -30:
                descriptions.append("G- = -synclinal")

        n_dihedrals = len(values)

        if n_dihedrals == 0:
            text += "\nThere are no dihedrals in this system.\n"
        else:
            if dihedral_handle is not None:
                dihedral_table = dihedral_handle["table"]
                rows = {}

                column = column_name["id"]
                if column is not None:
                    if P["only first id"]:
                        if "single" in P["table output"] and have_first_id:
                            rows[column] = ["" for i in range(n_dihedrals)]
                        else:
                            rows[column] = [
                                id_text if i == 0 else "" for i in range(n_dihedrals)
                            ]
                            have_first_id = True
                        have_first_id = True
                    else:
                        rows[column] = [id_text for i in range(n_dihedrals)]

                column = column_name["term type"]
                if column is not None:
                    rows[column] = ["dihedral" for i in _is]

                column = column_name["indx1"]
                if column is not None:
                    rows[column] = _is

                column = column_name["indx2"]
                if column is not None:
                    rows[column] = _js

                column = column_name["indx3"]
                if column is not None:
                    rows[column] = _ks

                column = column_name["indx4"]
                if column is not None:
                    rows[column] = _ls

                column = column_name["el1"]
                if column is not None:
                    rows[column] = el1s

                column = column_name["el2"]
                if column is not None:
                    rows[column] = el2s

                column = column_name["el3"]
                if column is not None:
                    rows[column] = el3s

                column = column_name["el4"]
                if column is not None:
                    rows[column] = el4s

                column = column_name["atom indices"]
                if column is not None:
                    rows[column] = indices

                column = column_name["term"]
                if column is not None:
                    rows[column] = terms

                column = column_name["value"]
                if column is not None:
                    rows[column] = values

                rows = pandas.DataFrame.from_dict(rows)
                dihedral_table = pandas.concat(
                    [dihedral_table, rows], ignore_index=True
                )
                dihedral_handle["table"] = dihedral_table
                dihedral_handle["current index"] = dihedral_table.shape[0] - 1

                # Save!
                self._save_table(dihedral_handle)

            if True:
                tab = {
                    "Atoms": indices,
                    "Dihedral": terms,
                    "Value (º)": values,
                    "Description": descriptions,
                }
                tmp = tabulate(
                    tab,
                    headers="keys",
                    tablefmt="pretty",
                    disable_numparse=True,
                    colalign=("center", "center", "right", "left"),
                )
                length = len(tmp.splitlines()[0])
                text += "\n"
                text += "Dihedral Angles".center(length)
                text += "\n"
                text += tmp
                text += "\n"

        #
        # Out-of-plane terms
        #

        # The atom indices for the oops sorted so el1 < el3 < el4
        _is = []
        _js = []
        _ks = []
        _ls = []
        el1s = []
        el2s = []
        el3s = []
        el4s = []
        if specified:
            for i, j, k, l in target["dihedrals"]:
                el1 = symbol[i - 1]
                el2 = symbol[j - 1]
                el3 = symbol[k - 1]
                el4 = symbol[l - 1]
                els = sorted([(el1, i), (el3, k), (el4, l)], key=lambda tmp: tmp[0])
                el1, i = els[0]
                el3, k = els[1]
                el4, l = els[2]  # noqa: E741
        else:
            for j in range(n_atoms):
                if len(neighbors[j]) != 3:
                    continue
                el2 = symbol[j - 1]
                els = sorted(
                    [(symbol[i - 1], i) for i in neighbors[j]], key=lambda tmp: tmp[0]
                )
                el1, i = els[0]
                el3, k = els[1]
                el4, l = els[2]  # noqa: E741
                _is.append(i)
                _js.append(j)
                _ks.append(k)
                _ls.append(l)
                el1s.append(el1)
                el2s.append(el2)
                el3s.append(el3)
                el4s.append(el4)
        b21s = [
            bondorders[(j, i)] if (j, i) in bondorders else "."
            for j, i in zip(_js, _is)
        ]
        b23s = [
            bondorders[(j, k)] if (j, k) in bondorders else "."
            for j, k in zip(_js, _ks)
        ]
        b24s = [
            bondorders[(j, l)] if (j, l) in bondorders else "."
            for j, l in zip(_js, _ls)
        ]
        indices = [f"{i}-{j}(-{k})-{l}" for i, j, k, l in zip(_is, _js, _ks, _ls)]
        terms = [
            f"{el1}{b21}{el2}({b23}{el3}){b34}{el4}"
            for el1, el2, el3, el4, b21, b23, b34 in zip(
                el1s, el2s, el3s, el4s, b21s, b23s, b24s
            )
        ]
        values = [
            f"{oop(XYZ[i - 1], XYZ[j - 1], XYZ[k - 1], XYZ[l - 1]):.2f}"
            for i, j, k, l in zip(_is, _js, _ks, _ls)
        ]

        n_oops = len(values)

        if n_oops == 0:
            text += "\nThere are no out-of-planes in this system.\n"
        else:
            if oop_handle is not None:
                oop_table = oop_handle["table"]
                rows = {}

                column = column_name["id"]
                if column is not None:
                    if P["only first id"]:
                        if "single" in P["table output"] and have_first_id:
                            rows[column] = ["" for i in range(n_oops)]
                        else:
                            rows[column] = [
                                id_text if i == 0 else "" for i in range(n_oops)
                            ]
                            have_first_id = True
                        have_first_id = True
                    else:
                        rows[column] = [id_text for i in range(n_oops)]

                column = column_name["term type"]
                if column is not None:
                    rows[column] = ["oop" for i in _is]

                column = column_name["indx1"]
                if column is not None:
                    rows[column] = _is

                column = column_name["indx2"]
                if column is not None:
                    rows[column] = _js

                column = column_name["indx3"]
                if column is not None:
                    rows[column] = _ks

                column = column_name["indx4"]
                if column is not None:
                    rows[column] = _ls

                column = column_name["el1"]
                if column is not None:
                    rows[column] = el1s

                column = column_name["el2"]
                if column is not None:
                    rows[column] = el2s

                column = column_name["el3"]
                if column is not None:
                    rows[column] = el3s

                column = column_name["el4"]
                if column is not None:
                    rows[column] = el4s

                column = column_name["atom indices"]
                if column is not None:
                    rows[column] = indices

                column = column_name["term"]
                if column is not None:
                    rows[column] = terms

                column = column_name["value"]
                if column is not None:
                    rows[column] = values

                rows = pandas.DataFrame.from_dict(rows)
                oop_table = pandas.concat([oop_table, rows], ignore_index=True)
                oop_handle["table"] = oop_table
                oop_handle["current index"] = oop_table.shape[0] - 1

                # Save!
                self._save_table(oop_handle)

            if True:
                tab = {
                    "Atoms": indices,
                    "Oop": terms,
                    "Value (º)": values,
                }
                tmp = tabulate(
                    tab,
                    headers="keys",
                    tablefmt="pretty",
                    disable_numparse=True,
                    colalign=("center", "center", "right"),
                )
                length = len(tmp.splitlines()[0])
                text += "\n"
                text += "Out-of-plane Angles".center(length)
                text += "\n"
                text += tmp
                text += "\n"

        # Results data
        data = {}

        printer.normal(__(text, indent=4 * " ", wrap=False, dedent=False))

        # Analyze the results
        self.analyze()

        # Put any requested results into variables or tables
        self.store_results(
            configuration=configuration,
            data=data,
        )

        # Add other citations here or in the appropriate place in the code.
        # Add the bibtex to data/references.bib, and add a self.reference.cite
        # similar to the above to actually add the citation to the references.

        return next_node

    def analyze(self, indent="", **kwargs):
        """Do any analysis of the output from this step.

        Also print important results to the local step.out file using
        "printer".

        Parameters
        ----------
        indent: str
            An extra indentation for the output
        """
        pass

    def _save_table(self, handle):
        """Write a table to disk."""
        filename = handle["filename"]
        index = handle["index column"]
        file_type = Path(filename).suffix
        table = handle["table"]
        if file_type == ".csv":
            if index is None:
                table.to_csv(filename, index=False)
            else:
                table.to_csv(filename, index=True, header=True)
        elif file_type == ".json":
            if index is None:
                table.to_json(filename, indent=4, orient="table", index=False)
            else:
                table.to_json(filename, indent=4, orient="table", index=True)
        elif file_type == ".xlsx":
            if index is None:
                table.to_excel(filename, index=False)
            else:
                table.to_excel(filename, index=True)
        elif file_type == ".txt":
            with open(filename, "w") as fd:
                if index is None:
                    fd.write(table.to_string(header=True, index=False))
                else:
                    fd.write(table.to_string(header=True, index=True))
        else:
            raise RuntimeError(
                f"Save table: cannot handle format '{file_type}' for file "
                f"'{filename}'"
            )
