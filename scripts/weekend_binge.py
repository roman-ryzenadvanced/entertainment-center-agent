#!/usr/bin/env python3
"""
Weekend Binge Architect
========================
Generates a detailed weekend entertainment schedule for Saturday and Sunday,
organized into morning/afternoon/evening time blocks. Mixes movies, YouTube
series, podcasts, free games, documentaries, and reading with time estimates.

Usage:
    python weekend_binge.py --hours 12 --interests "movies,games,podcasts"
    python weekend_binge.py --hours 16 --output epic_weekend.md
"""

import argparse
import sys
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Activity templates organized by time-of-day suitability and type
# ---------------------------------------------------------------------------
MORNING_ACTIVITIES = [
    {"type": "podcast", "emoji": "\U0001f399\ufe0f", "title": "True Crime Deep Dive",
     "desc": "Start the morning with a gripping true crime podcast episode while making breakfast.",
     "duration": 45, "platform": "Spotify Podcasts / Apple Podcasts",
     "search": "best true crime podcasts 2024", "link": "https://open.spotify.com/podcasts"},
    {"type": "reading", "emoji": "\U0001f4da", "title": "Classic Novel Chapter",
     "desc": "Read 2-3 chapters of a classic novel from Project Gutenberg with your morning coffee.",
     "duration": 40, "platform": "Project Gutenberg",
     "search": "Project Gutenberg top 100", "link": "https://gutenberg.org/ebooks/search/"},
    {"type": "youtube", "emoji": "\U0001f4fa", "title": "Science Explainer Binge",
     "desc": "Watch 3-4 Kurzgesagt or Veritasium videos \u2014 learn something amazing before lunch.",
     "duration": 35, "platform": "YouTube",
     "search": "Kurzgesagt In a Nutshell playlist", "link": "https://youtube.com/@kurzgesagt"},
    {"type": "documentary", "emoji": "\U0001f30f", "title": "Nature Documentary",
     "desc": "Watch a BBC Earth or nature documentary on YouTube. Start the day with beauty.",
     "duration": 50, "platform": "YouTube / Tubi",
     "search": "BBC Earth documentary full", "link": "https://youtube.com/@BBCEarth"},
    {"type": "podcast", "emoji": "\U0001f399\ufe0f", "title": "Daily News Briefing",
     "desc": "Catch up on world events with a quality news podcast while getting ready.",
     "duration": 25, "platform": "Spotify / Apple Podcasts",
     "search": "daily news podcast briefing", "link": "https://open.spotify.com/podcasts"},
    {"type": "reading", "emoji": "\U0001f4da", "title": "Short Story Collection",
     "desc": "Read a short story from a free anthology on Standard Ebooks or Smashwords.",
     "duration": 30, "platform": "Standard Ebooks",
     "search": "free short story collection", "link": "https://standardebooks.org"},
    {"type": "youtube", "emoji": "\U0001f4fa", "title": "Fitness / Yoga Flow",
     "desc": "Start the day right with a yoga class or bodyweight workout video.",
     "duration": 30, "platform": "YouTube",
     "search": "Yoga With Adriene morning routine", "link": "https://youtube.com/@yogawithadriene"},
    {"type": "documentary", "emoji": "\U0001f30f", "title": "History Channel Episode",
     "desc": "Watch a CrashCourse or Oversimplified history video to get your brain going.",
     "duration": 20, "platform": "YouTube",
     "search": "Oversimplified history full video", "link": "https://youtube.com/@OverSimplified"},
]

