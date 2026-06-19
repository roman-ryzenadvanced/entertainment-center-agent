#!/usr/bin/env python3
"""Tests for youtube_programmer.py"""

import unittest
import sys
import os
import subprocess
import tempfile
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

import youtube_programmer as yp

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'youtube_programmer.py')


class TestYouTubeProgrammerData(unittest.TestCase):
    """Test built-in data structures."""

    def test_channel_data_has_categories(self):
        self.assertGreater(len(yp.CHANNEL_DATA), 0)

    def test_each_category_has_channels(self):
        for cat, data in yp.CHANNEL_DATA.items():
            self.assertGreater(len(data["channels"]), 0, f"Category '{cat}' has no channels")

    def test_each_category_has_emoji(self):
        for cat, data in yp.CHANNEL_DATA.items():
            self.assertIn("emoji", data, f"Category '{cat}' missing emoji")

    def test_time_blocks_has_3_blocks(self):
        self.assertEqual(len(yp.TIME_BLOCKS), 3)
        self.assertIn("morning", yp.TIME_BLOCKS)
        self.assertIn("afternoon", yp.TIME_BLOCKS)
        self.assertIn("evening", yp.TIME_BLOCKS)

    def test_day_names_has_7_days(self):
        self.assertEqual(len(yp.DAY_NAMES), 7)

    def test_trending_topics_not_empty(self):
        self.assertGreater(len(yp.TRENDING_TOPICS), 0)


class TestGenerateSchedule(unittest.TestCase):
    """Test the generate_schedule function."""

    def test_default_schedule(self):
        cats = list(yp.CHANNEL_DATA.keys())[:4]
        result = yp.generate_schedule(categories=cats, days=7)
        self.assertIsInstance(result, str)
        self.assertIn("Personal YouTube Network", result)

    def test_schedule_has_all_days(self):
        result = yp.generate_schedule(categories=["documentaries", "comedy"], days=7)
        for day in yp.DAY_NAMES:
            self.assertIn(day, result)

    def test_schedule_has_time_blocks(self):
        result = yp.generate_schedule(categories=["tech", "food"], days=1)
        self.assertIn("Morning", result)
        self.assertIn("Afternoon", result)
        self.assertIn("Evening", result)

    def test_schedule_has_deep_dives(self):
        result = yp.generate_schedule(categories=["documentaries"], days=1)
        self.assertIn("Category Deep Dives", result)

    def test_schedule_has_trending(self):
        result = yp.generate_schedule(categories=["comedy"], days=1)
        self.assertIn("Trending", result)

    def test_14_day_schedule(self):
        result = yp.generate_schedule(categories=["tech"], days=14)
        self.assertIn("Week 1", result)
        self.assertIn("Week 2", result)

    def test_network_channels_table(self):
        result = yp.generate_schedule(categories=["documentaries", "tech"], days=1)
        self.assertIn("Network Channels", result)
        self.assertIn("| Category | Channels |", result)

    def test_single_day_schedule(self):
        result = yp.generate_schedule(categories=["cozy"], days=1)
        self.assertIn("Monday", result)
        self.assertNotIn("Week", result)


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
            self.assertIn("YouTube Network", content)
        finally:
            os.unlink(path)

    def test_cli_with_categories(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path,
                 "--categories", "documentaries,comedy,tech", "--days", "3"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("Documentaries", content)
            self.assertIn("Comedy", content)
            self.assertIn("Tech", content)
        finally:
            os.unlink(path)

    def test_cli_invalid_days_exits(self):
        result = subprocess.run(
            ["python3", SCRIPT_PATH, "--days", "50", "--output", "/tmp/test_yt_days.md"],
            capture_output=True, text=True, timeout=30
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())

    def test_cli_unknown_category_warning(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path,
                 "--categories", "documentaries,notarealcategory123"],
                capture_output=True, text=True, timeout=30
            )
            # Should still succeed but with a warning
            self.assertEqual(result.returncode, 0)
            self.assertIn("Unknown categories", result.stderr)
        finally:
            os.unlink(path)


if __name__ == '__main__':
    unittest.main()