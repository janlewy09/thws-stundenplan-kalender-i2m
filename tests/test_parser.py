import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from update_calendar import build_ics, parse_timetable  # noqa: E402


class TimetableParserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "tests" / "fixture.html").read_text(encoding="utf-8")
        cls.events, cls.stand = parse_timetable(cls.html)

    def test_reads_dates_and_events(self):
        self.assertGreaterEqual(len(self.events), 2)
        titles = {event["title"] for event in self.events}
        self.assertIn("Entrepreneurship & Innovationsfinanzierung (Frie)", titles)
        self.assertIn("Trendanalyse, Innovationsbewertung & Strategieentwicklung (Frie)", titles)

    def test_reads_time_and_location(self):
        event = next(e for e in self.events if e["title"].startswith("Entrepreneurship"))
        self.assertEqual(event["start"].strftime("%Y-%m-%d %H:%M"), "2026-10-12 08:15")
        self.assertEqual(event["end"].strftime("%Y-%m-%d %H:%M"), "2026-10-12 12:30")
        self.assertIn("Frie 17a", event["location"])
        self.assertEqual(event["site_code"], "Frie")
        self.assertEqual(event["source_title"], "Entrepreneurship & Innovationsfinanzierung")

    def test_source_stand_timestamp(self):
        self.assertIsNotNone(self.stand)
        self.assertTrue(self.stand.startswith("2026-10-12T07:05:00"))

    def test_ics_is_valid_shape_and_escapes_lines(self):
        ics = build_ics(self.events, self.stand)
        self.assertTrue(ics.startswith("BEGIN:VCALENDAR\r\n"))
        self.assertIn("BEGIN:VEVENT", ics)
        self.assertIn("DTSTART:20261012T061500Z", ics)  # Berlin is UTC+2 on this date.
        self.assertIn("END:VCALENDAR\r\n", ics)

    def test_mue_venue_code_is_appended_to_title(self):
        html = self.html.replace("WÜ - Frie 17a: F.0.11", "WÜ - Mü 12: F.0.11")
        events, _ = parse_timetable(html)
        event = next(e for e in events if e["source_title"].startswith("Entrepreneurship"))
        self.assertEqual(event["title"], "Entrepreneurship & Innovationsfinanzierung (Mü)")
        self.assertEqual(event["site_code"], "Mü")

    def test_cancelled_event_is_excluded_from_the_feed(self):
        html = self.html.replace(
            "seminaristischer Unterricht / Übung",
            "seminaristischer Unterricht / Übung<br>Diese Veranstaltung entfällt",
            1,
        )
        events, _ = parse_timetable(html)
        titles = {event["source_title"] for event in events}
        self.assertNotIn("Entrepreneurship & Innovationsfinanzierung", titles)
        self.assertIn("Trendanalyse, Innovationsbewertung & Strategieentwicklung", titles)

    def test_struck_through_event_is_excluded(self):
        html = self.html.replace(
            "Entrepreneurship &amp; Innovationsfinanzierung [M2IV]",
            "<del>Entrepreneurship &amp; Innovationsfinanzierung [M2IV]</del>",
            1,
        )
        events, _ = parse_timetable(html)
        self.assertFalse(any(e["source_title"].startswith("Entrepreneurship") for e in events))

    def test_uid_stays_stable_if_venue_code_changes(self):
        html_mue = self.html.replace("WÜ - Frie 17a: F.0.11", "WÜ - Mü 12: F.0.11")
        events_frie, stand_frie = parse_timetable(self.html)
        events_mue, stand_mue = parse_timetable(html_mue)
        title = "Entrepreneurship & Innovationsfinanzierung"
        uid_frie = next(
            line for line in build_ics(events_frie, stand_frie).splitlines()
            if line.startswith("UID:")
        )
        uid_mue = next(
            line for line in build_ics(events_mue, stand_mue).splitlines()
            if line.startswith("UID:")
        )
        self.assertEqual(uid_frie, uid_mue)


if __name__ == "__main__":
    unittest.main()
