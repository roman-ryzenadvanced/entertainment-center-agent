---
name: entertainment-center-agent
description: "Unified AI Entertainment Center Agent that transforms your laptop into a free, premium entertainment hub using Claude. Orchestrates 8 powerful workflows: Entertainment Dashboard Builder, Personal Music Curator (replaces Spotify), Movie Night Planner, YouTube-to-Netflix Programmer, Weekend Binge Architect, Book & Podcast Discovery, Free Gaming Guide, and Documentary & Learning Curator. Use this skill whenever the user wants to replace paid subscriptions (Spotify, Disney+, Apple TV+, Netflix), build a free entertainment system, discover free content across movies/music/books/games, plan weekend entertainment, or create a personalized media experience. Also use when users mention 'cancel spotify', 'free entertainment', 'entertainment center', 'free movies', 'free music', 'binge plan', 'movie night', or 'free streaming'."
---

# Entertainment Center Agent — Cancel Subscriptions, Keep the Experience

A unified orchestration skill for GLM/Claude that turns a single natural language prompt into a fully personalized, free entertainment system. No more paying for Spotify, Disney+, Apple TV+, or Netflix — this agent chains 8 powerful workflows together to build a premium-feeling entertainment hub using only free and legal sources.

## When This Skill Activates

- User wants to cancel paid subscriptions: *"I want to stop paying for Spotify"*
- User asks for free entertainment alternatives: *"Find me free movies and music"*
- User wants a personalized media experience: *"Build me a movie night plan"*
- User wants a full entertainment system: *"Turn my laptop into an entertainment center"*
- User asks for content recommendations: *"What should I watch tonight?"*
- User wants a weekend plan: *"Plan my weekend entertainment"*
- User mentions any of: 'cancel spotify', 'free entertainment', 'entertainment dashboard', 'movie night', 'binge plan', 'free music', 'free streaming', 'YouTube Netflix'

## Core Orchestration Workflows

The agent supports 8 primary workflows. Detect which one the user needs and execute it. If the user's request spans multiple workflows, chain them in sequence.

### Workflow 1: Entertainment Dashboard Builder

**Purpose:** Generate a comprehensive, organized entertainment dashboard that replaces all paid subscription services with free alternatives across 8 content categories.

**Steps:**
1. **Parse user preferences** — Extract favorite genres, artists, interests, mood preferences
2. **Run `scripts/dashboard_builder.py`** — Generates a structured dashboard with:
   - Movies section (5 free platforms + recommendations)
   - TV Shows section (5 free platforms + recommendations)
   - Music section (5 free platforms + playlist links)
   - Podcasts section (5 free platforms + top picks)
   - Books section (5 free platforms + reading lists)
   - Games section (5 free platforms + suggestions)
   - Documentaries section (5 free platforms + curated picks)
   - Learning section (5 free platforms + course picks)
3. **Format as premium homepage** — CSS-styled dashboard with categories, icons, and direct links
4. **Save output** — HTML dashboard + Markdown summary

**Prompt template:**
```
Act as my entertainment system designer. Create a simple laptop entertainment
dashboard using only free and legal sources. Organize it into Movies, TV Shows,
Music, Podcasts, Books, Games, Documentaries, and Learning. For each section,
give me 5 reliable free platforms, what they are best for, and how I should use
them. Keep it beginner-friendly and make it feel like a premium streaming homepage.
```

**Example:**
> User: "Build me a free entertainment dashboard"
> Agent: Generates HTML dashboard with 8 categories, each with 5 platforms, styled like a premium streaming homepage

### Workflow 2: Personal Music Curator (Replace Spotify)

**Purpose:** Create a personalized, weekly music plan using free and legal platforms to fully replace Spotify.

**Steps:**
1. **Collect music taste** — Extract artists, genres, moods from user input
2. **Run `scripts/music_curator.py`** — Generates:
   - Personalized daily playlists (Monday–Sunday)
   - Mood-based playlists: focus, workout, chill, deep work, cooking, night
   - Platform-specific search terms (copy-paste ready)
   - Free platform recommendations: YouTube Music, SoundCloud, Bandcamp, radio stations, public playlists
