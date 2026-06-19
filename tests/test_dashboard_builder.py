#!/usr/bin/env python3
"""Tests for dashboard_builder.py"""

import unittest
import sys
import os
import subprocess
import tempfile
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

import dashboard_builder as db

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'dashboard_builder.py')


class TestDashboardBuilderData(unittest.TestCase):
    """Test the built-in data structures."""

    def test_categories_has_8_entries(self):
        self.assertEqual(len(db.CATEGORIES), 8)

    def test_category_names(self):
        expected = {"Movies", "TV Shows", "Music", "Podcasts", "Books", "Games", "Documentaries", "Learning"}
        self.assertEqual(set(db.CATEGORIES.keys()), expected)

    def test_each_category_has_at_least_5_platforms(self):
        for name, data in db.CATEGORIES.items():
            self.assertGreaterEqual(len(data["platforms"]), 5, f"{name} has fewer than 5 platforms")

    def test_each_category_has_emoji(self):
        for name, data in db.CATEGORIES.items():
            self.assertIn("emoji", data, f"{name} missing emoji")

    def test_each_platform_has_name_url_description(self):
        for cat_name, cat_data in db.CATEGORIES.items():
            for p in cat_data["platforms"]:
                self.assertIn("name", p, f"{cat_name} platform missing name")
                self.assertIn("url", p, f"{cat_name} platform missing url")
                self.assertIn("description", p, f"{cat_name} platform missing description")
                self.assertTrue(p["url"].startswith("http"), f"{p['name']} URL invalid: {p['url']}")


class TestGenerateHTML(unittest.TestCase):
    """Test HTML generation."""

    def test_generate_html_returns_string(self):
        result = db.generate_html()
        self.assertIsInstance(result, str)

    def test_html_contains_doctype(self):
        result = db.generate_html()
        self.assertIn("<!DOCTYPE html>", result)

    def test_html_contains_all_category_names(self):
        result = db.generate_html()
        for cat_name in db.CATEGORIES:
            self.assertIn(cat_name, result, f"Missing category: {cat_name}")

    def test_html_contains_css(self):
        result = db.generate_html()
        self.assertIn("<style>", result)
        self.assertIn("</style>", result)

    def test_html_with_preferences_highlights_categories(self):
        result = db.generate_html(preferences=["movies", "music"])
        self.assertIn("highlighted", result)
        self.assertIn("movies", result)

    def test_html_contains_links(self):
        result = db.generate_html()
        self.assertIn('href="https://tubitv.com"', result)


class TestGenerateMarkdown(unittest.TestCase):
    """Test Markdown generation."""

    def test_generate_markdown_returns_string(self):
        result = db.generate_markdown()
        self.assertIsInstance(result, str)

    def test_markdown_has_h1_title(self):
        result = db.generate_markdown()
        self.assertTrue(re.search(r"^# .+Entertainment", result, re.MULTILINE))

    def test_markdown_contains_all_categories(self):
        result = db.generate_markdown()
        for cat_name in db.CATEGORIES:
            self.assertIn(f"## {db.CATEGORIES[cat_name]['emoji']} {cat_name}", result)

    def test_markdown_with_preferences(self):
        result = db.generate_markdown(preferences=["games"])
        self.assertIn("Highlighted", result)
        self.assertIn("games", result)


class TestCLI(unittest.TestCase):
    """Test command-line interface via subprocess."""

    def test_cli_html_output_created(self):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path, "--format", "html"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            self.assertTrue(os.path.exists(path))
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("<!DOCTYPE html>", content)
        finally:
            os.unlink(path)

    def test_cli_markdown_output_created(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path, "--format", "markdown"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            self.assertTrue(os.path.exists(path))
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("#", content)
        finally:
            os.unlink(path)

    def test_cli_preferences_flag(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path, "--format", "markdown",
                 "--preferences", "movies,music,games"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("Highlighted", content)
            self.assertIn("movies", content)
            self.assertIn("music", content)
            self.assertIn("games", content)
        finally:
            os.unlink(path)

    def test_cli_output_to_subdirectory(self):
        tmpdir = os.path.join("/tmp", "test_dash_subdir")
        path = os.path.join(tmpdir, "output.md")
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path, "--format", "markdown"],
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