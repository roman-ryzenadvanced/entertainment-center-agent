#!/usr/bin/env python3
"""Tests for the platforms.md reference database.

Reads and parses references/platforms.md to verify:
- All 8 categories exist
- Each category has at least 5 platforms
- Platform URLs look valid
- Data consistency across the file
"""

import unittest
import os
import re

# Path to the platforms reference file
PLATFORMS_MD = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'references', 'platforms.md'
)


def parse_platforms_md(filepath):
    """Parse platforms.md and return a dict of category -> list of platform dicts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    categories = {}
    current_category = None
    current_rows = []

    for line in content.split('\n'):
        # Match ## heading for categories (but not subsections like ###)
        h2_match = re.match(r'^## (.+)$', line)
        if h2_match:
            # Save previous category
            if current_category and current_rows:
                categories[current_category] = current_rows
            cat_name = h2_match.group(1).strip()
            # Skip non-category headings like "Platform Quality Ratings"
            if cat_name in ("Platform Quality Ratings",):
                current_category = None
                continue
            current_category = cat_name
            current_rows = []
            continue

        # Match table rows (skip header/separator)
        if current_category and line.startswith('|') and '---' not in line and 'Platform' not in line:
            cells = [c.strip() for c in line.split('|')]
            # Remove empty first and last elements from split
            cells = [c for c in cells if c]
            if len(cells) >= 2:
                row = {"name": cells[0], "url": cells[1] if len(cells) > 1 else ""}
                if len(cells) > 2:
                    row["best_for"] = cells[2]
                if len(cells) > 3:
                    row["content_type"] = cells[3]
                if len(cells) > 4:
                    row["extra"] = cells[4]
                current_rows.append(row)

    # Save last category
    if current_category and current_rows:
        categories[current_category] = current_rows

    return categories


class TestPlatformsMDBasicParsing(unittest.TestCase):
    """Test that we can parse the markdown file."""

    def test_file_exists(self):
        self.assertTrue(os.path.exists(PLATFORMS_MD),
                        f"platforms.md not found at {PLATFORMS_MD}")

    def test_file_not_empty(self):
        with open(PLATFORMS_MD, 'r') as f:
            content = f.read()
        self.assertGreater(len(content), 100)

    def test_parsing_returns_dict(self):
        categories = parse_platforms_md(PLATFORMS_MD)
        self.assertIsInstance(categories, dict)


class TestPlatformsMDCategories(unittest.TestCase):
    """Test that all 8 expected categories exist."""

    EXPECTED_CATEGORIES = [
        "Movies", "TV Shows", "Music", "Podcasts",
        "Books", "Games", "Documentaries", "Learning"
    ]

    @classmethod
    def setUpClass(cls):
        cls.categories = parse_platforms_md(PLATFORMS_MD)

    def test_has_8_categories(self):
        self.assertEqual(len(self.categories), 8,
                         f"Expected 8 categories, got: {list(self.categories.keys())}")

    def test_movies_category_exists(self):
        self.assertIn("Movies", self.categories)

    def test_tv_shows_category_exists(self):
        self.assertIn("TV Shows", self.categories)

    def test_music_category_exists(self):
        self.assertIn("Music", self.categories)

    def test_podcasts_category_exists(self):
        self.assertIn("Podcasts", self.categories)

    def test_books_category_exists(self):
        self.assertIn("Books", self.categories)

    def test_games_category_exists(self):
        self.assertIn("Games", self.categories)

    def test_documentaries_category_exists(self):
        self.assertIn("Documentaries", self.categories)

    def test_learning_category_exists(self):
        self.assertIn("Learning", self.categories)


class TestPlatformsMDPlatformCount(unittest.TestCase):
    """Test that each category has at least 5 platforms."""

    @classmethod
    def setUpClass(cls):
        cls.categories = parse_platforms_md(PLATFORMS_MD)

    def test_movies_at_least_5(self):
        self.assertGreaterEqual(len(self.categories["Movies"]), 5)

    def test_tv_shows_at_least_5(self):
        self.assertGreaterEqual(len(self.categories["TV Shows"]), 5)

    def test_music_at_least_5(self):
        self.assertGreaterEqual(len(self.categories["Music"]), 5)

    def test_podcasts_at_least_5(self):
        self.assertGreaterEqual(len(self.categories["Podcasts"]), 5)

    def test_books_at_least_5(self):
        self.assertGreaterEqual(len(self.categories["Books"]), 5)

    def test_games_at_least_5(self):
        self.assertGreaterEqual(len(self.categories["Games"]), 5)

    def test_documentaries_at_least_5(self):
        self.assertGreaterEqual(len(self.categories["Documentaries"]), 5)

    def test_learning_at_least_5(self):
        self.assertGreaterEqual(len(self.categories["Learning"]), 5)

    def test_all_categories_at_least_5(self):
        for cat, platforms in self.categories.items():
            self.assertGreaterEqual(len(platforms), 5,
                                    f"Category '{cat}' has only {len(platforms)} platforms")


class TestPlatformsMDURLValidity(unittest.TestCase):
    """Test that platform URLs look valid."""

    URL_PATTERN = re.compile(
        r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$'
    )

    @classmethod
    def setUpClass(cls):
        cls.categories = parse_platforms_md(PLATFORMS_MD)

    def test_all_platforms_have_names(self):
        for cat, platforms in self.categories.items():
            for p in platforms:
                self.assertTrue(p["name"].strip(), f"Empty name in {cat}")

    def test_all_platforms_have_urls(self):
        for cat, platforms in self.categories.items():
            for p in platforms:
                self.assertTrue(p["url"].strip(), f"Empty URL for '{p['name']}' in {cat}")

    def test_urls_look_valid(self):
        for cat, platforms in self.categories.items():
            for p in platforms:
                url = p["url"]
                # Remove markdown link formatting if present
                url_clean = re.sub(r'\[.*?\]\((.*?)\)', r'\1', url)
                self.assertRegex(url_clean, self.URL_PATTERN,
                                 f"Invalid URL for '{p['name']}' in {cat}: {url_clean}")

    def test_no_duplicate_platform_names_within_category(self):
        for cat, platforms in self.categories.items():
            names = [p["name"].lower() for p in platforms]
            self.assertEqual(len(names), len(set(names)),
                             f"Duplicate platform names in '{cat}'")


class TestPlatformsMDConsistency(unittest.TestCase):
    """Test data consistency across the file."""

    @classmethod
    def setUpClass(cls):
        cls.categories = parse_platforms_md(PLATFORMS_MD)

    def test_total_platforms_reasonable(self):
        total = sum(len(p) for p in self.categories.values())
        # Should have at least 50 total platforms across 8 categories
        self.assertGreaterEqual(total, 50, f"Only {total} platforms total")

    def test_known_platforms_present(self):
        """Check that some well-known platforms appear."""
        all_names = set()
        for platforms in self.categories.values():
            for p in platforms:
                all_names.add(p["name"].lower())

        for expected in ["tubi", "youtube", "spotify", "project gutenberg", "itch.io",
                         "khan academy"]:
            found = any(expected in name for name in all_names)
            self.assertTrue(found, f"Expected platform '{expected}' not found")

    def test_file_has_quality_ratings_section(self):
        with open(PLATFORMS_MD, 'r') as f:
            content = f.read()
        self.assertIn("Platform Quality Ratings", content)

    def test_each_category_has_description_column(self):
        """Verify that at least the Movies table has a description/Best For column."""
        # Movies should have a "Best For" column (3rd column)
        movies = self.categories["Movies"]
        for p in movies:
            self.assertIn("best_for", p,
                          f"Movies table missing 'Best For' column for '{p['name']}'")


if __name__ == '__main__':
    unittest.main()