3. **Weekly rotation plan** — Auto-refreshes recommendations each week

**Prompt template:**
```
Act as my personal music curator. I like [insert artists/genres/moods].
Build me a weekly music plan using free legal platforms like YouTube,
SoundCloud, Bandcamp, radio stations, live sessions, and public playlists.
Create daily playlists for focus, workout, chill, deep work, cooking, and
night listening. Include search terms I can copy and paste.
```

### Workflow 3: Movie Night Planner

**Purpose:** Find the perfect free movie for tonight based on mood, preferences, and available platforms.

**Steps:**
1. **Detect mood** — Parse user's mood preference (funny/scary/romantic/action/slow/deep)
2. **Run `scripts/movie_planner.py`** — Generates:
   - 10 movie recommendations from free legal platforms
   - Public domain libraries
   - Ad-supported streaming services
   - Each recommendation includes: why you'll like it, who it's best for, backup option
3. **Platform-aware matching** — Only suggests content available on free platforms

**Prompt template:**
```
Act as my movie night assistant. I want to watch something tonight for free
and legally. My mood is [funny/scary/romantic/action/slow/deep]. Give me 10
movie ideas available through free legal platforms, public domain libraries,
or ad-supported streaming. For each one, include why I might like it, who it
is best for, and a backup option if I cannot find it.
```

### Workflow 4: YouTube-to-Netflix Programmer

**Purpose:** Transform YouTube into a curated Netflix-like experience with weekly programming schedules.

**Steps:**
1. **Map content categories** — Documentaries, comedy, travel, tech, food, fitness, interviews, cozy background
2. **Run `scripts/youtube_programmer.py`** — Generates:
   - 3 channel recommendations per category
   - Search terms for discovery
   - 7-day watching schedule (Mon–Sun)
   - "Now Trending" section
   - Channel subscription list

**Prompt template:**
```
Act as a YouTube programming director. Build me a Netflix-style weekly schedule
using only YouTube. I want categories like documentaries, comedy, travel, tech,
food, fitness, interviews, and cozy background videos. Give me 3 channel
recommendations per category, what to search for, and a 7-day watching schedule.
```

### Workflow 5: Weekend Binge Architect

**Purpose:** Create a complete weekend entertainment plan with time-blocked scheduling.

**Steps:**
1. **Gather availability** — Get hours available and interests
2. **Run `scripts/weekend_binge.py`** — Generates:
   - Morning, afternoon, evening entertainment blocks
   - Mix of movies, YouTube series, podcasts, free games, documentaries, reading
   - Time estimates for each activity
   - "Skip ahead" options for when you want to switch

**Prompt template:**
```
Create a free weekend entertainment plan for me. I have [number] hours available.
My interests are [insert interests]. Build a schedule with movies, YouTube series,
podcasts, free games, documentaries, and reading. Make it feel like a curated
streaming bundle. Include morning, afternoon, and evening options.
```

### Workflow 6: Book & Podcast Discovery

**Purpose:** Find free books, audiobooks, and podcasts based on interests and reading habits.

**Steps:**
1. **Collect reading preferences** — Genres, authors, topics, format preferences
2. **Run `scripts/book_podcast_finder.py`** — Generates:
   - 10 book recommendations from free platforms (Project Gutenberg, Librivox, Open Library)
   - 10 podcast recommendations (free on Spotify, Apple Podcasts, YouTube)
   - Reading schedule with estimated completion times
   - Genre exploration suggestions

**Prompt template:**
```
Act as my book and podcast curator. I'm interested in [insert genres/topics].
Find me free books from Project Gutenberg, Open Library, and Librivox. Also
recommend podcasts available on free platforms. Create a weekly reading and
listening schedule with variety across genres.
```

### Workflow 7: Free Gaming Guide

**Purpose:** Discover high-quality free games across platforms.

