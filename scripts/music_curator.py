#!/usr/bin/env python3
"""
Personal Music Curator
======================
Generates a weekly music plan with mood-based playlists tailored to different
activities throughout the week. Recommends free platforms (YouTube Music,
SoundCloud, Bandcamp) and provides specific search terms, channels, and artists.

Usage:
    python music_curator.py --artists "Tame Impala, Daft Punk" --genres "electronic,rock"
    python music_curator.py --moods "chill,focus,workout" --output my_plan.md
"""

import argparse
import sys
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Mood → activity mapping used across the week
# ---------------------------------------------------------------------------
MOOD_SCHEDULE = {
    "Monday":    {"mood": "Focus",       "emoji": "\U0001f4bb", "desc": "Start the week with concentration"},
    "Tuesday":   {"mood": "Deep Work",   "emoji": "\U0001f52c", "desc": "Flow-state productivity music"},
    "Wednesday": {"mood": "Chill",       "emoji": "\u2615", "desc": "Midweek relaxation"},
    "Thursday":  {"mood": "Workout",     "emoji": "\U0001f3cb\ufe0f", "desc": "Energy boost for exercise"},
    "Friday":    {"mood": "Cooking",     "emoji": "\U0001f373", "desc": "Fun dinner prep vibes"},
    "Saturday":  {"mood": "Exploration",  "emoji": "\U0001f30d", "desc": "Discover something new"},
    "Sunday":    {"mood": "Night",       "emoji": "\U0001f319", "desc": "Wind down before Monday"},
}

