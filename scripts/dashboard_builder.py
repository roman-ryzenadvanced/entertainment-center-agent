#!/usr/bin/env python3
"""
Entertainment Dashboard Builder
=================================
Generates a comprehensive HTML entertainment dashboard organized into 8 categories
of free entertainment platforms. The dashboard uses a dark theme inspired by
Netflix/Spotify and is fully responsive.

Categories covered:
  1. Movies
  2. TV Shows
  3. Music
  4. Podcasts
  5. Books
  6. Games
  7. Documentaries
  8. Learning

Usage:
    python dashboard_builder.py --output dashboard.html --format html
    python dashboard_builder.py --format markdown --output hub.md
    python dashboard_builder.py --preferences "movies,music,games"
"""

import argparse
import sys
import os
from datetime import datetime


# ---------------------------------------------------------------------------
# Platform data: each category contains 5 real free platforms
# ---------------------------------------------------------------------------
CATEGORIES = {
    "Movies": {
        "emoji": "\U0001f3ac",
        "platforms": [
            {
                "name": "Tubi",
                "url": "https://tubitv.com",
                "description": (
                    "Over 50,000 movies and TV shows, completely free with ads. "
                    "Owned by Fox. Strong library of classic films, indie gems, "
                    "and genre titles from horror to anime. Available on web, "
                    "iOS, Android, Roku, Fire TV, and smart TVs."
                ),
            },
            {
                "name": "Pluto TV",
                "url": "https://pluto.tv",
                "description": (
                    "Paramount's free streaming service with 250+ live channels "
                    "and thousands of on-demand movies. Features a \"TV guide\" "
                    "experience with channels like MST3K, Screem, and ACTION. "
                    "Great for channel-surfing nostalgia."
                ),
            },
            {
                "name": "YouTube Movies (Free)",
                "url": "https://youtube.com/feed/storefront",
                "description": (
                    "YouTube hosts hundreds of ad-supported full-length movies for "
                    "free. Look for the \"Free with Ads\" tag. Includes public "
                    "domain classics, Bollywood hits, martial arts films, and "
                    "independent productions."
                ),
            },
            {
                "name": "Crackle",
                "url": "https://crackle.com",
                "description": (
                    "Sony's free streaming platform featuring original series and "
                    "a rotating catalog of popular movies. Known for action and "
                    "thriller titles. No signup required to start watching."
                ),
            },
            {
                "name": "Amazon Freevee",
                "url": "https://amazon.com/freevee",
                "description": (
                    "Amazon's free ad-supported service with a solid movie catalog. "
                    "Includes Originals and popular studio films. Available within "
                    "the Prime Video app or as a standalone app."
                ),
            },
        ],
    },
    "TV Shows": {
        "emoji": "\U0001f4fa",
        "platforms": [
            {
                "name": "Tubi TV",
                "url": "https://tubitv.com",
                "description": (
                    "Massive library of full TV series — sitcoms, dramas, "
                    "reality TV, anime, and British imports. Many complete series "
                    "available. Includes fan-favorites like The IT Crowd, 3rd Rock "
                    "from the Sun, and original Tubi series."
                ),
            },
            {
                "name": "Pluto TV",
                "url": "https://pluto.tv",
                "description": (
                    "Live and on-demand TV channels for free. Dedicated channels "
                    "for CSI, Naruto, Degrassi, classic sitcoms, and news. The "
                    "on-demand section has full seasons of popular shows."
                ),
            },
            {
                "name": "YouTube (Full Series)",
                "url": "https://youtube.com",
                "description": (
                    "Many shows upload full episodes legally on YouTube — "
                    "especially older series, cooking shows, and educational "
                    "content. Search for your favorite classic shows."
                ),
            },
            {
                "name": "The Roku Channel",
                "url": "https://therokuchannel.roku.com",
                "description": (
                    "Free on-demand and live TV available via the web (not just "
                    "Roku devices). Features popular TV shows, live news, and "
                    "original content. Over 10,000 titles available."
                ),
            },
            {
                "name": "CW Seed",
                "url": "https://cwtv.com/cwseed",
                "description": (
                    "The CW's free streaming platform with full episodes of "
                    "past CW shows and original web series. Great for superhero "
                    "and young-adult drama fans."
                ),
            },
        ],
    },
    "Music": {
        "emoji": "\U0001f3b5",
        "platforms": [
            {
                "name": "YouTube Music (Free)",
                "url": "https://music.youtube.com",
                "description": (
                    "Access to YouTube's entire music library for free with ads. "
                    "Supports playlists, recommendations, artist radio. Works on "
                    "all devices. The largest free music catalog available."
                ),
            },
            {
                "name": "SoundCloud",
                "url": "https://soundcloud.com",
                "description": (
                    "The go-to platform for independent and emerging artists. "
                    "Millions of tracks available for free streaming. Essential for "
                    "discovering new music, remixes, and DJ sets."
                ),
            },
            {
                "name": "Bandcamp",
                "url": "https://bandcamp.com",
                "description": (
                    "Support artists directly. Many tracks are free to stream and "
                    "some offer free downloads. Incredible for indie, jazz, "
                    "electronic, metal, and experimental music discovery."
                ),
            },
            {
                "name": "Spotify (Free Tier)",
                "url": "https://spotify.com",
                "description": (
                    "Free ad-supported music streaming with access to millions "
                    "of songs. Includes curated playlists, podcasts, and "
                    "personalized recommendations. Shuffle-only on mobile."
                ),
            },
            {
                "name": "Pandora",
                "url": "https://pandora.com",
                "description": (
                    "Pioneer of internet radio with the Music Genome Project. "
                    "Create stations based on songs, artists, or genres. Free tier "
                    "with ads. Excellent for passive listening and discovery."
                ),
            },
        ],
    },
    "Podcasts": {
        "emoji": "\U0001f399\ufe0f",
        "platforms": [
            {
                "name": "Spotify Podcasts",
                "url": "https://spotify.com/podcasts",
                "description": (
                    "Massive free podcast library with built-in player. "
                    "Thousands of shows from news and comedy to science and "
                    "true crime. Download for offline listening on mobile."
                ),
            },
            {
                "name": "Apple Podcasts (Web)",
                "url": "https://podcasts.apple.com",
                "description": (
                    "The largest podcast directory, accessible via web. Free "
                    "to browse and listen to virtually any podcast. Includes "
                    "charts, categories, and editorial picks."
                ),
            },
            {
                "name": "YouTube Podcasts",
                "url": "https://youtube.com/podcasts",
                "description": (
                    "YouTube's dedicated podcast hub. Many podcasts publish "
                    "video versions here. Great for long-form interviews, "
                    "educational content, and talk shows."
                ),
            },
            {
                "name": "Pocket Casts (Free Web)",
                "url": "https://pocketcasts.com",
                "description": (
                    "Excellent podcast player with free web access. Supports "
                    "variable speed, trim silence, and cross-device sync. "
                    "Discover new shows through curated recommendations."
                ),
            },
            {
                "name": "iHeartRadio Podcasts",
                "url": "https://iheart.com/podcasts",
                "description": (
                    "Free access to thousands of podcasts including iHeart's "
                    "original shows. Includes top charts by category and "
                    "personalized recommendations."
                ),
            },
        ],
    },
    "Books": {
        "emoji": "\U0001f4da",
        "platforms": [
            {
                "name": "Project Gutenberg",
                "url": "https://gutenberg.org",
                "description": (
                    "Over 70,000 free ebooks — the definitive source for public "
                    "domain literature. Classic novels, poetry, essays, and "
                    "historical texts. Available in EPUB, Kindle, HTML, and plain "
                    "text formats."
                ),
            },
            {
                "name": "Open Library",
                "url": "https://openlibrary.org",
                "description": (
                    "Internet Archive's lending library with over 4 million ebooks "
                    "available to borrow for free. Includes modern titles through "
                    "a controlled digital lending program. Sign up for a free card."
                ),
            },
            {
                "name": "Librivox",
                "url": "https://librivox.org",
                "description": (
                    "Free audiobooks of public domain texts, read by volunteers. "
                    "Over 16,000 titles. Perfect for commuting, exercising, or "
                    "relaxing. Available as MP3 downloads or streaming."
                ),
            },
            {
                "name": "Smashwords (Free)",
                "url": "https://smashwords.com",
                "description": (
                    "Indie ebook distributor with a large free section. Thousands "
                    "of free books across all genres from self-published authors. "
                    "Download in multiple formats including EPUB and Kindle."
                ),
            },
            {
                "name": "Standard Ebooks",
                "url": "https://standardebooks.org",
                "description": (
                    "Beautifully typeset public domain ebooks with modern "
                    "formatting, covers, and typography. Higher quality than "
                    "Gutenberg's raw files. Great for serious readers."
                ),
            },
        ],
    },
    "Games": {
        "emoji": "\U0001f3ae",
        "platforms": [
            {
                "name": "itch.io",
                "url": "https://itch.io",
                "description": (
                    "The indie game paradise. Thousands of free browser and "
                    "downloadable games from independent developers. Includes "
                    "game jams, experimental titles, and hidden gems across "
                    "every genre imaginable."
                ),
            },
            {
                "name": "Steam (Free-to-Play)",
                "url": "https://store.steampowered.com/genre/Free%20to%20Play",
                "description": (
                    "Hundreds of quality free-to-play games on Steam. From "
                    "Fortnite and Apex Legends to indie gems. Community reviews "
                    "help you find the best titles."
                ),
            },
            {
                "name": "Kongregate",
                "url": "https://kongregate.com",
                "description": (
                    "Classic browser gaming portal with thousands of free games. "
                    "Strong catalog of strategy, RPG, puzzle, and idle games. "
                    "Achievement system and community features."
                ),
            },
            {
                "name": "Poki",
                "url": "https://poki.com",
                "description": (
                    "Modern web gaming platform with curated free games optimized "
                    "for browser play. No downloads required. Includes popular "
                    "HTML5 games, .io games, and casual titles."
                ),
            },
            {
                "name": "Epic Games Store (Free Games)",
                "url": "https://store.epicgames.com/free",
                "description": (
                    "Weekly free game giveaways — often premium titles. Past "
                    "freebies include GTA V, Subnautica, Celeste, and more. "
                    "Claim weekly to build your library."
                ),
            },
        ],
    },
    "Documentaries": {
        "emoji": "\U0001f30f",
        "platforms": [
            {
                "name": "YouTube Documentaries",
                "url": "https://youtube.com/results?search_query=documentary",
                "description": (
                    "Endless free documentaries on every topic imaginable. "
                    "Channels like Vox, Vice, BBC, National Geographic, and "
                    "thousands of independent filmmakers upload full-length docs."
                ),
            },
            {
                "name": "Tubi Documentaries",
                "url": "https://tubitv.com/categories/documentaries",
                "description": (
                    "Extensive free documentary library. Categories include nature, "
                    "true crime, history, science, biography, and sports. "
                    "Includes award-winning independent documentaries."
                ),
            },
            {
                "name": "Pluto TV Documentary Channels",
                "url": "https://pluto.tv",
                "description": (
                    "Live documentary channels including BBC Documentaries, "
                    "Discovery, Science, and Nature channels. Always something "
                    "on — perfect for passive documentary watching."
                ),
            },
            {
                "name": "NASA YouTube Channel",
                "url": "https://youtube.com/@NASA",
                "description": (
                    "Free space and science documentaries from NASA. Includes "
                    "live ISS feeds, rocket launches, mission briefings, and "
                    "produced documentary series about space exploration."
                ),
            },
            {
                "name": "Internet Archive",
                "url": "https://archive.org/details/documentaries",
                "description": (
                    "Thousands of free documentaries, educational films, and "
                    "public domain content. Includes vintage educational films "
                    "and modern independent productions."
                ),
            },
        ],
    },
    "Learning": {
        "emoji": "\U0001f393",
        "platforms": [
            {
                "name": "Khan Academy",
                "url": "https://khanacademy.org",
                "description": (
                    "World-class free education. Math, science, computing, "
                    "history, economics, and test prep. Interactive exercises, "
                    "video lessons, and progress tracking. Used by millions."
                ),
            },
            {
                "name": "MIT OpenCourseWare",
                "url": "https://ocw.mit.edu",
                "description": (
                    "Free access to virtually all MIT course content — lectures, "
                    "assignments, exams. Computer science, physics, math, and more. "
                    "University-level education at zero cost."
                ),
            },
            {
                "name": "Coursera (Audit)",
                "url": "https://coursera.org",
                "description": (
                    "Audit thousands of university courses for free from Stanford, "
                    "Yale, Google, IBM, and more. Access video lectures and "
                    "reading materials without paying for certificates."
                ),
            },
            {
                "name": "YouTube Edu",
                "url": "https://youtube.com/education",
                "description": (
                    "YouTube's education hub with content from CrashCourse, "
                    "TED-Ed, Kurzgesagt, Numberphile, and hundreds of "
                    "educational creators. Learn anything for free."
                ),
            },
            {
                "name": "freeCodeCamp",
                "url": "https://freecodecamp.org",
                "description": (
                    "Full-stack web development curriculum, completely free. "
                    "Python, JavaScript, data science, and more. Certifications "
                    "included. Interactive coding challenges and projects."
                ),
            },
        ],
    },
}