**Steps:**
1. **Identify gaming preferences** — Platform (PC/Mac/Mobile), genre, play style
2. **Run `scripts/gaming_guide.py`** — Generates:
   - Free game recommendations by category: indie, RPG, strategy, puzzle, casual, multiplayer
   - Platform availability matrix
   - Browser-based games (no download needed)
   - Free-to-play quality picks
   - Weekly gaming schedule

**Prompt template:**
```
Act as my free gaming curator. I play on [PC/Mac/Mobile/Browser]. I like
[insert genres]. Find me the best free games from itch.io, Steam free-to-play,
browser games, and mobile free games. Organize by genre and include difficulty
level, time commitment, and why each is worth playing.
```

### Workflow 8: Documentary & Learning Curator

**Purpose:** Create a personalized learning and documentary experience for free.

**Steps:**
1. **Identify learning interests** — Topics, difficulty level, time available
2. **Run `scripts/learning_curator.py`** — Generates:
   - Documentary recommendations from YouTube, free streaming
   - Free course recommendations (Coursera audits, Khan Academy, MIT OCW, YouTube Edu)
   - Weekly learning schedule
   - Topic exploration paths (beginner → intermediate → advanced)
   - TED talk and lecture recommendations

**Prompt template:**
```
Act as my learning and documentary curator. I'm interested in [insert topics].
Find me free documentaries on YouTube and ad-supported platforms. Also recommend
free courses from Khan Academy, Coursera (audit mode), MIT OpenCourseWare, and
YouTube educational channels. Build a weekly learning schedule.
```

## Full Orchestration: One-Prompt Entertainment Hub

When the user wants the complete experience (inspired by the viral tweet), chain all 8 workflows:

**Steps:**
1. **Dashboard Builder** — Generate the master entertainment dashboard
2. **Music Curator** — Create the personalized music plan
3. **Movie Night Planner** — Set up movie recommendations
4. **YouTube Programmer** — Build the Netflix-style YouTube schedule
5. **Weekend Binge** — Create the weekend entertainment plan
6. **Book & Podcast Discovery** — Add reading and listening recommendations
7. **Free Gaming Guide** — Include game recommendations
8. **Learning Curator** — Add documentary and learning content

**Example:**
> User: "Cancel all my subscriptions and build me a free entertainment center"
> Agent: Chains all 8 workflows → produces a complete HTML dashboard + individual recommendation files for each category

## Script Reference

### Script: `dashboard_builder.py`

Generates a comprehensive HTML entertainment dashboard.

```bash
python3 scripts/dashboard_builder.py \
  --output dashboard.html \
  [--preferences "action movies, rock music, sci-fi books"] \
  [--format html|markdown]
```

**What it does:**
- Creates a premium-styled HTML dashboard with 8 content categories
- Each category has 5 free platform recommendations
- Direct links and search terms for each platform
- Responsive design that works on any screen size
- Optional Markdown output for text-based viewing

### Script: `music_curator.py`

Generates personalized weekly music plans.

```bash
python3 scripts/music_curator.py \
  --artists "Radiohead, Daft Punk, Kendrick Lamar" \
  --genres "electronic, hip-hop, indie rock" \
  --moods "focus, workout, chill" \
  --output music_plan.md
```

### Script: `movie_planner.py`

Generates movie night recommendations.

```bash
python3 scripts/movie_planner.py \
  --mood "action" \
  --output movie_night.md \
  [--count 10]
```

### Script: `youtube_programmer.py`

Generates Netflix-style YouTube schedules.

```bash
python3 scripts/youtube_programmer.py \
  --categories "documentaries, comedy, tech, food" \
  --days 7 \
  --output youtube_schedule.md
```

### Script: `weekend_binge.py`

Generates weekend entertainment plans.

```bash
python3 scripts/weekend_binge.py \
  --hours 12 \
  --interests "movies, gaming, cooking, documentaries" \
  --output weekend_plan.md
```

### Script: `book_podcast_finder.py`

Discovers free books and podcasts.