# ---------------------------------------------------------------------------
# Mood → playlist data (genres, search terms, platform recommendations)
# ---------------------------------------------------------------------------
MOOD_PLAYLISTS = {
    "Focus": {
        "emoji": "\U0001f4bb",
        "genres": ["lo-fi beats", "ambient", "classical", "minimal electronic", "post-rock"],
        "search_terms": [
            "lo-fi hip hop beats to study to",
            "ambient focus music no lyrics",
            "classical music for concentration",
            "minimal techno deep focus",
            "post-rock instrumental study",
        ],
        "youtube_music_channels": [
            "ChilledCow / Lofi Girl",
            "Ambient",
            "HALIENE",
            "MrSuicideSheep",
        ],
        "soundcloud_artists": [
            "Kupla",
            "j'san",
            "idealism",
            "in love with a ghost",
        ],
        "bandcamp_recommendations": [
            "Albums tagged 'lo-fi' on Bandcamp",
            "Tycho \u2014 Dive (or any Tycho album)",
            "Bing & Ruth \u2014 No Home of the Mind",
        ],
        "tip": "Keep BPM between 60-90 for optimal focus. Avoid lyrics during deep concentration tasks.",
    },
    "Deep Work": {
        "emoji": "\U0001f52c",
        "genres": ["drone", "dark ambient", "binaural beats", "space music", "new age"],
        "search_terms": [
            "binaural beats for deep work",
            "dark ambient background music",
            "space ambient concentration",
            "tibetan singing bowl meditation focus",
            "isochronic tones productivity",
        ],
        "youtube_music_channels": [
            "The Honest Guys",
            "Meditative Mind",
            "YellowBrickCinema",
            "Relax Melodies",
        ],
        "soundcloud_artists": [
            "Stars of the Lid",
            "Brian Eno",
            "William Basinski",
            "Tim Hecker",
        ],
        "bandcamp_recommendations": [
            "Brian Eno \u2014 Music for Airports",
            "Stars of the Lid \u2014 And Their Refinement of the Decline",
            "A Winged Victory for the Sullen",
        ],
        "tip": "Use noise-cancelling headphones. Drone and binaural beats can sustain focus for 90-minute blocks.",
    },
    "Chill": {
        "emoji": "\u2615",
        "genres": ["indie folk", "bossa nova", "jazz", "soft rock", "acoustic"],
        "search_terms": [
            "chill indie folk playlist",
            "bossa nova coffee morning",
            "jazz cafe background music",
            "acoustic covers popular songs",
            "chillwave sunset playlist",
        ],
        "youtube_music_channels": [
            "Chill Nation",
            "Jazz Lounge Music",
            "Bossa Nova Lounge",
            "The Vibe Guide",
        ],
        "soundcloud_artists": [
            "Mac DeMarco",
            "Mazzy Star",
            "Norah Jones",
            "Bon Iver",
        ],
        "bandcamp_recommendations": [
            "Sufjan Stevens \u2014 Carrie & Lowell",
            "Nick Drake \u2014 Pink Moon",
            "Iron & Wine \u2014 Our Endless Numbered Days",
        ],
        "tip": "Pair with coffee or tea. Acoustic instruments and warm vocals create a cozy atmosphere.",
    },
    "Workout": {
        "emoji": "\U0001f3cb\ufe0f",
        "genres": ["hip-hop", "EDM", "drum and bass", "rock", "trap"],
        "search_terms": [
            "workout music motivation 2024",
            "drum and bass gym playlist",
            "hip-hop running playlist",
            "EDM cardio mix",
            "rock workout anthems",
        ],
        "youtube_music_channels": [
            "FitLife Music",
            "Workout Music Station",
            "Trap Nation",
            "Monstercat",
        ],
        "soundcloud_artists": [
            "Skrillex",
            "Excision",
            "Noisia",
            "Sub Focus",
        ],
        "bandcamp_recommendations": [
            "The Prodigy \u2014 The Fat of the Land",
            "Pendulum \u2014 Immersion",
            " various artists on 'Monstercat' label",
        ],
        "tip": "Aim for 140-170 BPM for cardio, 120-140 for weight training. Build intensity throughout the set.",
    },
    "Cooking": {
        "emoji": "\U0001f373",
        "genres": ["soul", "reggae", "funk", "Latin", "world music"],
        "search_terms": [
            "cooking music feel good playlist",
            "reggae dinner party music",
            "funk and soul kitchen playlist",
            "latin jazz cooking vibes",
            "french cafe music cooking",
        ],
        "youtube_music_channels": [
            "Funky Kitchen",
            "Cafe Music BGM",
            "Soul Kitchen",
            "Tropkillaz",
        ],
        "soundcloud_artists": [
            "Curtis Mayfield",
            "Bob Marley",
            "Buena Vista Social Club",
            "A Tribe Called Quest",
        ],
        "bandcamp_recommendations": [
            "Herbie Hancock \u2014 Head Hunters",
            "Santana \u2014 Abraxas",
            "Fela Kuti \u2014 Zombie",
        ],
        "tip": "Cooking playlists should be groovy but not overwhelming \u2014 you want to enjoy the process!",
    },
    "Exploration": {
        "emoji": "\U0001f30d",
        "genres": ["psychedelic", "world", "experimental", "krautrock", "afrobeat"],
        "search_terms": [
            "psychedelic rock discovery playlist",
            "afrobeat music introduction",
            "krautrock for beginners",
            "world music fusion playlist",
            "experimental electronic new artists",
        ],
        "youtube_music_channels": [
            "Psychedelic Pills",
            "Wonderful Music",
            "Music for the Soul",
            "Afrobeat Radio",
        ],
        "soundcloud_artists": [
            "Khruangbin",
            "King Gizzard & the Lizard Wizard",
            "Mild High Club",
            "Men I Trust",
        ],
        "bandcamp_recommendations": [
            "Khruangbin \u2014 Con Todo el Mundo",
            "Can \u2014 Ege Bamyasi",
            "Fela Kuti \u2014 Expensive Shit",
        ],
        "tip": "Saturdays are for musical adventure. Follow recommendations rabbit holes \u2014 skip what you don't like!",
    },
    "Night": {
        "emoji": "\U0001f319",
        "genres": ["dream pop", "R&B", "slow jams", "neo-soul", "trip-hop"],
        "search_terms": [
            "dream pop night playlist",
            "R&B slow jams evening",
            "neo-soul bedtime music",
            "trip-hop late night vibes",
            "piano lullaby peaceful sleep",
        ],
        "youtube_music_channels": [
            "Dream Pop",
            "Late Night Tales",
            "The Soulful Lounge",
            "Sleeping Music",
        ],
        "soundcloud_artists": [
            "Massive Attack",
            "Portishead",
            "Frank Ocean",
            "SZA",
        ],
        "bandcamp_recommendations": [
            "Massive Attack \u2014 Mezzanine",
            "Cocteau Twins \u2014 Heaven or Las Vegas",
            "Beach House \u2014 Bloom",
        ],
        "tip": "Gradually decrease tempo as the evening progresses. Transition from dream pop to ambient by midnight.",
    },
}