AFTERNOON_ACTIVITIES = [
    {"type": "movie", "emoji": "\U0001f3ac", "title": "Feature Film on Tubi",
     "desc": "Settle in for a complete movie from Tubi's library. Pick from the comedy or action categories.",
     "duration": 120, "platform": "Tubi",
     "search": "Tubi best free movies 2024", "link": "https://tubitv.com"},
    {"type": "gaming", "emoji": "\U0001f3ae", "title": "Indie Game Session",
     "desc": "Play a free indie game from itch.io. Try something you've never heard of from the featured section.",
     "duration": 90, "platform": "itch.io",
     "search": "itch.io featured games", "link": "https://itch.io/featured"},
    {"type": "youtube", "emoji": "\U0001f4fa", "title": "Video Essay Marathon",
     "desc": "Watch 3 long-form video essays from creators like Johnny Harris, Polyphonic, or Game Maker's Toolkit.",
     "duration": 75, "platform": "YouTube",
     "search": "best video essays 2024 YouTube", "link": "https://youtube.com"},
    {"type": "podcast", "emoji": "\U0001f399\ufe0f", "title": "Long-Form Interview",
     "desc": "Listen to a 1-hour interview from Diary of a CEO or Hot Ones while doing chores or cooking.",
     "duration": 60, "platform": "Spotify / YouTube",
     "search": "Hot Ones best interviews 2024", "link": "https://open.spotify.com"},
    {"type": "documentary", "emoji": "\U0001f30f", "title": "Full-Length Documentary",
     "desc": "Watch a complete documentary on YouTube or Tubi. True crime, nature, or science.",
     "duration": 90, "platform": "YouTube / Tubi",
     "search": "full documentary free 2024", "link": "https://tubitv.com/categories/documentaries"},
    {"type": "gaming", "emoji": "\U0001f3ae", "title": "Browser Game Blitz",
     "desc": "Try 3-4 quick browser games on Poki or CrazyGames. Perfect for casual afternoon fun.",
     "duration": 45, "platform": "Poki / CrazyGames",
     "search": "best free browser games Poki", "link": "https://poki.com"},
    {"type": "reading", "emoji": "\U0001f4da", "title": "Deep Reading Session",
     "desc": "Read 4-5 chapters of your current book from Open Library. Find a comfortable spot and focus.",
     "duration": 60, "platform": "Open Library",
     "search": "Open Library free borrow", "link": "https://openlibrary.org"},
    {"type": "movie", "emoji": "\U0001f3ac", "title": "Classic Film Matinee",
     "desc": "Watch a classic movie you've always meant to see. Try Hitchcock, Kurosawa, or Chaplin.",
     "duration": 105, "platform": "YouTube / Tubi",
     "search": "public domain classic movies", "link": "https://youtube.com"},
]

EVENING_ACTIVITIES = [
    {"type": "movie", "emoji": "\U0001f3ac", "title": "Movie Night Double Feature",
     "desc": "Two movies back-to-back for the ultimate binge. Start lighter, end with something intense.",
     "duration": 240, "platform": "Tubi / Pluto TV",
     "search": "Tubi double feature recommendations", "link": "https://tubitv.com"},
    {"type": "youtube", "emoji": "\U0001f4fa", "title": "YouTube Series Binge",
     "desc": "Watch an entire season of a YouTube original series or playlist. Great Rabbit-Hole content.",
     "duration": 90, "platform": "YouTube",
     "search": "YouTube original series playlist", "link": "https://youtube.com"},
    {"type": "gaming", "emoji": "\U0001f3ae", "title": "Free-to-Play Steam Session",
     "desc": "Play a free game from Steam or Epic. Try something new from the F2P section.",
     "duration": 120, "platform": "Steam F2P",
     "search": "Steam free to play best rated", "link": "https://store.steampowered.com/genre/Free%20to%20Play"},
    {"type": "podcast", "emoji": "\U0001f399\ufe0f", "title": "Late Night Story Podcast",
     "desc": "Wind down with a storytelling podcast \u2014 Lore, Welcome to Night Vale, or a sleep story.",
     "duration": 45, "platform": "Spotify / Apple Podcasts",
     "search": "best storytelling podcasts evening", "link": "https://open.spotify.com"},
    {"type": "documentary", "emoji": "\U0001f30f", "title": "True Crime Documentary Night",
     "desc": "Watch a true crime doc on YouTube or Tubi. Perfect for evening viewing with the lights low.",
     "duration": 80, "platform": "YouTube / Tubi",
     "search": "true crime documentary free full", "link": "https://tubitv.com"},
    {"type": "reading", "emoji": "\U0001f4da", "title": "Bedtime Reading",
     "desc": "Read a chapter or two before bed. Light fiction or poetry works best for winding down.",
     "duration": 30, "platform": "Project Gutenberg",
     "search": "classic literature bedtime reading", "link": "https://gutenberg.org"},
    {"type": "gaming", "emoji": "\U0001f3ae", "title": "Relaxing Game Before Bed",
     "desc": "Play a calming game \u2014 try A Short Hike, Stardew Valley (demo), or a cozy browser game.",
     "duration": 45, "platform": "itch.io / Poki",
     "search": "cozy games free browser", "link": "https://itch.io/games/tag-cozy"},
    {"type": "movie", "emoji": "\U0001f3ac", "title": "Cult Classic Discovery",
     "desc": "Watch that cult classic everyone references but you've never seen. Tonight's the night.",
     "duration": 110, "platform": "Tubi / YouTube",
     "search": "must-see cult classic movies free", "link": "https://tubitv.com"},
]

# ---------------------------------------------------------------------------
# Interest → activity type preference mapping
# ---------------------------------------------------------------------------
INTEREST_TO_TYPE = {
    "movies": ["movie"],
    "tv": ["movie", "youtube"],
    "music": ["youtube"],
    "podcasts": ["podcast"],
    "podcast": ["podcast"],
    "books": ["reading"],
    "reading": ["reading"],
    "games": ["gaming"],
    "gaming": ["gaming"],
    "documentaries": ["documentary"],
    "docs": ["documentary"],
    "youtube": ["youtube"],
    "science": ["documentary", "youtube"],
    "history": ["documentary", "reading"],
    "tech": ["youtube", "gaming"],
    "fitness": ["youtube", "podcast"],
    "cooking": ["youtube"],
    "food": ["youtube"],
    "travel": ["youtube", "documentary"],
    "comedy": ["youtube", "movie"],
    "horror": ["movie", "documentary"],
    "learning": ["documentary", "reading", "youtube"],
}

