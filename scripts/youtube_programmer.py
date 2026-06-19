#!/usr/bin/env python3
"""
YouTube-to-Netflix Programmer
==============================
Generates a Netflix-style 7-day viewing schedule for YouTube channels organized
by categories. Creates daily viewing blocks (morning/afternoon/evening), channel
recommendations with search terms, and a trending section.

Usage:
    python youtube_programmer.py --categories "documentaries,comedy,tech,food"
    python youtube_programmer.py --days 14 --output two_week_schedule.md
"""

import argparse
import sys
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Channel database by category
# Each category has 6+ real channels with descriptions and search terms
# ---------------------------------------------------------------------------
CHANNEL_DATA = {
    "documentaries": {
        "emoji": "\U0001f3ac",
        "channels": [
            {"name": "Vox", "desc": "Explains the world through compelling visual storytelling", "search": "Vox documentary"},
            {"name": "Johnny Harris", "desc": "Beautifully produced video essays on geopolitics and culture", "search": "Johnny Harris video essay"},
            {"name": "Veritasium", "desc": "Science and engineering explained with stunning experiments", "search": "Veritasium science documentary"},
            {"name": "RealLifeLore", "desc": "Maps, data, and global stories presented visually", "search": "RealLifeLore documentary"},
            {"name": "TLDR News", "desc": "Quick, well-researched explainers on global news events", "search": "TLDR News explained"},
            {"name": "Nebula Originals", "desc": "Premium documentary content from top YouTubers (free samples on YT)", "search": "Nebula documentary YouTube"},
        ],
    },
    "comedy": {
        "emoji": "\U0001f602",
        "channels": [
            {"name": "Abdullah Saafir / NigaHiga", "desc": "Classic YouTube comedy with sketches and parodies", "search": "NigaHiga comedy sketch"},
            {"name": "Ryan George", "desc": "Hilarious 'Screen Rant' pitch meetings and movie breakdowns", "search": "Ryan George pitch meeting"},
            {"name": "Drew Gooden", "desc": "Sharp commentary on internet culture and bad content", "search": "Drew Gooden commentary"},
            {"name": "Jenna Marbles (archived)", "desc": "Iconic comedy content spanning a decade of YouTube", "search": "Jenna Marbles best videos"},
            {"name": "Cody Ko", "desc": "Witty commentary and reaction videos with great chemistry", "search": "Cody Ko commentary video"},
            {"name": "Yes Theory", "desc": "Seeking discomfort through travel and challenge videos", "search": "Yes Theory documentary challenge"},
        ],
    },
    "travel": {
        "emoji": "\u2708\ufe0f",
        "channels": [
            {"name": "Bald and Bankrupt", "desc": "Off-the-beaten-path travel to post-Soviet countries", "search": "Bald and Bankrupt travel"},
            {"name": "Kara and Nate", "desc": "Couple traveling to every country in the world", "search": "Kara and Nate travel vlog"},
            {"name": "Mark Wiens", "desc": "Street food and travel across Asia and beyond", "search": "Mark Wiens street food travel"},
            {"name": "Indigo Traveller", "desc": "Raw, unfiltered travel to misunderstood countries", "search": "Indigo Traveller documentary"},
            {"name": "Lost LeBlanc", "desc": "Cinematic travel guides and destination tips", "search": "Lost LeBlanc travel guide"},
            {"name": "Globe Trekker (clips)", "desc": "Professional travel show content available on YouTube", "search": "Globe Trekker destination"},
        ],
    },
    "tech": {
        "emoji": "\U0001f4bb",
        "channels": [
            {"name": "Marques Brownlee (MKBHD)", "desc": "The gold standard for tech reviews and product analysis", "search": "MKBHD tech review 2024"},
            {"name": "Linus Tech Tips", "desc": "PC building, tech news, and gadget deep dives", "search": "Linus Tech Tips build"},
            {"name": "The Verge", "desc": "Tech news, reviews, and explainers with a cultural lens", "search": "The Verge tech explainer"},
            {"name": "Fireship", "desc": "100-second code and tech explainers \u2014 rapid learning", "search": "Fireship 100 seconds"},
            {"name": "TechLinked", "desc": "Fast-paced daily tech news roundup", "search": "TechLinked news today"},
            {"name": "Michael Reeves", "desc": "Hilarious robot building and coding comedy", "search": "Michael Reeves robot build"},
        ],
    },
    "food": {
        "emoji": "\U0001f354",
        "channels": [
            {"name": "Babish Culinary Universe", "desc": "Recreating iconic foods from movies and TV shows", "search": "Babish cooking movie food"},
            {"name": "Joshua Weissman", "desc": "From-scratch recipes with meticulous technique", "search": "Joshua Weissman recipe"},
            {"name": "Bon Appétit (classics)", "desc": "Iconic test kitchen videos and pro techniques", "search": "Bon Appetit test kitchen"},
            {"name": "Maangchi", "desc": "The queen of Korean cooking with authentic recipes", "search": "Maangchi Korean recipe"},
            {"name": "Ethan Chlebowski", "desc": "Food science and technique explained beautifully", "search": "Ethan Chlebowski cooking science"},
            {"name": "Adam Ragusea", "desc": "Practical home cooking with honest, no-nonsense approach", "search": "Adam Ragusea home cooking"},
        ],
    },
    "fitness": {
        "emoji": "\U0001f3cb\ufe0f",
        "channels": [
            {"name": "Hybrid Calisthenics", "desc": "Bodyweight fitness from beginner to advanced. Incredibly motivating.", "search": "Hybrid Calisthenics workout"},
            {"name": "AthleanX", "desc": "Jeff Cavaliere's science-backed fitness and injury prevention", "search": "AthleanX exercise science"},
            {"name": "Yoga With Adriene", "desc": "Free yoga for every level and mood. Millions of practitioners.", "search": "Yoga With Adriene class"},
            {"name": " THENX", "desc": "Chris Heria's calisthenics training for street workout", "search": "THENX calisthenics tutorial"},
            {"name": "FitnessBlender", "desc": "Free full-length workout videos with no equipment needed", "search": "FitnessBlender full workout"},
            {"name": "Tom Merrick", "desc": "Mobility, flexibility, and functional movement", "search": "Tom Merrick mobility routine"},
        ],
    },
    "interviews": {
        "emoji": "\U0001f4ac",
        "channels": [
            {"name": "Hot Ones", "desc": "Celebrities eat increasingly spicy wings while answering questions", "search": "Hot Ones interview celebrity"},
            {"name": "The Joe Rogan Experience (clips)", "desc": "Long-form conversations with diverse guests", "search": "Joe Rogan highlights clip"},
            {"name": "Diary of a CEO", "desc": "Steven Bartlett interviews entrepreneurs and cultural figures", "search": "Diary of a CEO interview"},
            {"name": "Graham Bensinger", "desc": "In-depth interviews with athletes, celebrities, and leaders", "search": "Graham Bensinger interview"},
            {"name": "Theory of Everything (TOE)", "desc": "Deep interviews with scientists, philosophers, and thinkers", "search": "Curt Jaimungal TOE interview"},
            {"name": "Lex Fridman (clips)", "desc": "Conversations with AI researchers, scientists, and creators", "search": "Lex Fridman podcast clips"},
        ],
    },
    "cozy": {
        "emoji": "\U0001f9e0",
        "channels": [
            {"name": "Lofi Girl", "desc": "24/7 lo-fi beats to relax/study to. The iconic animated stream.", "search": "Lofi Girl live stream"},
            {"name": "Hazel / Study With Me", "desc": "Ambient study sessions and productive day-in-my-life videos", "search": "Study With Me ambient pomodoro"},
            {"name": "Kirsten Dirksen", "desc": "Tiny houses, simple living, and alternative homes", "search": "Kirsten Dirksen tiny house"},
            {"name": "Andrew Rea (pre-Babish)", "desc": "Comforting cooking content for rainy day viewing", "search": "Babish basics recipe"},
            {"name": "Simple History", "desc": "Animated history summaries perfect for relaxed learning", "search": "Simple History animated"},
            {"name": "Le Floff / Ambience", "desc": "Ambient soundscapes \u2014 rain, coffee shops, fireplaces", "search": "ambient fireplace rain sounds"},
        ],
    },
    "science": {
        "emoji": "\U0001f52c",
        "channels": [
            {"name": "Kurzgesagt", "desc": "Beautiful animated explainers on space, biology, and existential topics", "search": "Kurzgesagt animated science"},
            {"name": "Vsauce", "desc": "Michael Stevens asks deep questions about science and thought experiments", "search": "Vsauce mind field"},
            {"name": "SmarterEveryDay", "desc": "Destin's infectious curiosity applied to engineering and physics", "search": "SmarterEveryDay slow motion"},
            {"name": "Steve Mould", "desc": "Captivating science demonstrations and phenomena explained", "search": "Steve Mould science trick"},
            {"name": "3Blue1Brown", "desc": "Visualizing math and linear algebra in stunning animations", "search": "3Blue1Brown math explained"},
            {"name": "Joe Hanson / It's Okay To Be Smart", "desc": "Accessible, enthusiastic science communication", "search": "It's Okay To Be Smart episode"},
        ],
    },
    "music": {
        "emoji": "\U0001f3b5",
        "channels": [
            {"name": "Polyphonic", "desc": "Video essays on music history and album analysis", "search": "Polyphonic music essay"},
            {"name": "CHON", "desc": "Musical performances and creative guitar content", "search": "CHON music performance"},
            {"name": "Laurence Peril", "desc": "Album reviews and music criticism with depth", "search": "Laurence Peril album review"},
            {"name": "Rick Beato", "desc": "What Makes This Song Great series \u2014 deep music analysis", "search": "Rick Beato what makes great"},
            {"name": "Adam Neely", "desc": "Music theory explained with humor and intelligence", "search": "Adam Neely music theory"},
            {"name": "David Bennett Piano", "desc": "Piano covers and music theory made accessible", "search": "David Bennett piano tutorial"},
        ],
    },
    "gaming": {
        "emoji": "\U0001f3ae",
        "channels": [
            {"name": "Game Maker's Toolkit", "desc": "Design analysis of video games with excellent editing", "search": "Game Maker's Toolkit analysis"},
            {"name": "Super Eyepatch Wolf", "desc": "Deep video essays on gaming culture and specific games", "search": "Super Eyepatch Wolf essay"},
            {"name": "NakeyJakey", "desc": "Humorous, well-researched game design critiques", "search": "NakeyJakey game video essay"},
            {"name": "The Completionist", "desc": "Completing games to 100% with entertaining commentary", "search": "The Completionist review"},
            {"name": "Game Grumps", "desc": "Let's Play comedy with genuine friendship chemistry", "search": "Game Grumps play"},
            {"name": "GNM / Game News Machine", "desc": "Gaming news and industry analysis", "search": "gaming news analysis 2024"},
        ],
    },
    "history": {
        "emoji": "\U0001f3db\ufe0f",
        "channels": [
            {"name": "Oversimplified", "desc": "Animated history with humor and incredible clarity", "search": "Oversimplified history animation"},
            {"name": "CrashCourse History", "desc": "John Green's rapid-fire world history courses", "search": "CrashCourse world history episode"},
            {"name": "Historia Civilis", "desc": "Deep political and military history with maps and strategy", "search": "Historia Civilis ancient"},
            {"name": "Kings and Generals", "desc": "Animated battle maps and military history", "search": "Kings and Generals battle"},
            {"name": "Sabine / TierZoo (historical)", "desc": "Evolutionary and historical content with a gaming lens", "search": "history documentary YouTube"},
            {"name": "Fall of Civilizations", "desc": "Epic, deeply researched series on collapsed civilizations", "search": "Fall of Civilizations episode"},
        ],
    },
}