# ---------------------------------------------------------------------------
# Genre → bonus discovery search terms
# ---------------------------------------------------------------------------
GENRE_EXTRAS = {
    "electronic": {
        "terms": ["synthwave playlist", "deep house radio", "IDM experimental electronic"],
        "note": "Explore sub-genres: ambient techno, dub techno, acid house",
    },
    "rock": {
        "terms": ["classic rock essentials", "post-punk revival playlist", "stoner rock"],
        "note": "Check out math rock for complex rhythms",
    },
    "hip-hop": {
        "terms": ["underground hip-hop playlist", "jazz rap instrumental", "lo-fi hip hop beats"],
        "note": "Don't sleep on underground and indie hip-hop scenes",
    },
    "jazz": {
        "terms": ["jazz fusion essentials", "modal jazz playlist", "cool jazz classics"],
        "note": "Start with Miles Davis' Kind of Blue, then explore from there",
    },
    "classical": {
        "terms": ["romantic era piano pieces", "baroque classical essentials", "modern classical"],
        "note": "Explore contemporary classical like Nils Frahm and Olafur Arnalds",
    },
    "pop": {
        "terms": ["indie pop playlist", "synth pop essentials", "bedroom pop chill"],
        "note": "Indie pop often has more musical depth than mainstream pop",
    },
    "metal": {
        "terms": ["progressive metal playlist", "doom metal essentials", "black metal atmospheric"],
        "note": "Explore bands between genres \u2014 death-doom, black-thrash, etc.",
    },
    "folk": {
        "terms": ["contemporary folk playlist", "folk punk energy", "celtic folk traditional"],
        "note": "Explore folk from different cultures for fresh sounds",
    },
    "blues": {
        "terms": ["delta blues essentials", "chicago blues electric", "modern blues rock"],
        "note": "Chicago blues is great entry point; then explore Texas and Delta styles",
    },
    "r-and-b": {
        "terms": ["neo-soul essentials", "alternative R&B playlist", "90s R&B slow jams"],
        "note": "90s R&B is a goldmine \u2014 Erykah Badu, D'Angelo, Lauryn Hill",
    },
    "country": {
        "terms": ["outlaw country classics", "alt-country playlist", "country folk americana"],
        "note": "Alt-country and americana scenes have incredible songwriting",
    },
    "reggae": {
        "terms": ["roots reggae essentials", "dub reggae playlist", "dancehall classic"],
        "note": "Lee 'Scratch' Perry productions are essential listening",
    },
    "ambient": {
        "terms": ["dark ambient playlist", "space ambient cosmic", "ambient classical drone"],
        "note": "Perfect for reading, meditation, or falling asleep",
    },
    "punk": {
        "terms": ["post-punk essentials", "hardcore punk energy", "anarcho punk playlist"],
        "note": "Post-punk revival (2000s) bridges punk and new wave beautifully",
    },
}