BLOCK_TIMES = {
    "morning":   {"start": "8:00 AM",  "end": "12:00 PM", "emoji": "\u2600\ufe0f", "label": "Morning"},
    "afternoon": {"start": "1:00 PM",  "end": "5:00 PM",  "emoji": "\U0001f305", "label": "Afternoon"},
    "evening":   {"start": "7:00 PM",  "end": "10:00 PM", "emoji": "\U0001f319", "label": "Evening"},
}


def select_activities(block_activities, preferred_types, max_hours):
    """Select activities for a block, preferring the user's interests."""
    scored = []
    for act in block_activities:
        score = 0
        if preferred_types and act["type"] in preferred_types:
            score += 10
        score += (max_hours * 60 - act["duration"])  # prefer shorter if tight on time
        scored.append((score, act))
    scored.sort(key=lambda x: -x[0])
    return [act for _, act in scored[:2]]  # top 2 per block


def generate_plan(hours, interests):
    """Generate the weekend entertainment plan as markdown."""
    now = datetime.now().strftime("%B %d, %Y")

    # Determine preferred activity types from interests
    preferred_types = []
    if interests:
        for interest in interests:
            types = INTEREST_TO_TYPE.get(interest.lower(), [])
            preferred_types.extend(types)
        preferred_types = list(set(preferred_types))

    hours_per_day = hours / 2

    lines = []
    lines.append(f"# \U0001f3a0 Weekend Binge Plan")
    lines.append(f"*{hours} hours of curated entertainment across Saturday & Sunday \u2014 {now}*\n")

    # Summary
    if interests:
        lines.append("## \u2699\ufe0f Your Interests\n")
        lines.append(f"Tailoring plan around: **{', '.join(interests)}**\n")
        if preferred_types:
            type_labels = {
                "movie": "\U0001f3ac Movies", "youtube": "\U0001f4fa YouTube",
                "podcast": "\U0001f399\ufe0f Podcasts", "reading": "\U0001f4da Reading",
                "gaming": "\U0001f3ae Gaming", "documentary": "\U0001f30f Documentaries",
            }
            mapped = [type_labels.get(t, t.title()) for t in preferred_types if t in type_labels]
            if mapped:
                lines.append(f"Activity mix: {', '.join(mapped)}\n")

    # Saturday
    lines.append("---\n")
    lines.append(f"## \U0001f3c0 Saturday ({hours_per_day:.0f} hours planned)\n")
    sat_time_used = 0

    for block_name in ["morning", "afternoon", "evening"]:
        block_info = BLOCK_TIMES[block_name]
        if block_name == "morning":
            pool = MORNING_ACTIVITIES
        elif block_name == "afternoon":
            pool = AFTERNOON_ACTIVITIES
        else:
            pool = EVENING_ACTIVITIES

        selected = select_activities(pool, preferred_types, hours_per_day)

        lines.append(f"### {block_info['emoji']} {block_info['label']} ({block_info['start']} \u2013 {block_info['end']})\n")

        for i, act in enumerate(selected, 1):
            sat_time_used += act["duration"]
            lines.append(f"**{i}. {act['emoji']} {act['title']}**")
            lines.append(f"- \u23f1\ufe0f Duration: **{act['duration']} minutes**")
            lines.append(f"- \U0001f3af Platform: [{act['platform']}]({act['link']})")
            lines.append(f"- \U0001f4dd {act['desc']}")
            lines.append(f"- \U0001f50d Search: `{act['search']}`")
            lines.append("")

    sat_total = f"{sat_time_used / 60:.1f}"
    lines.append(f"> Saturday total: **{sat_total} hours** of entertainment\n")

    # Sunday
    lines.append("---\n")
    lines.append(f"## \U0001f305 Sunday ({hours_per_day:.0f} hours planned)\n")
    sun_time_used = 0

    for block_name in ["morning", "afternoon", "evening"]:
        block_info = BLOCK_TIMES[block_name]
        if block_name == "morning":
            pool = MORNING_ACTIVITIES
        elif block_name == "afternoon":
            pool = AFTERNOON_ACTIVITIES
        else:
            pool = EVENING_ACTIVITIES

        selected = select_activities(pool, preferred_types, hours_per_day)

        lines.append(f"### {block_info['emoji']} {block_info['label']} ({block_info['start']} \u2013 {block_info['end']})\n")

        for i, act in enumerate(selected, 1):
            sun_time_used += act["duration"]
            lines.append(f"**{i}. {act['emoji']} {act['title']}**")
            lines.append(f"- \u23f1\ufe0f Duration: **{act['duration']} minutes**")
            lines.append(f"- \U0001f3af Platform: [{act['platform']}]({act['link']})")
            lines.append(f"- \U0001f4dd {act['desc']}")
            lines.append(f"- \U0001f50d Search: `{act['search']}`")
            lines.append("")

    sun_total = f"{sun_time_used / 60:.1f}"
    lines.append(f"> Sunday total: **{sun_total} hours** of entertainment\n")

    # Free Platform Quick Reference
    lines.append("---\n")
    lines.append("## \U0001f517 Quick Platform Links\n")
    lines.append("| Platform | URL | Free Content |")
    lines.append("|----------|-----|-------------|")
    lines.append("| [Tubi]({}) | tubitv.com | Movies & TV |".format("https://tubitv.com"))
    lines.append("| [Pluto TV]({}) | pluto.tv | Live & On-Demand TV |".format("https://pluto.tv"))
    lines.append("| [YouTube]({}) | youtube.com | Everything |".format("https://youtube.com"))
    lines.append("| [Spotify Podcasts]({}) | spotify.com | Podcasts |".format("https://open.spotify.com"))
    lines.append("| [Project Gutenberg]({}) | gutenberg.org | Free Books |".format("https://gutenberg.org"))
    lines.append("| [Open Library]({}) | openlibrary.org | Borrowed Books |".format("https://openlibrary.org"))
    lines.append("| [itch.io]({}) | itch.io | Indie Games |".format("https://itch.io"))
    lines.append("| [Poki]({}) | poki.com | Browser Games |".format("https://poki.com"))
    lines.append("| [Kongregate]({}) | kongregate.com | Browser Games |".format("https://kongregate.com"))
    lines.append("| [Steam F2P]({}) | store.steampowered.com | PC Games |".format("https://store.steampowered.com/genre/Free%20to%20Play"))
    lines.append("")

    # Weekend tips
    lines.append("---\n")
    lines.append("## \U0001f4a1 Weekend Binge Tips\n")
    lines.append("- **Prep Friday night**: Queue up your weekend content and pre-load games.")
    lines.append("- **Mix it up**: Alternate between screen time and active time for better enjoyment.")
    lines.append("- **Snack breaks**: Make a big batch of popcorn once and keep it for movie blocks.")
    lines.append("- **Take real breaks**: Step outside between blocks \u2014 your eyes and brain will thank you.")
    lines.append("- **Stay hydrated**: Keep water nearby \u2014 binge sessions sneak up on you!")
    lines.append("- **Sleep matters**: Don't sacrifice Sunday night sleep for one more episode.")
    lines.append("")

    total_time = (sat_time_used + sun_time_used) / 60
    lines.append(f"*\U0001f3a0 Total weekend entertainment: **{total_time:.1f} hours** \u2014 Generated {now}*\n")

    return "\n".join(lines)