# ---------------------------------------------------------------------------
# Time blocks per day
# ---------------------------------------------------------------------------
TIME_BLOCKS = {
    "morning": {"emoji": "\u2600\ufe0f", "time": "8:00 AM \u2013 12:00 PM", "style": "Start your day with lighter, educational content"},
    "afternoon": {"emoji": "\U0001f305", "time": "1:00 PM \u2013 5:00 PM", "style": "Mid-day is great for longer-form content and deep dives"},
    "evening": {"emoji": "\U0001f319", "time": "7:00 PM \u2013 10:00 PM", "style": "Wind down with entertainment, interviews, or cozy content"},
}

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ---------------------------------------------------------------------------
# Trending topics (updated periodically)
# ---------------------------------------------------------------------------
TRENDING_TOPICS = [
    "AI and machine learning explainers",
    "Space exploration updates",
    "True crime mini-documentaries",
    "Sustainable living and zero waste",
    "Mental health and wellness content",
    "Cooking on a budget series",
    "Home workout no-equipment challenges",
    "Retro gaming nostalgia content",
    "Van life and alternative housing",
    "Climate science and environmental docs",
]


def generate_schedule(categories, days):
    """Generate the Netflix-style YouTube schedule as markdown."""
    now = datetime.now().strftime("%B %d, %Y")
    cat_list = categories if categories else list(CHANNEL_DATA.keys())
    cycle_length = len(cat_list)

    lines = []
    lines.append(f"# \U0001f4fa Your Personal YouTube Network")
    lines.append(f"*Netflix-style programming for {days} days \u2014 generated {now}*\n")

    # Network overview
    lines.append("## \U0001f4e1 Network Channels\n")
    lines.append("| Category | Channels | Search Terms |")
    lines.append("|----------|----------|-------------|")

    for cat in cat_list:
        if cat not in CHANNEL_DATA:
            continue
        data = CHANNEL_DATA[cat]
        channel_names = ", ".join(ch["name"] for ch in data["channels"][:3])
        search_sample = data["channels"][0]["search"]
        lines.append(f"| {data['emoji']} {cat.title()} | {channel_names} | `{search_sample}` |")
    lines.append("")

    # Weekly schedule
    lines.append("---\n")
    lines.append(f"## \U0001f4c5 {days}-Day Programming Schedule\n")

    for day_idx in range(days):
        day_name = DAY_NAMES[day_idx % 7]
        week_num = day_idx // 7 + 1
        if days > 7:
            lines.append(f"### Week {week_num} \u2014 {day_name}\n")
        else:
            lines.append(f"### {day_name}\n")

        # Assign 3 different categories to the 3 time blocks
        for block_idx, (block_name, block_info) in enumerate(TIME_BLOCKS.items()):
            cat_idx = (day_idx * 3 + block_idx) % cycle_length
            cat_name = cat_list[cat_idx % len(cat_list)]

            if cat_name not in CHANNEL_DATA:
                continue

            cat_data = CHANNEL_DATA[cat_name]
            # Pick different channels for each block
            ch_indices = [(day_idx * 3 + block_idx + offset) % len(cat_data["channels"]) for offset in range(3)]
            channels_for_block = [cat_data["channels"][i] for i in ch_indices]

            lines.append(f"**{block_info['emoji']} {block_name.capitalize()} ({block_info['time']})**")
            lines.append(f"*{block_info['style']}*\n")

            for ch in channels_for_block:
                lines.append(f"- \U0001f4fc **{ch['name']}** \u2014 {ch['desc']}")
                lines.append(f"  \u2500 Search: `{ch['search']}`")
            lines.append("")

        lines.append("---\n")

    # Category deep-dive section
    lines.append("## \U0001f50d Category Deep Dives\n")

    for cat in cat_list:
        if cat not in CHANNEL_DATA:
            continue
        data = CHANNEL_DATA[cat]
        lines.append(f"### {data['emoji']} {cat.title()}\n")
        lines.append("| Channel | Description | Search Term |")
        lines.append("|---------|-------------|-------------|")
        for ch in data["channels"]:
            lines.append(f"| {ch['name']} | {ch['desc']} | `{ch['search']}` |")
        lines.append("")

    # Trending section
    lines.append("---\n")
    lines.append("## \U0001f525 Trending This Season\n")
    lines.append("Search these topics on YouTube to discover the latest viral content:\n")
    for topic in TRENDING_TOPICS:
        lines.append(f"- \U0001f4a1 **{topic}** \u2014 `youtube.com/results?search_query={topic.lower().replace(' ', '+')}`")
    lines.append("")

    # Tips
    lines.append("---\n")
    lines.append("## \U0001f4a1 YouTube Programming Tips\n")
    lines.append("- **Use YouTube's Watch Later** feature to queue up your week's content on Sunday.")
    lines.append("- **Create playlists** for each category so YouTube's algorithm feeds you more of what you like.")
    lines.append("- **Enable Restricted Mode** for family-friendly browsing during morning blocks.")
    lines.append("- **Use the timer** \u2014 YouTube lets you set a reminder to take a break.")
    lines.append("- **Download offline** \u2014 Premium-free users can still use the YouTube app to watch downloaded content.")
    lines.append("- **Follow playlists** curated by the channels above for a continuous viewing experience.")
    lines.append("")

    lines.append(f"*\U0001f4fa Happy watching! \u2014 Generated {now}*\n")

    return "\n".join(lines)