def generate_html(preferences=None):
    """Build the full HTML dashboard as a string."""
    now = datetime.now().strftime("%B %d, %Y")

    # Highlight categories matching preferences
    highlighted = set()
    if preferences:
        highlighted = {p.strip().lower() for p in preferences if p.strip()}

    # --- CSS ---
    css = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: #0b0b0f;
        color: #e0e0e0;
        line-height: 1.6;
    }
    .header {
        background: linear-gradient(135deg, #e50914 0%, #831010 50%, #1db954 100%);
        padding: 40px 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        animation: drift 20s linear infinite;
    }
    @keyframes drift {
        0% { transform: translate(0, 0); }
        100% { transform: translate(30px, 30px); }
    }
    .header h1 {
        font-size: 2.8em;
        font-weight: 800;
        color: #fff;
        text-shadow: 0 2px 20px rgba(0,0,0,0.5);
        position: relative;
        z-index: 1;
    }
    .header p {
        font-size: 1.1em;
        color: rgba(255,255,255,0.85);
        margin-top: 10px;
        position: relative;
        z-index: 1;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 30px 20px;
    }
    .category {
        margin-bottom: 40px;
        border-radius: 16px;
        overflow: hidden;
        background: #141420;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }
    .category.highlighted {
        outline: 2px solid #1db954;
        outline-offset: 2px;
    }
    .category-header {
        padding: 20px 28px;
        font-size: 1.5em;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid #222233;
    }
    .platforms {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 0;
    }
    .platform {
        padding: 24px 28px;
        border-bottom: 1px solid #1a1a2e;
        transition: background 0.2s;
    }
    .platform:hover {
        background: #1a1a2e;
    }
    .platform h3 {
        font-size: 1.15em;
        margin-bottom: 6px;
    }
    .platform h3 a {
        color: #1db954;
        text-decoration: none;
    }
    .platform h3 a:hover {
        text-decoration: underline;
    }
    .platform p {
        color: #a0a0b0;
        font-size: 0.92em;
    }
    .footer {
        text-align: center;
        padding: 40px 20px;
        color: #555;
        font-size: 0.9em;
    }
    @media (max-width: 768px) {
        .header h1 { font-size: 1.8em; }
        .platforms { grid-template-columns: 1fr; }
    }
    """

    # --- Body ---
    parts = []
    parts.append(f"<!DOCTYPE html>\n<html lang='en'>\n<head>")
    parts.append(f"  <meta charset='UTF-8'>")
    parts.append(f"  <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
    parts.append(f"  <title>My Free Entertainment Hub</title>")
    parts.append(f"  <style>{css}</style>")
    parts.append(f"</head>\n<body>")

    # Header
    parts.append('  <div class="header">')
    parts.append('    <h1>\U0001f680 My Free Entertainment Hub</h1>')
    parts.append(f'    <p>Your guide to the best free entertainment on the internet &mdash; updated {now}</p>')
    parts.append("  </div>")

    if highlighted:
        parts.append('  <div class="container"><p style="margin-bottom:20px;color:#1db954;">')
        parts.append(f"  \u2b50 Highlighted for your interests: {', '.join(sorted(highlighted))}")
        parts.append("  </p>")
    else:
        parts.append('  <div class="container">')

    for cat_name, cat_data in CATEGORIES.items():
        is_highlighted = cat_name.lower() in highlighted
        cls = "category highlighted" if is_highlighted else "category"
        parts.append(f'  <section class="{cls}">')
        parts.append(f'    <div class="category-header">{cat_data["emoji"]} {cat_name}</div>')
        parts.append('    <div class="platforms">')
        for plat in cat_data["platforms"]:
            parts.append('      <div class="platform">')
            parts.append(f'        <h3><a href="{plat["url"]}" target="_blank">{plat["name"]}</a></h3>')
            parts.append(f'        <p>{plat["description"]}</p>')
            parts.append("      </div>")
        parts.append("    </div>")
        parts.append("  </section>")

    parts.append("  </div>")
    parts.append('  <div class="footer">')
    parts.append(f'    <p>\u0001f3a5 My Free Entertainment Hub &mdash; Generated {now}</p>')
    parts.append("  </div>")
    parts.append("</body>\n</html>")

    return "\n".join(parts)


def generate_markdown(preferences=None):
    """Build the dashboard as structured markdown."""
    now = datetime.now().strftime("%B %d, %Y")

    highlighted = set()
    if preferences:
        highlighted = {p.strip().lower() for p in preferences if p.strip()}

    lines = []
    lines.append(f"# \U0001f680 My Free Entertainment Hub")
    lines.append(f"\n*Your guide to the best free entertainment on the internet \u2014 updated {now}*\n")

    if highlighted:
        lines.append(f"**\u2b50 Highlighted for your interests:** {', '.join(sorted(highlighted))}\n")
        lines.append("---\n")

    for cat_name, cat_data in CATEGORIES.items():
        is_highlighted = cat_name.lower() in highlighted
        marker = " \u2b50" if is_highlighted else ""
        lines.append(f"## {cat_data['emoji']} {cat_name}{marker}\n")
        for plat in cat_data["platforms"]:
            lines.append(f"### [{plat['name']}]({plat['url']})\n")
            lines.append(f"{plat['description']}\n")

    lines.append("---\n")
    lines.append(f"*Generated on {now} by the Entertainment Dashboard Builder*\n")

    return "\n".join(lines)


def main():
    """Parse arguments and generate the entertainment dashboard."""
    parser = argparse.ArgumentParser(
        description="Generate a comprehensive free entertainment dashboard.",
        epilog="Example: python dashboard_builder.py --output hub.html --preferences 'movies,music,games'",
    )
    parser.add_argument(
        "--output",
        default="dashboard.html",
        help="Output file path (default: dashboard.html)",
    )
    parser.add_argument(
        "--format",
        choices=["html", "markdown"],
        default="html",
        help="Output format: html or markdown (default: html)",
    )
    parser.add_argument(
        "--preferences",
        default="",
        help="Comma-separated interests to highlight (e.g. 'movies,music,games')",
    )

    args = parser.parse_args()

    preferences = [p.strip() for p in args.preferences.split(",") if p.strip()] if args.preferences else None

    try:
        if args.format == "html":
            content = generate_html(preferences=preferences)
        else:
            content = generate_markdown(preferences=preferences)

        # Ensure output directory exists
        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)

        abs_path = os.path.abspath(args.output)
        cat_count = len(CATEGORIES)
        plat_count = sum(len(c["platforms"]) for c in CATEGORIES.values())

        print(f"\n{'='*60}")
        print(f"  Entertainment Dashboard Generated Successfully!")
        print(f"{'='*60}")
        print(f"  \U0001f4c4 Format:   {args.format.upper()}")
        print(f"  \U0001f4c1 File:     {abs_path}")
        print(f"  \U0001f3af Categories: {cat_count}")
        print(f"  \U0001f3af Platforms:  {plat_count}")
        if preferences:
            print(f"  \u2b50 Highlighted: {', '.join(preferences)}")
        print(f"{'='*60}\n")

    except PermissionError:
        print(f"Error: Permission denied writing to '{args.output}'.", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: Could not write file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