def main():
    """Parse arguments and generate the weekend plan."""
    parser = argparse.ArgumentParser(
        description="Generate a weekend entertainment schedule with mixed activities and time blocks.",
        epilog="Example: python weekend_binge.py --hours 14 --interests 'movies,games,podcasts' --output weekend.md",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=12,
        help="Total hours of entertainment for the weekend (default: 12)",
    )
    parser.add_argument(
        "--interests",
        default="",
        help="Comma-separated interests to prioritize (e.g., movies,games,podcasts,reading)",
    )
    parser.add_argument(
        "--output",
        default="weekend_plan.md",
        help="Output markdown file path (default: weekend_plan.md)",
    )

    args = parser.parse_args()

    if args.hours < 2 or args.hours > 48:
        print("Error: --hours must be between 2 and 48.", file=sys.stderr)
        sys.exit(1)

    interests = [i.strip() for i in args.interests.split(",") if i.strip()] if args.interests else None

    try:
        content = generate_plan(hours=args.hours, interests=interests)

        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)

        abs_path = os.path.abspath(args.output)
        print(f"\n{'='*60}")
        print(f"  \U0001f3a0 Weekend Binge Plan Generated Successfully!")
        print(f"{'='*60}")
        print(f"  \U0001f4c4 File:      {abs_path}")
        print(f"  \u23f1\ufe0f Hours:     {args.hours} ({args.hours // 2} per day)")
        print(f"  \U0001f4c5 Days:      Saturday & Sunday")
        print(f"  \u23f0 Blocks/day: Morning / Afternoon / Evening")
        if interests:
            print(f"  \U0001f499 Interests: {', '.join(interests)}")
        print(f"{'='*60}\n")

    except PermissionError:
        print(f"Error: Permission denied writing to '{args.output}'.", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: Could not write file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