# ---------------------------------------------------------------------------
# Artist → similar discovery suggestions
# ---------------------------------------------------------------------------
ARTIST_SUGGESTIONS = {
    "tame impala": "Try: Pond, Melody's Echo Chamber, King Gizzard, MGMT, Unknown Mortal Orchestra",
    "daft punk": "Try: Justice, Cassius, Stardust, Breakbot, Kavinsky",
    "radiohead": "Try: Muse (early), Sigur Rós, Björk, Portishead, Scott Walker (later)",
    "beatles": "Try: The Kinks, The Byrds, Big Star, Badfinger, ELO",
    "kendrick lamar": "Try: J. Cole, Vince Staples, Isaiah Rashad, Earl Sweatshirt, Ab-Soul",
    "taylor swift": "Try: Phoebe Bridgers, Lucy Dacus, Julien Baker, Ingrid Andress, Lorde",
    "drake": "Try: PARTYNEXTDOOR, Bryson Tiller, 21 Savage, Future, Travis Scott",
}


def discover_artist(name):
    """Return discovery suggestion for a known artist, or a generic tip."""
    key = name.strip().lower()
    if key in ARTIST_SUGGESTIONS:
        return ARTIST_SUGGESTIONS[key]
    return f"Search SoundCloud and Bandcamp for '{name}' and check the 'Fans also like' section."


def generate_plan(artists=None, genres=None, moods=None):
    """Generate the full weekly music plan as markdown."""
    now = datetime.now().strftime("%B %d, %Y")
    lines = []

    lines.append(f"# \U0001f3b5 Weekly Music Plan")
    lines.append(f"*Personalized for your taste \u2014 generated {now}*\n")

    # --- Prefs summary ---
    if artists or genres or moods:
        lines.append("## \u2699\ufe0f Your Preferences\n")
        if artists:
            lines.append(f"- **Artists:** {', '.join(artists)}")
        if genres:
            lines.append(f"- **Genres:** {', '.join(genres)}")
        if moods:
            lines.append(f"- **Preferred Moods:** {', '.join(moods)}")
        lines.append("")

    # --- Artist discovery ---
    if artists:
        lines.append("## \U0001f50d Artist Discovery\n")
        for a in artists:
            lines.append(f"**{a}:** {discover_artist(a)}\n")
        lines.append("")

    # --- Genre extras ---
    if genres:
        lines.append("## \U0001f3b6 Genre Deep Dives\n")
        for g in genres:
            gkey = g.strip().lower()
            if gkey in GENRE_EXTRAS:
                info = GENRE_EXTRAS[gkey]
                lines.append(f"### {g.title()}\n")
                for t in info["terms"]:
                    lines.append(f"- Search: `{t}`")
                lines.append(f"\n> {info['note']}\n")
            else:
                lines.append(f"### {g.title()}\n")
                lines.append(f"- Search: `{g.strip()} playlist 2024`")
                lines.append(f"- Search: `best {g.strip()} artists to discover`\n")
        lines.append("")

    # --- Weekly schedule ---
    lines.append("## \U0001f4c5 Weekly Mood Schedule\n")
    lines.append("| Day | Mood | Description | Key Genres | Search Starters |")
    lines.append("|-----|------|-------------|-----------|-----------------|")

    for day, info in MOOD_SCHEDULE.items():
        playlist = MOOD_PLAYLISTS[info["mood"]]
        genres_str = ", ".join(playlist["genres"][:3])
        search_str = playlist["search_terms"][0]
        lines.append(
            f"| {info['emoji']} {day} | {playlist['emoji']} {info['mood']} | "
            f"{info['desc']} | {genres_str} | `{search_str}` |"
        )
    lines.append("")

    # --- Detailed daily breakdown ---
    lines.append("---\n")
    lines.append("## \U0001f4dd Detailed Daily Playlists\n")

    for day, info in MOOD_SCHEDULE.items():
        pl = MOOD_PLAYLISTS[info["mood"]]
        lines.append(f"### {info['emoji']} {day} \u2014 {pl['emoji']} {info['mood']}\n")

        lines.append("**\U0001f3bc Recommended Genres:**\n")
        for g in pl["genres"]:
            lines.append(f"- {g}")
        lines.append("")

        lines.append("**\U0001f50d Search Terms (paste into YouTube Music / SoundCloud):**\n")
        for st in pl["search_terms"]:
            lines.append(f"- `{st}`")
        lines.append("")

        lines.append("**\U0001fa97 YouTube Music Channels:**\n")
        for ch in pl["youtube_music_channels"]:
            lines.append(f"- {ch}")
        lines.append("")

        lines.append("**\U0001f3a7 SoundCloud Artists:**\n")
        for sc in pl["soundcloud_artists"]:
            lines.append(f"- {sc}")
        lines.append("")

        lines.append("**\U0001f3a5 Bandcamp Picks:**\n")
        for bc in pl["bandcamp_recommendations"]:
            lines.append(f"- {bc}")
        lines.append("")

        lines.append(f"**\U0001f4a1 Pro Tip:** {pl['tip']}\n")
        lines.append("---\n")

    # --- Free Platform Quick-Reference ---
    lines.append("## \U0001f4f1 Free Music Platforms Quick Reference\n")
    lines.append("| Platform | URL | Best For |")
    lines.append("|----------|-----|----------|")
    lines.append("| YouTube Music (Free) | https://music.youtube.com | Largest catalog, playlists, recommendations |")
    lines.append("| SoundCloud | https://soundcloud.com | Indie artists, remixes, new discoveries |")
    lines.append("| Bandcamp | https://bandcamp.com | Supporting artists, deep catalog, free streams |")
    lines.append("| Spotify (Free) | https://spotify.com | Curated playlists, podcasts, mobile app |")
    lines.append("| Pandora | https://pandora.com | Radio stations, passive listening, discovery |")
    lines.append("| Audiomack | https://audiomack.com | Hip-hop, R&B, electronic \u2014 free uploads |")
    lines.append("| Jamendo | https://jamendo.com | Creative Commons music, royalty-free |")
    lines.append("")

    lines.append(f"*\U0001f3b5 Enjoy your personalized music week! \u2014 Generated {now}*\n")

    return "\n".join(lines)


