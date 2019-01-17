from .base_cmd import CmdBase
import wx
from beautifultable import BeautifulTable
from termcolor import colored  # also install colorama to make this work on windows
from parsing.dump_pmodel import dump_old_structure


class CmdDumpDisplayModel(CmdBase):
    def execute(self):
        # Also called by Snapshot manager.
        # When create Snapshot manager we pass ourselves as a controller and DumpStatus() is expected to exist.
        import locale

        # http://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators-in-python-2-x
        locale.setlocale(locale.LC_ALL, "")

        # self.dump_parse_models()
        table = self.context.coordmapper.DumpCalibrationInfo(dump_nodes=False, doprint=False)
        self.dump_overlaps(into_existing_table=table)
        self.context.displaymodel.Dump()

    def dump_parse_models(self):
        for pmodel in self.context.displaymodel.pmodels_i_have_seen:
            print(dump_old_structure(pmodel))

    def dump_overlaps(self, into_existing_table=None):
        if into_existing_table:
            t = into_existing_table
        else:
            t = BeautifulTable()
        t.append_row(["bounds", self.context.displaymodel.graph.GetBounds()[0], self.context.displaymodel.graph.GetBounds()[1]])
        t.append_row(["node-node overlaps", self.context.overlap_remover.CountOverlaps(), ""])
        t.append_row(["line-line intersections, crossings",
                      len(self.context.displaymodel.graph.CountLineOverLineIntersections()),
                      self.context.displaymodel.graph.CountLineOverNodeCrossings()["ALL"] / 2])

        t.column_alignments[0] = BeautifulTable.ALIGN_LEFT
        t.row_separator_char = ''
        print(t)
