#!/usr/bin/env python3
"""Tests for learning_curator.py"""

import unittest
import sys
import os
import subprocess
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

import learning_curator as lc

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'learning_curator.py')


class TestLearningCuratorData(unittest.TestCase):
    """Test built-in data structures."""

    def test_documentaries_not_empty(self):
        self.assertGreater(len(lc.DOCUMENTARIES), 0)

    def test_courses_not_empty(self):
        self.assertGreater(len(lc.COURSES), 0)

    def test_topic_aliases_has_common_aliases(self):
        self.assertIn("coding", lc.TOPIC_ALIASES)
        self.assertEqual(lc.TOPIC_ALIASES["coding"], "programming")
        self.assertIn("physics", lc.TOPIC_ALIASES)
        self.assertEqual(lc.TOPIC_ALIASES["physics"], "science")

    def test_learning_platforms_not_empty(self):
        self.assertGreater(len(lc.LEARNING_PLATFORMS), 0)

    def test_each_documentary_has_required_keys(self):
        required = {"title", "platform", "duration", "desc", "url", "subtopics"}
        for topic, docs in lc.DOCUMENTARIES.items():
            for d in docs:
                self.assertEqual(set(d.keys()), required,
                                 f"Doc '{d.get('title')}' in topic '{topic}' missing keys")

    def test_each_course_has_required_keys(self):
        required = {"title", "provider", "duration", "level", "desc", "url", "path"}
        for topic, courses in lc.COURSES.items():
            for c in courses:
                self.assertEqual(set(c.keys()), required,
                                 f"Course '{c.get('title')}' in topic '{topic}' missing keys")

    def test_week_schedule_has_7_days(self):
        self.assertEqual(len(lc.WEEK_SCHEDULE), 7)


class TestGeneratePlan(unittest.TestCase):
    """Test the generate_plan function."""

    def test_default_plan(self):
        result = lc.generate_plan(topics=["science", "history"], level="beginner")
        self.assertIsInstance(result, str)
        self.assertIn("Documentary & Learning Plan", result)

    def test_plan_has_learning_platforms(self):
        result = lc.generate_plan(topics=["science"], level="beginner")
        self.assertIn("Free Learning Platforms", result)
        self.assertIn("Khan Academy", result)

    def test_plan_has_documentary_recommendations(self):
        result = lc.generate_plan(topics=["science", "history"], level="beginner")
        self.assertIn("Documentary Recommendations", result)

    def test_plan_has_course_recommendations(self):
        result = lc.generate_plan(topics=["programming"], level="beginner")
        self.assertIn("Free Course Recommendations", result)

    def test_plan_has_weekly_schedule(self):
        result = lc.generate_plan(topics=["science"], level="beginner")
        self.assertIn("Weekly Learning Schedule", result)
        self.assertIn("Monday", result)
        self.assertIn("Sunday", result)

    def test_plan_has_tips(self):
        result = lc.generate_plan(topics=["science"], level="beginner")
        self.assertIn("Learning Tips", result)

    def test_level_filtering(self):
        result = lc.generate_plan(topics=["programming"], level="advanced")
        self.assertIn("Advanced", result)

    def test_topic_aliases(self):
        result = lc.generate_plan(topics=["coding", "physics"], level="beginner")
        # coding -> programming, physics -> science
        self.assertIn("Programming", result)
        self.assertIn("Science", result)

    def test_unknown_topics_fallback(self):
        result = lc.generate_plan(topics=["notarealtopic"], level="beginner")
        # Should use defaults and still produce output
        self.assertIn("Documentary & Learning Plan", result)

    def test_plan_has_progression_paths(self):
        result = lc.generate_plan(topics=["programming"], level="beginner")
        self.assertIn("Progression Path", result)


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
            self.assertIn("Documentary & Learning Plan", content)
        finally:
            os.unlink(path)

    def test_cli_with_topics(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
            path = f.name
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path,
                 "--topics", "history,science,programming", "--level", "intermediate"],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            with open(path, "r") as fh:
                content = fh.read()
            self.assertIn("Intermediate", content)
        finally:
            os.unlink(path)

    def test_cli_all_levels(self):
        for level in ["beginner", "intermediate", "advanced"]:
            with tempfile.NamedTemporaryFile(suffix=".md", delete=False, dir="/tmp") as f:
                path = f.name
            try:
                result = subprocess.run(
                    ["python3", SCRIPT_PATH, "--output", path,
                     "--topics", "science", "--level", level],
                    capture_output=True, text=True, timeout=30
                )
                self.assertEqual(result.returncode, 0,
                                 f"Level '{level}' failed: {result.stderr}")
            finally:
                os.unlink(path)

    def test_cli_output_to_subdirectory(self):
        tmpdir = os.path.join("/tmp", "test_learning_subdir")
        path = os.path.join(tmpdir, "learn.md")
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--output", path, "--topics", "science"],
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