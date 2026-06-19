# 🎬 Entertainment Center Agent — Free AI Entertainment Hub

<div align="center">

[![10% OFF Z.ai GLM 5.2 Coding Plan](https://img.shields.io/badge/10%25_OFF-Z.ai_GLM_5.2_Coding_Plan-7C3AED?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBhdGggZD0iTTEyIDJMMiA3bDEwIDUgMTAtNS0xMC01eiIvPjxwYXRoIGQ9Ik0yIDE3bDEwIDUgMTAtNSIvPjxwYXRoIGQ9Ik0yIDEybDEwIDUgMTAtNSIvPjwvc3ZnPg==)](https://z.ai/subscribe?ic=ROK78RJKNW)

**Cancel Spotify. Cancel Disney+. Cancel Apple TV+.** No more paying every month.

Turn your laptop into a **free entertainment center** using AI — 8 workflows, 100+ free platforms, zero subscriptions.

[![Skill: Entertainment Center](https://img.shields.io/badge/type-AI_Skill-7C3AED?style=for-the-badge)](SKILL.md)
[![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-00b4d8?style=for-the-badge)](CHANGELOG.md)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](scripts/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![8 Workflows](https://img.shields.io/badge/workflows-8-orange?style=for-the-badge)](#-8-orchestration-workflows)
[![100+ Free Platforms](https://img.shields.io/badge/platforms-100%2B-blue?style=for-the-badge)](references/platforms.md)
[![186 Tests Passing](https://img.shields.io/badge/tests-186_passing-brightgreen?style=for-the-badge)](tests/)

</div>

---

> [!NOTE]
> **Inspired by** the viral concept by **[@AItechscarlett](https://x.com/AItechscarlett/status/2067984321039012262)** — *["Claude transformed my laptop into a free entertainment center. Here are 8 prompts to create this system."](https://x.com/AItechscarlett/status/2067984321039012262)*

## What It Does

**Free AI entertainment hub** — replace Spotify, Disney+, Apple TV+, Netflix, and other paid subscriptions with a fully personalized, free entertainment system powered by Claude and AI agents.

```
"Cancel all my subscriptions and build me a free entertainment center"
```

↓ The agent generates a premium dashboard, personalized music plans, movie recommendations, YouTube schedules, weekend plans, reading lists, gaming guides, and learning curricula — all from free, legal sources.

## The 8 Workflows

| # | Workflow | Replaces | What It Generates |
|---|----------|----------|-------------------|
| 1 | **Entertainment Dashboard Builder** | Netflix homepage | HTML dashboard with 8 categories, 40+ free platforms |
| 2 | **Personal Music Curator** | Spotify | Weekly music plan with daily playlists and search terms |
| 3 | **Movie Night Planner** | Movie ticket apps | 10 mood-based movie picks with backups |
| 4 | **YouTube-to-Netflix Programmer** | Cable TV | 7-day YouTube schedule with channel recs |
| 5 | **Weekend Binge Architect** | Weekend plans | Time-blocked weekend schedule with mixed content |
| 6 | **Book & Podcast Discovery** | Kindle/Audible | Reading list + podcast recs with weekly schedule |
| 7 | **Free Gaming Guide** | Game purchases | Curated free games by platform and genre |
| 8 | **Documentary & Learning Curator** | MasterClass/Coursera | Learning paths with free courses and documentaries |

## Quick Start

### As a GLM/Claude Skill

1. Place this directory in your AI skills folder
2. The skill auto-activates when you mention entertainment, subscriptions, or free content
3. Just describe what you want:

> "Replace my Spotify with free music" → Generates a personalized weekly music plan
> "What should I watch tonight?" → Generates mood-based movie recommendations
> "Plan my weekend for free" → Generates a time-blocked weekend entertainment schedule

### Using the Scripts Directly

```bash
# 1. Generate your entertainment dashboard
python3 scripts/dashboard_builder.py --output dashboard.html

# 2. Create your personal music plan
python3 scripts/music_curator.py --genres "electronic,indie" --moods "focus,chill"

# 3. Get tonight's movie recommendations
python3 scripts/movie_planner.py --mood "action" --count 10

# 4. Turn YouTube into Netflix
python3 scripts/youtube_programmer.py --days 7

# 5. Plan your weekend
python3 scripts/weekend_binge.py --hours 12 --interests "movies,gaming,cooking"

# 6. Find free books and podcasts
python3 scripts/book_podcast_finder.py --genres "sci-fi,history"

# 7. Discover free games
python3 scripts/gaming_guide.py --platform "pc" --genres "indie,strategy"

# 8. Create a learning plan
python3 scripts/learning_curator.py --topics "AI,space,economics" --level "beginner"
```

### Run Everything (Full Entertainment Hub)

```bash
python3 scripts/dashboard_builder.py --output dashboard.html
python3 scripts/music_curator.py --output music_plan.md
python3 scripts/movie_planner.py --output movie_night.md
python3 scripts/youtube_programmer.py --output youtube_schedule.md
python3 scripts/weekend_binge.py --output weekend_plan.md
python3 scripts/book_podcast_finder.py --output reading_list.md
python3 scripts/gaming_guide.py --output gaming_guide.md
python3 scripts/learning_curator.py --output learning_plan.md
```

## Project Structure

```
entertainment-center-agent/
├── SKILL.md                         # Main skill definition (8 workflows)
├── scripts/
│   ├── dashboard_builder.py          # 🎬 Generate entertainment dashboard (HTML/Markdown)
│   ├── music_curator.py              # 🎵 Personal music curator (replaces Spotify)
│   ├── movie_planner.py              # 🎥 Movie night planner
│   ├── youtube_programmer.py        # 📺 YouTube-to-Netflix schedule
│   ├── weekend_binge.py              # 🍿 Weekend binge architect
│   ├── book_podcast_finder.py        # 📚 Book & podcast discovery
│   ├── gaming_guide.py               # 🎮 Free gaming guide
│   └── learning_curator.py           # 🧠 Documentary & learning curator
├── references/
│   ├── prompts.md                    # Complete 8 prompt templates
│   ├── platforms.md                  # 100+ curated free platforms database
│   └── conventions.md                # Output format standards
├── tests/
│   ├── test_dashboard_builder.py     # Dashboard builder tests
│   ├── test_music_curator.py         # Music curator tests
│   ├── test_movie_planner.py         # Movie planner tests
│   ├── test_youtube_programmer.py    # YouTube programmer tests
│   ├── test_weekend_binge.py         # Weekend binge tests
│   ├── test_book_podcast_finder.py   # Book/podcast finder tests
│   ├── test_gaming_guide.py          # Gaming guide tests
│   ├── test_learning_curator.py      # Learning curator tests
│   └── test_platforms_db.py         # Platform database validation tests
├── assets/
│   └── prompts/                      # Prompt templates directory
├── .github/
│   └── workflows/                    # GitHub Actions CI
├── .gitignore
├── LICENSE                           # MIT License
├── CHANGELOG.md                      # Version history
├── CODE_OF_CONDUCT.md                # Community guidelines
└── README.md                         # This file
```

## The 8 Master Prompts

This skill is built around 8 powerful prompts that each generate a complete entertainment experience:

### 1. Free Entertainment Dashboard
> "Act as my entertainment system designer. Create a simple laptop entertainment dashboard using only free and legal sources..."

### 2. Personal Music Curator
> "Act as my personal music curator. I like [artists/genres/moods]. Build me a weekly music plan using free legal platforms..."

### 3. Movie Night Planner
> "Act as my movie night assistant. I want to watch something tonight for free and legally. My mood is [mood]..."

### 4. YouTube-to-Netflix
> "Act as a YouTube programming director. Build me a Netflix-style weekly schedule using only YouTube..."

### 5. Weekend Binge Architect
> "Create a free weekend entertainment plan for me. I have [hours] available. My interests are [interests]..."

### 6. Book & Podcast Discovery
> "Act as my book and podcast curator. I'm interested in [genres/topics]. Find me free books from Project Gutenberg..."

### 7. Free Gaming Guide
> "Act as my free gaming curator. I play on [platform]. I like [genres]. Find me the best free games..."

### 8. Documentary & Learning Curator
> "Act as my learning and documentary curator. I'm interested in [topics]. Find me free documentaries..."

See `references/prompts.md` for the complete prompt templates with customization variables.

## Free Platform Database

The skill maintains a curated database of **100+ free and legal entertainment platforms**:

| Category | Platforms | Examples |
|----------|-----------|----------|
| 🎬 Movies | 10 | Tubi, Pluto TV, Crackle, Freevee |
| 📺 TV Shows | 10 | Tubi, Pluto TV, CW Seed, PBS |
| 🎵 Music | 10 | YouTube Music, SoundCloud, Bandcamp |
| 🎙️ Podcasts | 10 | Spotify (free), Apple Podcasts, YouTube |
| 📚 Books | 10 | Project Gutenberg, Open Library, Librivox |
| 🎮 Games | 10 | itch.io, Steam F2P, Poki, Kongregate |
| 🎥 Documentaries | 10 | YouTube, PBS, TED, Documentary+ |
| 🧠 Learning | 10 | Khan Academy, MIT OCW, Coursera (audit) |

See `references/platforms.md` for the complete verified database.

## Features

- **Zero dependencies** — All scripts use only Python standard library
- **Real platform data** — Curated database of 100+ verified free platforms
- **Multiple output formats** — HTML dashboard or Markdown documents
- **Personalized** — Customizes recommendations based on your preferences
- **Legal only** — Never recommends piracy or illegal streaming
- **Self-contained** — Each script works independently or as part of the chain
- **CLI interface** — Full argparse CLI with --help on every script

## Safety Principles

1. **Only free and legal sources** — No piracy, no torrents, no illegal streaming
2. **Age-appropriate** — Flags mature content when detected
3. **No subscription tricks** — Clearly distinguishes free tiers from paid upgrades
4. **Region awareness** — Notes when platform availability varies by country
5. **Creator respect** — Always includes attribution and links to support creators
6. **Privacy-first** — No account creation required unless explicitly stated
7. **Ad transparency** — Notes which platforms use ads vs truly free

## Testing

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test
python3 -m pytest tests/test_dashboard_builder.py -v

# Run with coverage
python3 -m pytest tests/ --cov=scripts -v
```

## Requirements

- Python 3.8+
- No external dependencies (standard library only)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Acknowledgments & Credits

- **Inspired by** [@AItechscarlett](https://x.com/AItechscarlett) — [original viral post: "8 prompts to create a free entertainment center with Claude"](https://x.com/AItechscarlett/status/2067984321039012262)
- **Skill architecture** based on [GitHub Agent Skill](https://github.com/roman-ryzenadvanced/github-agent-skill) by [roman-ryzenadvanced](https://github.com/roman-ryzenadvanced)
- **Platform data** verified against [EpicGames/lore](https://github.com/EpicGames/lore) open-source standards

---

<div align="center">

**Built for AI-Powered Entertainment — No Subscriptions Required**

[👉 Get 10% OFF Z.ai GLM 5.2 Coding Plan](https://z.ai/subscribe?ic=ROK78RJKNW)

</div>
