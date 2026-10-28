import importlib.machinery
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_with_config(config):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(config, handle)
    os.environ["MEETINGS_CONFIG"] = handle.name
    try:
        loader = importlib.machinery.SourceFileLoader(
            "meetings_widget_hours", str(ROOT / "bin" / "meetings-widget"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        return module
    finally:
        os.unlink(handle.name)


class DayHoursTests(unittest.TestCase):
    def test_defaults_without_config(self):
        widget = load_with_config({})
        self.assertEqual((widget.DAY_START_HOUR, widget.DAY_END_HOUR), (7, 23))

    def test_configured_hours(self):
        widget = load_with_config({"dayStartHour": 8, "dayEndHour": 17})
        self.assertEqual((widget.DAY_START_HOUR, widget.DAY_END_HOUR), (8, 17))

    def test_inverted_hours_fall_back_to_defaults(self):
        widget = load_with_config({"dayStartHour": 18, "dayEndHour": 9})
        self.assertEqual((widget.DAY_START_HOUR, widget.DAY_END_HOUR), (7, 23))

    def test_non_numbers_are_ignored(self):
        widget = load_with_config({"dayStartHour": "8", "dayEndHour": True})
        self.assertEqual((widget.DAY_START_HOUR, widget.DAY_END_HOUR), (7, 23))


if __name__ == "__main__":
    unittest.main()