```bash
python3 scripts/book_podcast_finder.py \
  --genres "sci-fi, self-help, history" \
  --output reading_list.md
```

### Script: `gaming_guide.py`

Finds free games across platforms.

```bash
python3 scripts/gaming_guide.py \
  --platform "pc" \
  --genres "indie, strategy, puzzle" \
  --output gaming_guide.md
```

### Script: `learning_curator.py`

Creates learning and documentary schedules.

```bash
python3 scripts/learning_curator.py \
  --topics "AI, space, history, economics" \
  --level "beginner" \
  --output learning_plan.md
```

## Decision Guide: Which Workflow to Use

| User Says | Workflow |
|-----------|----------|
| "Build me an entertainment dashboard" or "Free alternatives to Netflix" | Workflow 1 (Dashboard) |
| "Replace Spotify" or "Find me free music" | Workflow 2 (Music) |
| "What should I watch tonight?" or "Movie night ideas" | Workflow 3 (Movies) |
| "Make YouTube like Netflix" or "YouTube schedule" | Workflow 4 (YouTube) |
| "Plan my weekend" or "Weekend entertainment" | Workflow 5 (Binge) |
| "Free books" or "Podcast recommendations" | Workflow 6 (Books) |
| "Free games" or "Games to play" | Workflow 7 (Gaming) |
| "Learn about X" or "Free documentaries" | Workflow 8 (Learning) |
| "Cancel all subscriptions" or "Free entertainment center" | All 8 (Full Chain) |

## Free Platform Database

The agent maintains a curated database of free and legal entertainment platforms organized by category. See `references/platforms.md` for the complete list.

### Key Platforms by Category

| Category | Top Free Platforms |
|----------|-------------------|
| Movies | YouTube Movies (free section), Tubi, Pluto TV, Crackle, Freevee |
| TV Shows | Tubi, Pluto TV, YouTube, Freevee, Crackle |
| Music | YouTube Music (free), SoundCloud, Bandcamp, iHeartRadio, TuneIn |
| Podcasts | Spotify (free), Apple Podcasts, YouTube, Podbean, Stitcher |
| Books | Project Gutenberg, Open Library, Librivox, Smashwords, Google Books |
| Games | itch.io, Steam F2P, Kongregate, Poki, CrazyGames |
| Documentaries | YouTube, PBS, TED, Documentary+, CuriosityStream (free tier) |
| Learning | Khan Academy, Coursera (audit), MIT OCW, YouTube Edu, edX (free) |

## Safety & Guardrails

1. **Only free and legal sources** — Never recommends piracy, torrents, or illegal streaming
2. **Age-appropriate content** — Flags mature content when detected
3. **No subscription tricks** — Clearly distinguishes free tiers from paid upgrades
4. **Region awareness** — Notes when platform availability varies by country
5. **Respect creators** — Always includes attribution and links to support content creators
6. **Privacy-first** — No account creation required unless explicitly stated
7. **Ad-supported transparency** — Notes which platforms use ads vs truly free

## Error Handling

When operations fail, follow this sequence:

1. **Platform unavailable** — Suggest alternative free platforms from the database
2. **No results for preferences** — Broaden search or suggest exploring new genres
3. **Rate limiting** — Implement delays between API calls to free services
4. **Broken links** — Flag and suggest searching the platform directly
5. **Script not found** — Scripts are located at the path relative to this SKILL.md

## Integration with Existing Skills

- **web-reader** — Used to fetch content from free entertainment platforms
- **web-search** — Used to discover trending content and new free platforms
- **charts** — Can visualize entertainment consumption patterns and recommendations
- **github-agent** — Can create repos to publish custom entertainment dashboards

## Output Formats

The agent can output in multiple formats:

1. **HTML Dashboard** — Full interactive dashboard with CSS styling (default)
2. **Markdown Document** — Clean, readable markdown with structured sections
3. **JSON Data** — Machine-readable format for integration with other tools
4. **Plain Text** — Simple text output for terminal viewing
