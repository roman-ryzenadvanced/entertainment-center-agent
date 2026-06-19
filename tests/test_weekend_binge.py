#!/usr/bin/env python3
"""Tests for weekend_binge.py"""

import unittest
import sys
import os
import subprocess
import tempfile
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

import weekend_binge as wb

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'weekend_binge.py')


class TestWeekendBingeData(unittest.TestCase):
    """Test built-in data structures."""

    def test_morning_activities_not_empty(self):
        self.assertGreater(len(wb.MORNING_ACTIVITIES), 0)

    def test_afternoon_activities_not_empty(self):
        self.assertGreater(len(wb.AFTERNOON_ACTIVITIES), 0)

    def test_evening_activities_not_empty(self):
        self.assertGreater(len(wb.EVENING_ACTIVITIES), 0)

    def test_each_activity_has_required_keys(self):
        required = {"type", "emoji", "title", "desc", "duration", "platform", "search", "link"}
        for pool in [wb.MORNING_ACTIVITIES, wb.AFTERNOON_ACTIVITIES, wb.EVENING_ACTIVITIES]:
            for act in pool:
                self.assertEqual(set(act.keys()), required,
                                 f"Activity '{act.get('title')}' missing keys")

    def test_block_times(self):
        self.assertIn("morning", wb.BLOCK_TIMES)
        self.assertIn("afternoon", wb.BLOCK_TIMES)
        self.assertIn("evening", wb.BLOCK_TIMES)

    def test_interest_to_type_has_common_interests(self):
        for interest in ["movies", "games", "podcasts", "reading"]:
            self.assertIn(interest, wb.INTEREST_TO_TYPE)


class TestSelectActivities(unittest.TestCase):
    """Test the select_activities function."""

    def test_returns_list(self):
        result = wb.select_activities(wb.MORNING_ACTIVITIES, ["movie"], 6)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_prefers_matching_types(self):
        result = wb.select_activities(wb.MORNING_ACTIVITIES, ["podcast"], 6)
        types = [a["type"] for a in result]
        self.assertIn("podcast", types)

    def test_no_preference_still_returns_activities(self):
        result = wb.select_activities(wb.AFTERNOON_ACTIVITIES, None, 8)
        self.assertEqual(len(result), 2)


class TestGeneratePlan(unittest.TestCase):
    """Test the generate_plan function."""

    def test_default_plan(self):
        result = wb.generate_plan(hours=12, interests=None)
        self.assertIsInstance(result, str)
        self.assertIn("Weekend Binge Plan", result)

    def test_plan_has_saturday_and_sunday(self):
        result = wb.generate_plan(hours=12, interests=None)
        self.assertIn("Saturday", result)
        self.assertIn("Sunday", result)

    def test_plan_has_time_blocks(self):
        result = wb.generate_plan(hours=12, interests=None)
        self.assertIn("Morning", result)
        self.assertIn("Afternoon", result)
        self.assertIn("Evening", result)

    def test_plan_with_interests(self):
        result = wb.generate_plan(hours=14, interests=["movies", "games"])
        self.assertIn("movies", result)
        self.assertIn("games", result)
        self.assertIn("Your Interests", result)

    def test_plan_has_platform_links(self):
        result = wb.generate_plan(hours=12, interests=None)
        self.assertIn("Quick Platform Links", result)
        self.assertIn("Tubi", result)
        self.assertIn("YouTube", result)

    def test_plan_has_tips(self):
        result = wb.generate_plan(hours=12, interests=None)
        self.assertIn("Weekend Binge Tips", result)

    def test_plan_has_duration_info(self):
        result = wb.generate_plan(hours=12, interests=None)
        self.assertIn("minutes", result)

    def test_plan_total_hours_calculated(self):
        result = wb.generate_plan(hours=16, interests=None)
        # Should show total hours
        self.assertTrue(re.search(r"\d+\.\d+ hours", result))


class TestCLI(unittest.TestCase):
    """Test command-line interface."""

    def test_cli_default(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            self.assertTrue(os.path.exists(path))
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("Weekend Binge Plan", content)
        finally:
            os.unlink(path)

    def test_cli_with_interests(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path,
                 "--hours", "16", "--interests", "movies,games,podcasts"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("movies", content)
        finally:
            os.unlink(path)

    def test_cli_invalid_hours_too_low(self):
        result = subprocess.run(
            ["python3", SCRIPT_PATH, "--hours", "1", "--output", "/tmp/test_wb_low.md"],
            capture_output=True, text=True, timeout=30
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())

    def test_cli_invalid_hours_too_high(self):
        result = subprocess.run(
            ["python3", SCRIPT_PATH, "--hours", "100", "--output", "/tmp/test_wb_high.md"],
            capture_output=True, text=True, timeout=30
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())


if __name__ == '__main__':
    unittest.main()