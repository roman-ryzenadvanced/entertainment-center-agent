#!/usr/bin/env python3
"""Tests for music_curator.py"""

import unittest
import sys
import os
import subprocess
import tempfile
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

import music_curator as mc

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'music_curator.py')


class TestMusicCuratorData(unittest.TestCase):
    """Test built-in data structures."""

    def test_mood_schedule_has_7_days(self):
        self.assertEqual(len(mc.MOOD_SCHEDULE), 7)

    def test_all_days_present(self):
        expected = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        self.assertEqual(set(mc.MOOD_SCHEDULE.keys()), expected)

    def test_mood_playlists_has_7_entries(self):
        self.assertEqual(len(mc.MOOD_PLAYLISTS), 7)

    def test_each_mood_playlist_has_required_keys(self):
        required = {"emoji", "genres", "search_terms", "youtube_music_channels",
                     "soundcloud_artists", "bandcamp_recommendations", "tip"}
        for mood, data in mc.MOOD_PLAYLISTS.items():
            self.assertEqual(set(data.keys()), required, f"Mood '{mood}' missing keys")

    def test_genre_extras_is_not_empty(self):
        self.assertGreater(len(mc.GENRE_EXTRAS), 0)

    def test_artist_suggestions_has_known_artists(self):
        self.assertIn("tame impala", mc.ARTIST_SUGGESTIONS)
        self.assertIn("daft punk", mc.ARTIST_SUGGESTIONS)


class TestDiscoverArtist(unittest.TestCase):
    """Test artist discovery function."""

    def test_known_artist(self):
        result = mc.discover_artist("Tame Impala")
        self.assertIn("Pond", result)

    def test_known_artist_case_insensitive(self):
        result = mc.discover_artist("DAFT PUNK")
        self.assertIn("Justice", result)

    def test_unknown_artist(self):
        result = mc.discover_artist("Completely Unknown Band 12345")
        self.assertIn("Completely Unknown Band 12345", result)
        self.assertIn("SoundCloud", result)


class TestGeneratePlan(unittest.TestCase):
    """Test the generate_plan function."""

    def test_generate_default_plan(self):
        result = mc.generate_plan()
        self.assertIsInstance(result, str)
        self.assertIn("Weekly Music Plan", result)

    def test_plan_has_all_days(self):
        result = mc.generate_plan()
        for day in mc.MOOD_SCHEDULE:
            self.assertIn(day, result)

    def test_plan_with_artists(self):
        result = mc.generate_plan(artists=["Tame Impala", "Radiohead"])
        self.assertIn("Tame Impala", result)
        self.assertIn("Radiohead", result)
        self.assertIn("Artist Discovery", result)

    def test_plan_with_genres(self):
        result = mc.generate_plan(genres=["electronic", "rock"])
        self.assertIn("Genre Deep Dives", result)
        self.assertIn("Electronic", result)
        self.assertIn("Rock", result)

    def test_plan_with_moods(self):
        result = mc.generate_plan(moods=["focus", "chill"])
        self.assertIn("focus", result)
        self.assertIn("chill", result)

    def test_plan_has_mood_schedule_table(self):
        result = mc.generate_plan()
        self.assertIn("| Day | Mood |", result)
        self.assertIn("|-----|------|", result)

    def test_plan_has_platform_reference(self):
        result = mc.generate_plan()
        self.assertIn("YouTube Music", result)
        self.assertIn("SoundCloud", result)
        self.assertIn("Bandcamp", result)


class TestCLI(unittest.TestCase):
    """Test command-line interface."""

    def test_cli_default_output(self):
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
            self.assertIn("Weekly Music Plan", content)
        finally:
            os.unlink(path)

    def test_cli_with_all_options(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path,
                 "--artists", "Tame Impala", "--genres", "electronic",
                 "--moods", "focus,chill"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("Tame Impala", content)
            self.assertIn("Electronic", content)
        finally:
            os.unlink(path)

    def test_cli_output_contains_detailed_daily_playlists(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path],
                capture_output=True, text=True, timeout=30
            )
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("Detailed Daily Playlists", content)
            self.assertIn("Monday", content)
            self.assertIn("Sunday", content)
        finally:
            os.unlink(path)


if __name__ == '__main__':
    unittest.main()