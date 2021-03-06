# Unit tests for pyNsource that
# check that one to many works in the case of a test submitted by Antonio

import unittest
from parsing.api import old_parser, new_parser
from tests.settings import PYTHON_CODE_EXAMPLES_TO_PARSE
from common.logwriter import LogWriter
from parsing.core_parser_ast import set_DEBUGINFO, DEBUGINFO


class TestIncomingBugs(unittest.TestCase):
    def setUp(self):
        pass

    def test01(self):
        """
        """
        FILE = PYTHON_CODE_EXAMPLES_TO_PARSE + "testmodule_bug_pyplecs.py"

        # Can also run using
        # python3 pynsource-cli.py --mode 3 --graph tests/python-in/testmodule_bug_pyplecs.py

        # create a html log file to contain html info 
        log = LogWriter(FILE, print_to_console=False)
        log.out_html_header()

        # Normally debug info is false for performance reasons, so turn it on temporarily and restore it later
        old_debug_info_value = DEBUGINFO()
        set_DEBUGINFO(True)
        try:
            self.p, debuginfo = new_parser(FILE, log, options={"mode": 3})
        finally:
            set_DEBUGINFO(old_debug_info_value)

        log.out("<hr><h1>Errors:</h1>")
        log.out_wrap_in_html(self.p.errors)
        log.out("<hr><h1>debuginfo:</h1>")

        log.out(debuginfo)
        log.out_html_footer()
        log.finish()

        self.assertEqual(self.p.errors, "")
        print(self.p)

        # -------------------------------------------------------

        # gotevent1 = 0
        # gotevent2 = 0
        # gotevent3 = 0
        # gotevent4 = 0
        # gotevent5 = 0
        # gotevent6 = 0
        # gotevent7 = 0

        # for classname, classentry in list(self.p.classlist.items()):
        #     if classname == "Fred":
        #         gotevent1 = 1
        #         assert classentry.classesinheritsfrom == [
        #             "Mary",
        #             "Sam",
        #         ], classentry.classesinheritsfrom

        #     if classname == "MarySam":
        #         gotevent3 = False  # should not get this

        # assert gotevent1
        # assert not gotevent3

 