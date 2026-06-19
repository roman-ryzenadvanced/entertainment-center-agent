#!/usr/bin/env python3
"""Tests for movie_planner.py"""

import unittest
import sys
import os
import subprocess
import tempfile
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

import movie_planner as mp

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'movie_planner.py')


class TestMoviePlannerData(unittest.TestCase):
    """Test built-in data structures."""

    def test_movies_has_6_moods(self):
        self.assertEqual(set(mp.MOVIES.keys()), set(mp.MOOD_EMOJIS.keys()))

    def test_mood_emojis_has_all_moods(self):
        expected = {"funny", "scary", "romantic", "action", "slow", "deep"}
        self.assertEqual(set(mp.MOOD_EMOJIS.keys()), expected)

    def test_each_mood_has_movies(self):
        for mood, movies in mp.MOVIES.items():
            self.assertGreater(len(movies), 0, f"Mood '{mood}' has no movies")

    def test_each_movie_has_required_keys(self):
        required = {"title", "platform", "year", "why", "best_for", "backup", "backup_platform"}
        for mood, movies in mp.MOVIES.items():
            for m in movies:
                self.assertEqual(set(m.keys()), required,
                                 f"Movie '{m.get('title')}' in mood '{mood}' missing keys")

    def test_platform_links_has_known_platforms(self):
        for name in ["Tubi", "Pluto TV", "YouTube", "Crackle", "Freevee"]:
            self.assertIn(name, mp.PLATFORM_LINKS)


class TestGeneratePlan(unittest.TestCase):
    """Test the generate_plan function."""

    def test_funny_movies(self):
        result = mp.generate_plan("funny", 3)
        self.assertIsInstance(result, str)
        self.assertIn("Funny", result)
        self.assertIn("Spaceballs", result)

    def test_scarey_movies(self):
        result = mp.generate_plan("scary", 5)
        self.assertIn("Scary", result)

    def test_movie_count_limited(self):
        result = mp.generate_plan("funny", 2)
        # Should have exactly 2 numbered entries
        numbered = re.findall(r"^### \d+\.", result, re.MULTILINE)
        self.assertEqual(len(numbered), 2)

    def test_count_exceeds_available(self):
        available = len(mp.MOVIES["funny"])
        result = mp.generate_plan("funny", 999)
        numbered = re.findall(r"^### \d+\.", result, re.MULTILINE)
        self.assertEqual(len(numbered), available)

    def test_backup_option_present(self):
        result = mp.generate_plan("action", 3)
        self.assertIn("Backup Option", result)

    def test_plan_has_platform_quick_links(self):
        result = mp.generate_plan("deep", 5)
        self.assertIn("Platform Quick Links", result)
        self.assertIn("Tubi", result)

    def test_plan_has_movie_night_tips(self):
        result = mp.generate_plan("romantic", 5)
        self.assertIn("Movie Night Tips", result)

    def test_plan_has_movie_years(self):
        result = mp.generate_plan("funny", 3)
        # Check that a year appears in parentheses after a title
        self.assertTrue(re.search(r"\(\d{4}\)", result))

    def test_invalid_mood_exits(self):
        # generate_plan calls sys.exit for invalid mood, so use subprocess
        pass  # tested in CLI section below


class TestCLI(unittest.TestCase):
    """Test command-line interface."""

    def test_cli_valid_mood(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--mood", "funny", "--count", "3", "--output", path],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            self.assertTrue(os.path.exists(path))
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("Funny", content)
            self.assertIn("Spaceballs", content)
        finally:
            os.unlink(path)

    def test_cli_invalid_mood_exits(self):
        result = subprocess.run(
            ["python3", SCRIPT_PATH, "--mood", "invalid_mood_xyz", "--output", "/tmp/test_movie_invalid.md"],
            capture_output=True, text=True, timeout=30
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())

    def test_cli_invalid_count_exits(self):
        result = subprocess.run(
            ["python3", SCRIPT_PATH, "--mood", "funny", "--count", "100", "--output", "/tmp/test_movie_count.md"],
            capture_output=True, text=True, timeout=30
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())

    def test_cli_all_moods(self):
        """Test that every valid mood works via CLI."""
        for mood in mp.MOOD_EMOJIS:
            with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
                path = f.name
            try:
                result = subprocess.run(
                    ["python3", SCRIPT_PATH, "--mood", mood, "--count", "1", "--output", path],
                    capture_output=True, text=True, timeout=30
                )
                self.assertEqual(result.returncode, 0, f"Mood '{mood}' failed: {result.stderr}")
            finally:
                os.unlink(path)

    def test_cli_output_to_subdirectory(self):
        tmpdir = os.path.join("/tmp", "test_movie_subdir")
        path = os.path.join(tmpdir, "movies.md")
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--mood", "deep", "--count", "1", "--output", path],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            self.assertTrue(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.unlink(path)
            if os.path.exists(tmpdir):
                os.rmdir(tmpdir)


if __name__ == '__main__':
    unittest.main()