def main():
    """Parse arguments and generate the music plan."""
    parser = argparse.ArgumentParser(
        description="Generate a personalized weekly music plan with mood-based playlists.",
        epilog="Example: python music_curator.py --artists 'Tame Impala' --genres 'electronic,rock' --moods 'focus,chill'",
    )
    parser.add_argument(
        "--artists",
        default="",
        help="Comma-separated favorite artists for discovery suggestions",
    )
    parser.add_argument(
        "--genres",
        default="",
        help="Comma-separated preferred genres for deep-dive recommendations",
    )
    parser.add_argument(
        "--moods",
        default="",
        help="Comma-separated preferred moods (e.g. focus,chill,workout,night)",
    )
    parser.add_argument(
        "--output",
        default="music_plan.md",
        help="Output markdown file path (default: music_plan.md)",
    )

    args = parser.parse_args()

    artists = [a.strip() for a in args.artists.split(",") if a.strip()] if args.artists else None
    genres = [g.strip() for g in args.genres.split(",") if g.strip()] if args.genres else None
    moods = [m.strip() for m in args.moods.split(",") if m.strip()] if args.moods else None

    try:
        content = generate_plan(artists=artists, genres=genres, moods=moods)

        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)

        abs_path = os.path.abspath(args.output)
        print(f"\n{'='*60}")
        print(f"  \U0001f3b5 Music Plan Generated Successfully!")
        print(f"{'='*60}")
        print(f"  \U0001f4c4 File:     {abs_path}")
        if artists:
            print(f"  \U0001f9b4 Artists:  {', '.join(artists)}")
        if genres:
            print(f"  \U0001f3b6 Genres:   {', '.join(genres)}")
        print(f"  \U0001f4c5 Days:     7 (Monday \u2013 Sunday)")
        print(f"  \U0001f3b5 Moods:    {', '.join(MOOD_SCHEDULE[d]['mood'] for d in MOOD_SCHEDULE)}")
        print(f"{'='*60}\n")

    except PermissionError:
        print(f"Error: Permission denied writing to '{args.output}'.", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: Could not write file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
