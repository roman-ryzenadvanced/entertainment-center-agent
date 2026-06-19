# Entertainment Prompts Reference

This document contains the complete set of 8 master prompts that power the Entertainment Center Agent. Each prompt is designed to be used with Claude or any AI assistant to generate personalized entertainment content.

## The 8 Master Prompts

### Prompt 1: Free Entertainment Dashboard

```
Act as my entertainment system designer. Create a simple laptop entertainment
dashboard using only free and legal sources. Organize it into Movies, TV Shows,
Music, Podcasts, Books, Games, Documentaries, and Learning. For each section,
give me 5 reliable free platforms, what they are best for, and how I should use
them. Keep it beginner-friendly and make it feel like a premium streaming
homepage.
```

**Best for:** Getting a complete overview of all free entertainment options. Use this as your starting point to understand what's available.

**Customization variables:**
- `[favorite genres]` — Add your preferred genres for personalized picks
- `[region]` — Specify your country for region-specific platforms
- `[device]` — Laptop, tablet, phone for optimized layout

---

### Prompt 2: Personal Music Curator

```
Act as my personal music curator. I like [insert artists/genres/moods]. Build me
a weekly music plan using free legal platforms like YouTube, SoundCloud, Bandcamp,
radio stations, live sessions, and public playlists. Create daily playlists for
focus, workout, chill, deep work, cooking, and night listening. Include search
terms I can copy and paste.
```

**Best for:** Completely replacing Spotify with a personalized, free music experience.

**Customization variables:**
- `[insert artists]` — e.g., "Radiohead, Daft Punk, Kendrick Lamar"
- `[insert genres]` — e.g., "electronic, hip-hop, indie rock"
- `[insert moods]` — e.g., "focus, workout, chill, melancholy"

---

### Prompt 3: Movie Night Planner

```
Act as my movie night assistant. I want to watch something tonight for free and
legally. My mood is [funny/scary/romantic/action/slow/deep]. Give me 10 movie
ideas available through free legal platforms, public domain libraries, or
ad-supported streaming. For each one, include why I might like it, who it is
best for, and a backup option if I cannot find it.
```

**Best for:** When you know what you want to feel but don't know what to watch.

**Customization variables:**
- `[mood]` — funny, scary, romantic, action, slow, deep, inspiring, nostalgic
- `[duration]` — Short (<90min), Medium (90-120min), Long (>120min)
- `[decade]` — 80s, 90s, 2000s, modern for era preferences

---

### Prompt 4: YouTube-to-Netflix Programmer

```
Act as a YouTube programming director. Build me a Netflix-style weekly schedule
using only YouTube. I want categories like documentaries, comedy, travel, tech,
food, fitness, interviews, and cozy background videos. Give me 3 channel
recommendations per category, what to search for, and a 7-day watching schedule.
```

**Best for:** Turning YouTube's chaotic library into a curated, scheduled experience.

**Customization variables:**
- `[categories]` — Customize the content categories you want
- `[time per day]` — How much YouTube time per day (30min, 1hr, 2hr)
- `[exclude]` — Topics to avoid

---

### Prompt 5: Weekend Binge Architect

```
Create a free weekend entertainment plan for me. I have [number] hours available.
My interests are [insert interests]. Build a schedule with movies, YouTube
series, podcasts, free games, documentaries, and reading. Make it feel like a
curated streaming bundle. Include morning, afternoon, and evening options.
```

**Best for:** Planning your entire weekend without spending a cent.

**Customization variables:**
- `[hours available]` — Total hours for entertainment (6, 12, 20, etc.)
- `[interests]` — Movies, gaming, cooking, nature, history, comedy, etc.
- `[solo/group]` — Solo entertainment or group activities

---

### Prompt 6: Book & Podcast Discovery

```
Act as my book and podcast curator. I'm interested in [insert genres/topics].
Find me free books from Project Gutenberg, Open Library, and Librivox. Also
recommend podcasts available on free platforms. Create a weekly reading and
listening schedule with variety across genres.
```

**Best for:** Building a reading habit and podcast routine for free.

**Customization variables:**
- `[genres/topics]` — sci-fi, self-help, history, technology, true crime
- `[format]` — Text books, audiobooks, podcasts, or mix
- `[pace]` — Casual (1 book/month), Regular (1 book/week), Intensive

---

### Prompt 7: Free Gaming Guide

```
Act as my free gaming curator. I play on [PC/Mac/Mobile/Browser]. I like
[insert genres]. Find me the best free games from itch.io, Steam free-to-play,
browser games, and mobile free games. Organize by genre and include difficulty
level, time commitment, and why each is worth playing.
```

**Best for:** Discovering high-quality free games without spending on new titles.

**Customization variables:**
- `[platform]` — PC, Mac, Mobile (iOS/Android), Browser
- `[genres]` — indie, RPG, strategy, puzzle, casual, multiplayer, simulation
- `[commitment]` — Quick (15min sessions), Medium (1hr), Deep (multi-hour)

---

### Prompt 8: Documentary & Learning Curator

```
Act as my learning and documentary curator. I'm interested in [insert topics].
Find me free documentaries on YouTube and ad-supported platforms. Also recommend
free courses from Khan Academy, Coursera (audit mode), MIT OpenCourseWare, and
YouTube educational channels. Build a weekly learning schedule.
```

**Best for:** Self-education and intellectual entertainment without paying for courses.

**Customization variables:**
- `[topics]` — AI, space, history, economics, art, science, philosophy
- `[level]` — Beginner, intermediate, advanced
- `[format]` — Short videos (TED talks), Long-form (courses), Mix

---

## Prompt Chaining

These prompts work best when chained together for a complete entertainment system:

```
Chain: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

Dashboard → Music → Movies → YouTube → Weekend → Books → Games → Learning
```

You can run them all at once for a complete entertainment hub, or use them individually based on your current need.

## Quick Reference: Which Prompt When

| Situation | Prompt # | Name |
|-----------|---------|------|
| "I want to replace all subscriptions" | 1 | Dashboard Builder |
| "Play me music without Spotify" | 2 | Music Curator |
| "What should I watch tonight?" | 3 | Movie Planner |
| "Make YouTube organized" | 4 | YouTube Programmer |
| "Plan my weekend" | 5 | Weekend Binge |
| "I need reading material" | 6 | Book & Podcast |
| "Find me free games" | 7 | Gaming Guide |
| "I want to learn something new" | 8 | Learning Curator |
| "Full entertainment system" | All 8 | Complete Chain |
