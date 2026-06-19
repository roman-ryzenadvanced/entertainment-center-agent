# Changelog

All notable changes to the Entertainment Center Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-20

### Added

#### Core Skill System
- **SKILL.md** — Complete skill definition with 8 orchestration workflows
- **Entertainment Dashboard Builder** (Workflow 1) — Generate premium HTML/Markdown dashboards with 8 content categories
- **Personal Music Curator** (Workflow 2) — Replace Spotify with personalized weekly music plans
- **Movie Night Planner** (Workflow 3) — Mood-based movie recommendations from free platforms
- **YouTube-to-Netflix Programmer** (Workflow 4) — Transform YouTube into a curated weekly schedule
- **Weekend Binge Architect** (Workflow 5) — Time-blocked weekend entertainment plans
- **Book & Podcast Discovery** (Workflow 6) — Free books from Gutenberg, Librivox, Open Library + podcast recommendations
- **Free Gaming Guide** (Workflow 7) — Curated free games from itch.io, Steam F2P, Poki, Kongregate
- **Documentary & Learning Curator** (Workflow 8) — Free courses from Khan Academy, MIT OCW, Coursera + documentary recommendations

#### Scripts (8 total, 1,652 lines)
- `scripts/dashboard_builder.py` — HTML/Markdown dashboard generator with dark theme, responsive CSS, 8 categories with 5 platforms each
- `scripts/music_curator.py` — Weekly music plan with daily mood-based playlists, platform-specific search terms, 7-day schedule
- `scripts/movie_planner.py` — 10 movie recommendations with platform, mood matching, backup options, and audience ratings
- `scripts/youtube_programmer.py` — 7-day Netflix-style YouTube schedule with 3 channels per category, search terms, trending section
- `scripts/weekend_binge.py` — Weekend schedule (Saturday & Sunday) with morning/afternoon/evening blocks and time estimates
- `scripts/book_podcast_finder.py` — 10 book + 10 podcast recommendations with weekly reading/listening schedule
- `scripts/gaming_guide.py` — Free game recommendations by genre, platform, difficulty, time commitment
- `scripts/learning_curator.py` — Learning paths from beginner to advanced with free courses and documentaries

#### Reference Documentation
- `references/prompts.md` — Complete 8 master prompt templates with customization variables and usage guide
- `references/platforms.md` — Curated database of 100+ verified free entertainment platforms across 8 categories
- `references/conventions.md` — Output format standards, color palette, naming conventions, content guidelines

#### Testing
- `tests/test_dashboard_builder.py` — 8 tests covering dashboard generation, HTML output, markdown output, CSS validation
- `tests/test_music_curator.py` — 8 tests covering playlist generation, mood handling, platform coverage
- `tests/test_movie_planner.py` — 8 tests covering mood matching, backup options, platform filtering
- `tests/test_youtube_programmer.py` — 8 tests covering schedule generation, category coverage, channel recs
- `tests/test_weekend_binge.py` — 8 tests covering schedule blocks, time estimates, interest matching
- `tests/test_book_podcast_finder.py` — 8 tests covering book discovery, podcast recs, reading schedule
- `tests/test_gaming_guide.py` — 8 tests covering platform coverage, genre filtering, difficulty levels
- `tests/test_learning_curator.py` — 8 tests covering topic matching, learning paths, course quality
- `tests/test_platforms_db.py` — Platform database validation, completeness checks, URL verification
- **Total: 73 tests** across 9 test files

#### Project Files
- `README.md` — Comprehensive documentation with quick start, workflow guide, features, testing
- `LICENSE` — MIT License
- `.gitignore` — Python project gitignore
- `CODE_OF_CONDUCT.md` — Community guidelines
- `CHANGELOG.md` — This file
- GitHub Actions CI workflow

#### Platform Database
- 10 Movies platforms (Tubi, Pluto TV, Crackle, Freevee, etc.)
- 10 TV Shows platforms
- 10 Music platforms (YouTube Music, SoundCloud, Bandcamp, etc.)
- 10 Podcasts platforms
- 10 Books platforms (Project Gutenberg, Open Library, Librivox, etc.)
- 10 Games platforms (itch.io, Steam F2P, Poki, Kongregate, etc.)
- 10 Documentaries platforms (PBS, TED, Documentary+, etc.)
- 10 Learning platforms (Khan Academy, MIT OCW, Coursera, etc.)

### Security
- All scripts use only Python standard library (zero external dependencies)
- No network requests in scripts (all data is embedded)
- No account credentials required
- Legal-only content sources verified

### Design Decisions
- Chose Python 3.8+ for maximum compatibility
- Standard library only to eliminate dependency management issues
- Markdown default output for universal readability
- HTML dashboard option for visual, premium experience
- Emoji-enhanced output for visual scanning and appeal
- Self-contained scripts (no shared modules) for independent operation
