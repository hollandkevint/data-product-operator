import sys
import unittest
from datetime import date

from repo_checks import REPO

sys.path.insert(0, str(REPO / "lib"))
from loop_helpers import is_number, line_value, parse_date, table_rows  # noqa: E402


class ParseDate(unittest.TestCase):
    def test_iso_date(self):
        self.assertEqual(parse_date(" 2026-11-21 "), date(2026, 11, 21))

    def test_junk_is_none_never_a_crash(self):
        for junk in ("", "soon", "2026-13-40", "20261121", "2026-W47-1", "2026-11-21T10:00", None, 20261121, 1.5, [], {}):
            self.assertIsNone(parse_date(junk), junk)


class Small(unittest.TestCase):
    def test_table_rows_skips_rule_row_and_stops_at_table_end(self):
        text = "| Date | X |\n|---|---|\n| a | b |\n\nafter"
        self.assertEqual(table_rows(text, "Date"), [["a", "b"]])

    def test_is_number_rejects_bool_and_text(self):
        self.assertTrue(is_number(2) and is_number(1.5))
        self.assertFalse(is_number(True) or is_number("2") or is_number(None))

    def test_line_value(self):
        self.assertEqual(line_value("a: 1\nname:  x y \n", "name"), "x y")
        self.assertIsNone(line_value("a: 1", "name"))
