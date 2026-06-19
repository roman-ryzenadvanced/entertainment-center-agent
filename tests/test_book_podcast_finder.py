#!/usr/bin/env python3
"""Tests for book_podcast_finder.py"""

import unittest
import sys
import os
import subprocess
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

import book_podcast_finder as bpf

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'book_podcast_finder.py')


class TestBookPodcastData(unittest.TestCase):
    """Test built-in data structures."""

    def test_books_not_empty(self):
        self.assertGreater(len(bpf.BOOKS), 0)

    def test_podcasts_not_empty(self):
        self.assertGreater(len(bpf.PODCASTS), 0)

    def test_each_book_has_required_keys(self):
        required = {"title", "author", "platform", "format", "desc", "link", "pages"}
        for genre, books in bpf.BOOKS.items():
            for b in books:
                self.assertEqual(set(b.keys()), required,
                                 f"Book '{b.get('title')}' in genre '{genre}' missing keys")

    def test_each_podcast_has_required_keys(self):
        required = {"name", "platform", "desc", "link", "type"}
        for genre, pods in bpf.PODCASTS.items():
            for p in pods:
                self.assertEqual(set(p.keys()), required,
                                 f"Podcast '{p.get('name')}' in genre '{genre}' missing keys")

    def test_genre_aliases_has_common_aliases(self):
        self.assertIn("scifi", bpf.GENRE_ALIASES)
        self.assertIn("horror", bpf.GENRE_ALIASES)


class TestNormalizeGenre(unittest.TestCase):
    """Test genre normalization."""

    def test_sci_fi_alias(self):
        self.assertEqual(bpf.normalize_genre("sci-fi"), "science-fiction")

    def test_scifi_alias(self):
        self.assertEqual(bpf.normalize_genre("scifi"), "science-fiction")

    def test_mystery_alias(self):
        self.assertEqual(bpf.normalize_genre("crime"), "mystery")

    def test_unknown_genre_passthrough(self):
        self.assertEqual(bpf.normalize_genre("totallyunknown"), "totallyunknown")

    def test_case_insensitive(self):
        self.assertEqual(bpf.normalize_genre("SCIFI"), "science-fiction")

    def test_whitespace_handling(self):
        self.assertEqual(bpf.normalize_genre("  scifi  "), "science-fiction")


class TestGeneratePlan(unittest.TestCase):
    """Test the generate_plan function."""

    def test_default_genres(self):
        genres = ["science-fiction", "classic-literature", "history"]
        result = bpf.generate_plan(genres=genres)
        self.assertIsInstance(result, str)
        self.assertIn("Books & Podcasts Discovery Guide", result)

    def test_plan_has_book_sources(self):
        result = bpf.generate_plan(genres=["science-fiction"])
        self.assertIn("Free Book Sources", result)
        self.assertIn("Project Gutenberg", result)
        self.assertIn("Open Library", result)

    def test_plan_has_podcast_sources(self):
        result = bpf.generate_plan(genres=["science"])
        self.assertIn("Free Podcast Sources", result)
        self.assertIn("Spotify", result)

    def test_plan_has_weekly_schedule(self):
        result = bpf.generate_plan(genres=["history"])
        self.assertIn("Weekly Reading", result)
        self.assertIn("Monday", result)
        self.assertIn("Sunday", result)

    def test_plan_has_book_recommendations(self):
        result = bpf.generate_plan(genres=["science-fiction"])
        self.assertIn("Book Recommendations", result)
        self.assertIn("War of the Worlds", result)

    def test_plan_has_podcast_recommendations(self):
        result = bpf.generate_plan(genres=["true-crime"])
        self.assertIn("Podcast Recommendations", result)

    def test_unknown_genres_fallback(self):
        result = bpf.generate_plan(genres=["notarealgenre12345"])
        # Should fall back to defaults
        self.assertIn("Book Recommendations", result)
        self.assertIn("Podcast Recommendations", result)

    def test_genre_alias_resolution(self):
        result = bpf.generate_plan(genres=["scifi"])
        self.assertIn("Science Fiction", result)


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
            self.assertIn("Books & Podcasts", content)
        finally:
            os.unlink(path)

    def test_cli_with_genres(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path,
                 "--genres", "science-fiction,history,comedy"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("Science Fiction", content)
            self.assertIn("History", content)
        finally:
            os.unlink(path)

    def test_cli_with_genre_aliases(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path, "--genres", "scifi,mystery"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        finally:
            os.unlink(path)


if __name__ == '__main__':
    unittest.main()