def main():
    """Parse arguments and generate the YouTube schedule."""
    parser = argparse.ArgumentParser(
        description="Generate a Netflix-style YouTube viewing schedule organized by categories.",
        epilog="Example: python youtube_programmer.py --categories 'documentaries,comedy,tech,food' --days 7",
    )
    parser.add_argument(
        "--categories",
        default="documentaries,comedy,travel,tech,food,fitness,interviews,cozy",
        help="Comma-separated content categories (default: documentaries,comedy,travel,tech,food,fitness,interviews,cozy)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to program (default: 7)",
    )
    parser.add_argument(
        "--output",
        default="youtube_schedule.md",
        help="Output markdown file path (default: youtube_schedule.md)",
    )

    args = parser.parse_args()

    categories = [c.strip().lower() for c in args.categories.split(",") if c.strip()]

    # Validate categories
    valid = list(CHANNEL_DATA.keys())
    invalid = [c for c in categories if c not in valid]
    if invalid:
        print(f"Warning: Unknown categories ignored: {', '.join(invalid)}", file=sys.stderr)
        categories = [c for c in categories if c in valid]

    if not categories:
        categories = valid
        print(f"Info: Using all available categories: {', '.join(valid)}", file=sys.stderr)

    if args.days < 1 or args.days > 30:
        print("Error: --days must be between 1 and 30.", file=sys.stderr)
        sys.exit(1)

    try:
        content = generate_schedule(categories=categories, days=args.days)

        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)

        abs_path = os.path.abspath(args.output)
        total_channels = sum(len(CHANNEL_DATA[c]["channels"]) for c in categories if c in CHANNEL_DATA)

        print(f"\n{'='*60}")
        print(f"  \U0001f4fa YouTube Network Programmed Successfully!")
        print(f"{'='*60}")
        print(f"  \U0001f4c4 File:      {abs_path}")
        print(f"  \U0001f4c5 Days:      {args.days}")
        print(f"  \U0001f3af Categories: {len(categories)}")
        print(f"  \U0001f4fc Channels:  {total_channels}")
        print(f"  \u23f0 Blocks/day: 3 (morning/afternoon/evening)")
        print(f"{'='*60}\n")

    except PermissionError:
        print(f"Error: Permission denied writing to '{args.output}'.", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: Could not write file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
