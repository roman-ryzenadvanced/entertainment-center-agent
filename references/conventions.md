# Output Format Conventions

This document defines the standard output formats used across all entertainment center scripts.

## Output Format: Markdown

All scripts default to Markdown output with these conventions:

### Header Structure
```markdown
# [Title]
> Generated: [Date] | Entertainment Center Agent v1.0.0
```

### Category Headers
Use emoji prefixes for visual scanning:
- 🎬 Movies
- 📺 TV Shows
- 🎵 Music
- 🎙️ Podcasts
- 📚 Books
- 🎮 Games
- 🎥 Documentaries
- 🧠 Learning

### Tables
Use markdown tables for structured data:
```markdown
| Platform | Best For | URL | Quality |
|----------|----------|-----|---------|
| Tubi | Large movie catalog | tubitv.com | ⭐⭐⭐⭐⭐ |
```

### Rating System
- ⭐ — Poor (limited content, unreliable)
- ⭐⭐ — Fair (small catalog)
- ⭐⭐⭐ — Good (decent selection)
- ⭐⭐⭐⭐ — Very Good (large catalog)
- ⭐⭐⭐⭐⭐ — Excellent (top-tier free platform)

## Output Format: HTML

The HTML dashboard format uses these conventions:

### Theme
- Dark theme inspired by Netflix/Spotify
- CSS custom properties for easy theming
- Responsive design (mobile-first)

### Color Palette
```css
--bg-primary: #0a0a0a;
--bg-secondary: #1a1a1a;
--bg-card: #2a2a2a;
--text-primary: #ffffff;
--text-secondary: #b3b3b3;
--accent-primary: #e50914;  /* Netflix red */
--accent-secondary: #1db954; /* Spotify green */
--accent-music: #1db954;
--accent-movies: #e50914;
--accent-tv: #00a8e1;
--accent-podcasts: #872de2;
--accent-books: #f59e0b;
--accent-games: #10b981;
--accent-docs: #3b82f6;
--accent-learning: #ec4899;
```

### Layout
- CSS Grid for responsive layout
- Cards for each category
- Hover effects on interactive elements
- Embedded icons using Unicode/emoji

## File Naming Conventions

Generated output files follow these patterns:

| Script | Default Output | Custom via --output |
|--------|---------------|---------------------|
| dashboard_builder.py | dashboard.html | Any filename |
| music_curator.py | music_plan.md | Any filename |
| movie_planner.py | movie_night.md | Any filename |
| youtube_programmer.py | youtube_schedule.md | Any filename |
| weekend_binge.py | weekend_plan.md | Any filename |
| book_podcast_finder.py | reading_list.md | Any filename |
| gaming_guide.py | gaming_guide.md | Any filename |
| learning_curator.py | learning_plan.md | Any filename |

## Content Guidelines

### Platform Descriptions
Each platform recommendation must include:
1. **Name** — Platform name
2. **What it's best for** — One-line description of its strength
3. **Content available** — Type and amount of content
4. **Access method** — URL or app
5. **Quality rating** — Star rating (1-5)
6. **Notes** — Any limitations (ads, region, registration)

### Recommendations Format
Each content recommendation must include:
1. **Title** — Content title
2. **Platform** — Where to find it
3. **Why you'll like it** — Personalized pitch
4. **Best for** — Target audience/mood
5. **Duration/Length** — Time commitment
6. **Backup option** — Alternative if unavailable

### Schedule Format
Time-blocked schedules use 24-hour format:
```
09:00 - 10:30 | 🎬 Movie: [Title] on [Platform]
10:30 - 11:00 | ☕ Break
11:00 - 12:00 | 📚 Reading: [Book] on [Platform]
```

## Versioning

All generated files include a generation timestamp and version stamp:
```markdown
> Generated: 2026-06-20 | Entertainment Center Agent v1.0.0
```

This allows tracking when content was generated and which agent version was used.
