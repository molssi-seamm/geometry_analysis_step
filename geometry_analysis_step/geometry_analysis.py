# -*- coding: utf-8 -*-

"""Non-graphical part of the Geometry Analysis step in a SEAMM flowchart
"""

import logging
from pathlib import Path
import pkg_resources
import pprint  # noqa: F401

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
        self,
        flowchart=None,
        title="Geometry Analysis",
        extension=None,
        logger=logger
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
            "Please replace this with a short summary of the "
            "Geometry Analysis step, including key parameters."
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
        next_node = super().run(printer)
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Print what we are doing
        printer.important(__(self.description_text(P), indent=self.indent))

        directory = Path(self.directory)
        directory.mkdir(parents=True, exist_ok=True)

        # Get the current system and configuration (ignoring the system...)
        _, configuration = self.get_system_configuration(None)

        # Results data
        data = {}

        # Temporary code just to print the parameters. You will need to change
        # this!
        for key in P:
            print("{:>15s} = {}".format(key, P[key]))
            printer.normal(
                __(
                    "{key:>15s} = {value}",
                    key=key,
                    value=P[key],
                    indent=4 * " ",
                    wrap=False,
                    dedent=False,
                )
            )

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
        printer.normal(
            __(
                "This is a placeholder for the results from the Geometry Analysis step",
                indent=4 * " ",
                wrap=True,
                dedent=False,
            )
        )
