# -*- coding: utf-8 -*-

"""The graphical part of a Geometry Analysis step"""

import pprint  # noqa: F401
import tkinter as tk
import tkinter.ttk as ttk

import geometry_analysis_step  # noqa: F401
import seamm
from seamm_util import ureg, Q_, units_class  # noqa: F401
import seamm_widgets as sw


class TkGeometryAnalysis(seamm.TkNode):
    """
    The graphical part of a Geometry Analysis step in a flowchart.

    Attributes
    ----------
    tk_flowchart : TkFlowchart = None
        The flowchart that we belong to.
    node : Node = None
        The corresponding node of the non-graphical flowchart
    namespace : str
        The namespace of the current step.
    tk_subflowchart : TkFlowchart
        A graphical Flowchart representing a subflowchart
    canvas: tkCanvas = None
        The Tk Canvas to draw on
    dialog : Dialog
        The Pmw dialog object
    x : int = None
        The x-coordinate of the center of the picture of the node
    y : int = None
        The y-coordinate of the center of the picture of the node
    w : int = 200
        The width in pixels of the picture of the node
    h : int = 50
        The height in pixels of the picture of the node
    self[widget] : dict
        A dictionary of tk widgets built using the information
        contained in Geometry Analysis_parameters.py

    See Also
    --------
    GeometryAnalysis, TkGeometryAnalysis,
    GeometryAnalysisParameters,
    """

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=None,
        y=None,
        w=200,
        h=50,
    ):
        """
        Initialize a graphical node.

        Parameters
        ----------
        tk_flowchart: Tk_Flowchart
            The graphical flowchart that we are in.
        node: Node
            The non-graphical node for this step.
        namespace: str
            The stevedore namespace for finding sub-nodes.
        canvas: Canvas
           The Tk canvas to draw on.
        x: float
            The x position of the nodes center on the canvas.
        y: float
            The y position of the nodes cetner on the canvas.
        w: float
            The nodes graphical width, in pixels.
        h: float
            The nodes graphical height, in pixels.

        Returns
        -------
        None
        """
        self.dialog = None

        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h,
        )

    def create_dialog(self):
        """
        Create the dialog. A set of widgets will be chosen by default
        based on what is specified in the Geometry Analysis_parameters
        module.

        Parameters
        ----------
        None

        Returns
        -------
        None

        See Also
        --------
        TkGeometryAnalysis.reset_dialog
        """

        frame = super().create_dialog(title="Geometry Analysis")
        # Shortcut for parameters
        P = self.node.parameters

        # Then create the widgets
        for key in P:
            if (
                key[0] != "_"
                and key
                not in (
                    "ids",
                    "only first id",
                    "results",
                    "extra keywords",
                    "create tables",
                )
                and "column" not in key
            ):
                self[key] = P[key].widget(frame)

        # Frame for column information
        cframe = self["column frame"] = ttk.LabelFrame(
            frame,
            borderwidth=4,
            relief="sunken",
            text="Column Names",
            labelanchor="n",
            padding=10,
        )
        for key in P:
            if "column" in key or key in ("ids", "only first id"):
                w = self[key] = P[key].widget(cframe)

        # Bindings to make reactive
        for item in ("target", "table output"):
            w = self[item]
            w.combobox.bind("<<ComboboxSelected>>", self.reset_dialog)
            w.combobox.bind("<Return>", self.reset_dialog)
            w.combobox.bind("<FocusOut>", self.reset_dialog)
        for item in ("id column",):
            w = self[item]
            w.combobox.bind("<<ComboboxSelected>>", self.reset_columns)
            w.combobox.bind("<Return>", self.reset_columns)
            w.combobox.bind("<FocusOut>", self.reset_columns)

        # and lay them out
        self.reset_columns()
        self.reset_dialog()

    def reset_columns(self, widget=None):
        # Remove any widgets previously packed
        frame = self["column frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        widgets0 = []
        widgets1 = []
        widgets2 = []
        widgets3 = []

        row = 0
        self["id column"].grid(row=row, column=0, sticky=tk.EW)
        widgets0.append(self["id column"])
        if self["id column"].get().strip() != "":
            self["ids"].grid(row=row, column=1, sticky=tk.EW)
            widgets1.append(self["ids"])
            self["only first id"].grid(row=row, column=2, sticky=tk.EW)
            widgets2.append(self["ids"])
        row += 1

        self["term type column"].grid(row=row, column=0, sticky=tk.EW)
        widgets0.append(self["term type column"])
        row += 1

        self["indx1 column"].grid(row=row, column=0, sticky=tk.EW)
        widgets0.append(self["indx1 column"])
        self["indx2 column"].grid(row=row, column=1, sticky=tk.EW)
        widgets1.append(self["indx2 column"])
        self["indx3 column"].grid(row=row, column=2, sticky=tk.EW)
        widgets2.append(self["indx3 column"])
        self["indx4 column"].grid(row=row, column=3, sticky=tk.EW)
        widgets3.append(self["indx4 column"])
        row += 1

        self["el1 column"].grid(row=row, column=0, sticky=tk.EW)
        widgets0.append(self["el1 column"])
        self["el2 column"].grid(row=row, column=1, sticky=tk.EW)
        widgets1.append(self["el2 column"])
        self["el3 column"].grid(row=row, column=2, sticky=tk.EW)
        widgets2.append(self["el3 column"])
        self["el4 column"].grid(row=row, column=3, sticky=tk.EW)
        widgets3.append(self["el4 column"])
        row += 1

        self["atom indices column"].grid(row=row, column=0, sticky=tk.EW)
        widgets0.append(self["atom indices column"])
        row += 1

        self["term column"].grid(row=row, column=0, sticky=tk.EW)
        widgets0.append(self["term column"])
        row += 1

        self["value column"].grid(row=row, column=0, sticky=tk.EW)
        widgets0.append(self["value column"])
        row += 1

        sw.align_labels(widgets0, sticky=tk.E)
        sw.align_labels(widgets1, sticky=tk.E)
        sw.align_labels(widgets2, sticky=tk.E)
        sw.align_labels(widgets3, sticky=tk.E)

    def reset_dialog(self, widget=None):
        """Layout the widgets in the dialog.
        Parameters
        ----------
        widget : Tk Widget = None

        Returns
        -------
        None

        See Also
        --------
        TkGeometryAnalysis.create_dialog
        """

        # Remove any widgets previously packed
        frame = self["frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        # Shortcut for parameters
        P = self.node.parameters

        # keep track of the row in a variable, so that the layout is flexible
        # if e.g. rows are skipped to control such as "method" here
        row = 0
        widgets = []
        self["target"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        row += 1
        widgets.append(self["target"])
        target = self["target"].get()
        if target == "specified terms":
            self["specification"].grid(row=row, column=1, sticky=tk.EW)
            row += 1
        self["table output"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        row += 1
        widgets.append(self["table output"])
        output = self["table output"].get()
        if "single" in output:
            self["table"].grid(row=row, column=1, sticky=tk.EW)
            row += 1
            self["column frame"].grid(row=row, column=0, columnspan=3, sticky=tk.W)
            row += 1
        elif "separate" in output:
            widgets2 = []
            for key in (
                "bond table",
                "angle table",
                "dihedral table",
                "out-of-plane table",
            ):
                self[key].grid(row=row, column=1, sticky=tk.EW)
                row += 1
                widgets2.append(self[key])
            sw.align_labels(widgets2, sticky=tk.E)
            self["column frame"].grid(row=row, column=0, columnspan=3, sticky=tk.W)
            row += 1

        # Align the labels
        sw.align_labels(widgets, sticky=tk.E)
        frame.columnconfigure(0, minsize=30)

        # Setup the results if there are any
        have_results = (
            "results" in self.node.metadata and len(self.node.metadata["results"]) > 0
        )
        if have_results and "results" in P:
            self.setup_results()

    def right_click(self, event):
        """
        Handles the right click event on the node.

        Parameters
        ----------
        event : Tk Event

        Returns
        -------
        None

        See Also
        --------
        TkGeometryAnalysis.edit
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
