"""Tests for the memory signal viewer."""

import csv
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import memory_signal_viewer as viewer  # noqa: E402


CSV_HEADER = [
    "id", "data_owner_id", "data_owner_id_type", "domain", "process_capability",
    "schema_version", "attributes", "created_at", "updated_at", "event_time",
    "reference_keys", "data_expiration_time", "consents", "data_source",
]


def _row(id_, owner, attributes, event_time):
    """Build a CSV row dict with only the fields the viewer reads."""
    base = {col: "" for col in CSV_HEADER}
    base.update({
        "id": id_,
        "data_owner_id": owner,
        "attributes": attributes,
        "event_time": event_time,
    })
    return base


def _write_csv(rows):
    """Write rows to a temp CSV and return its path."""
    fd, path = tempfile.mkstemp(suffix=".csv")
    with os.fdopen(fd, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


def _attrs(signals=None, content="hi", timestamp="2026-06-25T20:27:40.527000+00:00"):
    d = {"raw_message": {"content": content, "timestamp": timestamp}}
    if signals is not None:
        d["signals"] = signals
    return json.dumps(d)


class LoadRecordsTest(unittest.TestCase):
    def test_parses_owner_content_and_signals(self):
        path = _write_csv([
            _row("1", "owner-a", _attrs(signals={"property_intent_type": "buyer"},
                                        content="User: hello"),
                 "2026-06-25 20:27:40.527"),
        ])
        try:
            records = viewer.load_records(path)
        finally:
            os.remove(path)

        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertEqual(rec["owner_id"], "owner-a")
        self.assertEqual(rec["content"], "User: hello")
        self.assertEqual(rec["signals"], {"property_intent_type": "buyer"})
        self.assertEqual(rec["raw_id"], "1")

    def test_missing_signals_is_none(self):
        path = _write_csv([_row("1", "owner-a", _attrs(), "2026-06-25 20:27:40.527")])
        try:
            records = viewer.load_records(path)
        finally:
            os.remove(path)
        self.assertIsNone(records[0]["signals"])

    def test_uses_raw_message_timestamp(self):
        path = _write_csv([
            _row("1", "owner-a",
                 _attrs(timestamp="2026-06-25T23:51:31.003000+00:00"),
                 "2026-06-26 09:51:45.506"),
        ])
        try:
            records = viewer.load_records(path)
        finally:
            os.remove(path)
        self.assertEqual(records[0]["timestamp"], "2026-06-25T23:51:31.003000+00:00")

    def test_falls_back_to_event_time_when_no_raw_timestamp(self):
        attrs = json.dumps({"raw_message": {"content": "hi"}})
        path = _write_csv([_row("1", "owner-a", attrs, "2026-06-26 09:51:45.506")])
        try:
            records = viewer.load_records(path)
        finally:
            os.remove(path)
        self.assertEqual(records[0]["timestamp"], "2026-06-26 09:51:45.506")

    def test_skips_unparseable_attributes(self):
        path = _write_csv([
            _row("1", "owner-a", "{not valid json", "2026-06-25 20:27:40.527"),
            _row("2", "owner-b", _attrs(content="ok"), "2026-06-25 20:27:40.527"),
        ])
        try:
            records = viewer.load_records(path)
        finally:
            os.remove(path)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["owner_id"], "owner-b")


class GroupByOwnerTest(unittest.TestCase):
    def test_groups_and_sorts_oldest_first(self):
        records = [
            {"owner_id": "a", "timestamp": "2026-06-25T12:00:00", "content": "second"},
            {"owner_id": "b", "timestamp": "2026-06-25T09:00:00", "content": "b-only"},
            {"owner_id": "a", "timestamp": "2026-06-25T08:00:00", "content": "first"},
        ]
        groups = viewer.group_by_owner(records)

        self.assertEqual(list(groups.keys()), ["a", "b"])
        self.assertEqual([r["content"] for r in groups["a"]], ["first", "second"])
        self.assertEqual(len(groups["b"]), 1)


class FormatSignalsTest(unittest.TestCase):
    def test_none_signals_renders_placeholder(self):
        self.assertIn("(none)", viewer.format_signals(None))

    def test_renders_keys_and_values(self):
        out = viewer.format_signals({"property_intent_type": "buyer"})
        self.assertIn("property_intent_type", out)
        self.assertIn("buyer", out)


class FormatRecordTest(unittest.TestCase):
    def test_includes_header_signals_and_message(self):
        rec = {
            "owner_id": "owner-abcdef", "timestamp": "2026-06-25T20:27:40",
            "signals": {"property_intent_type": "buyer"},
            "content": "User: hello\nAgent: hi", "raw_id": "1",
        }
        out = viewer.format_record(rec, 0, 3)
        self.assertIn("1/3", out)
        self.assertIn("SIGNALS", out)
        self.assertIn("buyer", out)
        self.assertIn("RAW MESSAGE", out)
        self.assertIn("User: hello", out)


class ColorEnabledTest(unittest.TestCase):
    class _Stream:
        def __init__(self, tty):
            self._tty = tty

        def isatty(self):
            return self._tty

    def test_disabled_when_forced(self):
        self.assertFalse(viewer.color_enabled(self._Stream(True), {}, force_no_color=True))

    def test_disabled_when_no_color_env_present(self):
        self.assertFalse(viewer.color_enabled(self._Stream(True), {"NO_COLOR": "1"}))

    def test_disabled_when_not_a_tty(self):
        self.assertFalse(viewer.color_enabled(self._Stream(False), {}))

    def test_enabled_when_tty_and_no_env(self):
        self.assertTrue(viewer.color_enabled(self._Stream(True), {}))


class PaletteTest(unittest.TestCase):
    def test_disabled_palette_returns_text_unchanged(self):
        paint = viewer.Palette(enabled=False)
        self.assertEqual(paint.header("hi"), "hi")

    def test_enabled_palette_wraps_with_ansi_and_reset(self):
        paint = viewer.Palette(enabled=True)
        out = paint.header("hi")
        self.assertTrue(out.startswith("\033["))
        self.assertTrue(out.endswith("\033[0m"))
        self.assertIn("hi", out)


class FormatRecordColorTest(unittest.TestCase):
    REC = {
        "owner_id": "owner-abcdef", "timestamp": "2026-06-25T20:27:40",
        "signals": {"property_intent_type": "buyer"},
        "content": "User: hello\nAgent: hi", "raw_id": "1",
    }

    def test_no_color_output_has_no_escape_codes(self):
        out = viewer.format_record(self.REC, 0, 3, viewer.Palette(enabled=False))
        self.assertNotIn("\033[", out)
        self.assertIn("User: hello", out)

    def test_colored_output_has_escape_codes_and_preserves_text(self):
        out = viewer.format_record(self.REC, 0, 3, viewer.Palette(enabled=True))
        self.assertIn("\033[", out)
        self.assertIn("User: hello", out)
        self.assertIn("buyer", out)


if __name__ == "__main__":
    unittest.main()
