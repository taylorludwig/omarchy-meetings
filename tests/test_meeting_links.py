import datetime
import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load():
    loader = importlib.machinery.SourceFileLoader(
        "meetings_widget_links", str(ROOT / "bin" / "meetings-widget"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class MeetingLinkInText(unittest.TestCase):
    def setUp(self):
        self.mw = load()

    def test_zoom_link_in_location(self):
        url = "https://us02web.zoom.us/j/83586232378?pwd=abc123"
        self.assertEqual(self.mw.text_meeting_uri(url, ""), url)

    def test_zoom_link_in_escaped_description(self):
        desc = "Join Zoom Meeting\\nhttps://us06web.zoom.us/j/813?pwd=x.1\\n\\nMeeting ID"
        self.assertEqual(self.mw.text_meeting_uri("", desc), "https://us06web.zoom.us/j/813?pwd=x.1")

    def test_location_wins_over_description(self):
        self.assertEqual(
            self.mw.text_meeting_uri("https://meet.google.com/abc-defg-hij",
                                     "https://us02web.zoom.us/j/1"),
            "https://meet.google.com/abc-defg-hij")

    def test_other_links_are_not_meetings(self):
        self.assertEqual(self.mw.text_meeting_uri("Room 4", "Notes: https://docs.google.com/d/1"), "")

    def test_google_row_without_conference_uses_location(self):
        row = {"start_date": "2026-10-28", "start_time": "10:00", "end_date": "2026-10-28",
               "end_time": "10:30", "title": "Weekly", "calendar": "me",
               "location": "https://us02web.zoom.us/j/835?pwd=x", "description": ""}
        event = self.mw.event_from(row, datetime.date(2026, 10, 28))
        self.assertEqual(event.get("hangout"), "https://us02web.zoom.us/j/835?pwd=x")


if __name__ == "__main__":
    unittest.main()
