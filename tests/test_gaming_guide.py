#!/usr/bin/env python3
"""Tests for gaming_guide.py"""

import unittest
import sys
import os
import subprocess
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

import gaming_guide as gg

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'gaming_guide.py')


class TestGamingGuideData(unittest.TestCase):
    """Test built-in data structures."""

    def test_games_not_empty(self):
        self.assertGreater(len(gg.GAMES), 0)

    def test_known_genres_exist(self):
        for genre in ["puzzle", "rpg", "strategy", "action", "adventure", "simulation", "cozy"]:
            self.assertIn(genre, gg.GAMES, f"Missing genre: {genre}")

    def test_each_game_has_required_keys(self):
        required = {"title", "platforms", "difficulty", "time", "why", "url"}
        for genre, games in gg.GAMES.items():
            for g in games:
                self.assertEqual(set(g.keys()), required,
                                 f"Game '{g.get('title')}' in genre '{genre}' missing keys")

    def test_platform_data_has_required_platforms(self):
        for key in ["pc", "mac", "mobile", "browser"]:
            self.assertIn(key, gg.PLATFORM_DATA, f"Missing platform: {key}")

    def test_each_game_has_platforms_list(self):
        for genre, games in gg.GAMES.items():
            for g in games:
                self.assertIsInstance(g["platforms"], list)
                self.assertGreater(len(g["platforms"]), 0)

    def test_platform_links_not_empty(self):
        self.assertGreater(len(gg.PLATFORM_LINKS), 0)


class TestGenerateGuide(unittest.TestCase):
    """Test the generate_guide function."""

    def test_pc_default_genres(self):
        genres = list(gg.GAMES.keys())
        result = gg.generate_guide(platform="pc", genres=genres)
        self.assertIsInstance(result, str)
        self.assertIn("Free Gaming Guide", result)

    def test_guide_has_platform_section(self):
        result = gg.generate_guide(platform="browser", genres=["puzzle"])
        self.assertIn("Your Platform", result)
        self.assertIn("Browser", result)

    def test_guide_has_game_recommendations(self):
        result = gg.generate_guide(platform="pc", genres=["puzzle", "rpg"])
        self.assertIn("Game Recommendations", result)
        self.assertIn("Puzzle", result)

    def test_browser_filter(self):
        result = gg.generate_guide(platform="browser", genres=["puzzle"])
        # Browser games should include "Browser" in their platforms
        lines = result.split("\n")
        # Check that at least some content is present
        self.assertIn("Puzzle", result)

    def test_guide_has_weekly_schedule(self):
        result = gg.generate_guide(platform="pc", genres=["rpg"])
        self.assertIn("Weekly Gaming Schedule", result)
        self.assertIn("Monday", result)

    def test_guide_has_gaming_tips(self):
        result = gg.generate_guide(platform="pc", genres=["action"])
        self.assertIn("Free Gaming Tips", result)

    def test_guide_has_all_platform_links(self):
        result = gg.generate_guide(platform="pc", genres=["puzzle"])
        self.assertIn("All Free Gaming Platforms", result)
        self.assertIn("itch.io", result)
        self.assertIn("Steam", result)

    def test_unknown_genres_fallback(self):
        result = gg.generate_guide(platform="pc", genres=["notarealgenre"])
        # Should still produce output using all genres
        self.assertIn("Free Gaming Guide", result)


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
            self.assertIn("Free Gaming Guide", content)
        finally:
            os.unlink(path)

    def test_cli_browser_platform(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--platform", "browser",
                 "--genres", "puzzle,action", "--output", path],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("Browser", content)
        finally:
            os.unlink(path)

    def test_cli_unknown_genres_warning(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path,
                 "--genres", "puzzle,notarealgenre"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Unknown genres", result.stderr)
        finally:
            os.unlink(path)

    def test_cli_output_to_subdirectory(self):
        tmpdir = os.path.join("/tmp", "test_gaming_subdir")
        path = os.path.join(tmpdir, "games.md")
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path, "--genres", "puzzle"],
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