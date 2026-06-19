#!/usr/bin/env python3
"""
Free Gaming Guide
==================
Finds free games from itch.io, Steam F2P, Kongregate, Poki, CrazyGames, and
Epic Games Store. Categorizes by genre with difficulty ratings, time commitment
estimates, and reasons to play. Includes browser-based games and a weekly schedule.

Usage:
    python gaming_guide.py --platform pc --genres "puzzle,rpg,strategy"
    python gaming_guide.py --platform browser --output browser_games.md
"""

import argparse
import sys
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Free game database organized by genre
# Each entry: title, platforms, difficulty, time_commitment, why_play, url
# ---------------------------------------------------------------------------
GAMES = {
    "puzzle": [
        {"title": "A Short Hike", "platforms": ["itch.io", "Steam"], "difficulty": "Easy",
         "time": "1-3 hours",
         "why": "A delightful hike up a mountain where you help other animal characters. Pure relaxation with surprisingly emotional moments.",
         "url": "https://adrium.itch.io/a-short-hike"},
        {"title": "Baba Is You", "platforms": ["itch.io", "Steam"], "difficulty": "Hard",
         "time": "5-15 hours",
         "why": "You manipulate the rules of the game to solve puzzles. Incredibly innovative \u2014 makes you think in entirely new ways.",
         "url": "https://hempuli.itch.io/baba-is-you"},
        {"title": "Steven's Sausage Roll", "platforms": ["itch.io", "Steam"], "difficulty": "Very Hard",
         "time": "10-20 hours",
         "why": "Push-block puzzles of absurd genius. Stephen's Sausage Roll has some of the most clever puzzle design ever made.",
         "url": "https://store.steampowered.com/app/353570"},
        {"title": "Cookie Clicker", "platforms": ["Browser"], "difficulty": "Easy",
         "time": "Endless",
         "why": "The original idle/clicker game. Deceptively addictive with surprisingly deep upgrades. The grandparent of idle games.",
         "url": "https://orteil.dashnet.org/cookieclicker"},
        {"title": "2048", "platforms": ["Browser"], "difficulty": "Medium",
         "time": "Endless",
         "why": "Slide tiles to combine numbers and reach 2048. Simple to learn, endlessly replayable, and a perfect brain teaser.",
         "url": "https://play2048.co"},
        {"title": "Unpacking", "platforms": ["Steam (demo)"], "difficulty": "Easy",
         "time": "3-5 hours",
         "why": "Unpack boxes and arrange items to tell a life story. The most therapeutic puzzle game you'll ever play. Try the demo for free.",
         "url": "https://store.steampowered.com/app/1173040"},
        {"title": "Mini Metro", "platforms": ["itch.io (demo)"], "difficulty": "Medium",
         "time": "5-10 hours",
         "why": "Design subway maps for growing cities. Elegant minimalism meets spatial strategy. The demo gives you the core experience.",
         "url": "https://dinopoloclub.itch.io/mini-metro"},
        {"title": "Peggle", "platforms": ["Browser"], "difficulty": "Easy",
         "time": "3-5 hours",
         "why": "Peggle meets pinball in this PopCap classic. Pure arcade joy with satisfying physics and the legendary 'Ode to Joy' moment.",
         "url": "https://poki.com/en/search/peggle"},
    ],
    "rpg": [
        {"title": "Dwarf Fortress", "platforms": ["itch.io", "Steam"], "difficulty": "Very Hard",
         "time": "100+ hours",
         "why": "The most complex simulation ever made. Manage a dwarven colony through economics, politics, combat, and existential dread. Free version is feature-complete.",
         "url": "https://www.bay12games.com/dwarves"},
        {"title": "Caves of Qud", "platforms": ["Steam (free version)"], "difficulty": "Hard",
         "time": "20-100 hours",
         "why": "A deeply weird roguelike RPG in a post-apocalyptic world of mutant plants, chrome-plated creatures, and water-merchant politics.",
         "url": "https://freeholdgames.itch.io/caves-of-qud-free"},
        {"title": "A Dark Room", "platforms": ["Browser"], "difficulty": "Medium",
         "time": "2-5 hours",
         "why": "Starts as a simple text-based idle game and unfolds into an atmospheric survival RPG. A masterclass in minimalism.",
         "url": "https://adarkroom.herokuapp.com"},
        {"title": "Candy Box!", "platforms": ["Browser"], "difficulty": "Medium",
         "time": "3-8 hours",
         "why": "The spiritual predecessor to A Dark Room. Starts absurd, becomes a real RPG. Full of surprises and secrets.",
         "url": "https://candybox2.github.io"},
        {"title": "Bit Heroes", "platforms": ["Browser", "Kongregate"], "difficulty": "Easy",
         "time": "Endless",
         "why": "Retro-styled RPG dungeon crawler with collectible heroes. Grindy but satisfying progression with a charming pixel art style.",
         "url": "https://www.kongregate.com/games/Juppiomenz/bit-heroes"},
        {"title": "Dragon Raja", "platforms": ["Browser", "Mobile"], "difficulty": "Easy",
         "time": "Endless",
         "why": "An anime-styled open-world RPG playable in-browser. Impressive graphics for a free game with real-time combat.",
         "url": "https://dragonraja.en.101xp.com"},
        {"title": "Wartune", "platforms": ["Browser"], "difficulty": "Easy",
         "time": "Endless",
         "why": "Strategy RPG with city building, dungeons, and PvP. One of the most polished browser RPGs available for free.",
         "url": "https://www.kongregate.com/games/Profile4/wartune"},
        {"title": "Runescape (Old School)", "platforms": ["Browser"], "difficulty": "Medium",
         "time": "100+ hours",
         "why": "The legendary MMORPG with a free-to-play area that offers dozens of hours of genuine content. Nostalgia overload.",
         "url": "https://oldschool.runescape.com"},
    ],
    "strategy": [
        {"title": "The Battle for Wesnoth", "platforms": ["Browser", "Steam"], "difficulty": "Medium",
         "time": "20-50 hours",
         "why": "A turn-based strategy game with a fantasy setting and dozens of campaigns. Open-source, community-driven, and deeply tactical.",
         "url": "https://www.wesnoth.org"},
        {"title": "Zero-K", "platforms": ["Steam", "itch.io"], "difficulty": "Hard",
         "time": "20-100 hours",
         "why": "An open-source RTS with massive battles, terraforming, and unit customization. Think Supreme Commander but free.",
         "url": "https://store.steampowered.com/app/722260"},
        {"title": "OpenTTD", "platforms": ["Browser", "Steam"], "difficulty": "Medium",
         "time": "30-100 hours",
         "why": "Transport Tycoon Deluxe, remade and improved. Build transport empires across vast maps. Endlessly replayable.",
         "url": "https://www.openttd.org"},
        {"title": "Kingdom Rush", "platforms": ["Browser"], "difficulty": "Medium",
         "time": "5-10 hours",
         "why": "One of the best tower defense games ever made. Four tower types, clever level design, and satisfying difficulty curve.",
         "url": "https://www.kongregate.com/games/ironhidegames/kingdom-rush"},
        {"title": "Bloons TD 6 (free version)", "platforms": ["Browser", "Mobile"], "difficulty": "Easy-Medium",
         "time": "Endless",
         "why": "The definitive tower defense series. Pop balloons with monkey towers. Surprisingly strategic with amazing variety.",
         "url": "https://ninja.kiwiforge.net.nz"},
        {"title": "Polytopia", "platforms": ["Browser"], "difficulty": "Easy-Medium",
         "time": "5-20 hours",
         "why": "A streamlined 4X strategy game perfect for quick sessions. Expand, research, and conquer in bite-sized turns.",
         "url": "https://polytopia.io"},
        {"title": "Fallen London", "platforms": ["Browser"], "difficulty": "Easy",
         "time": "Endless",
         "why": "A text-based RPG set in a Lovecraftian London underground. Rich narrative with branching stories and atmospheric writing.",
         "url": "https://www.fallenlondon.com"},
        {"title": "Mindustry", "platforms": ["Steam", "itch.io"], "difficulty": "Medium-Hard",
         "time": "20-50 hours",
         "why": "Factory building meets tower defense meets RTS. Mine resources, build production chains, and defend against waves.",
         "url": "https://anuke.itch.io/mindustry"},
    ],
    "action": [
        {"title": "Krunker", "platforms": ["Browser"], "difficulty": "Medium",
         "time": "Endless",
         "why": "A fast-paced FPS that runs entirely in your browser. Smooth movement, custom maps, and active multiplayer community.",
         "url": "https://krunker.io"},
        {"title": "War Brokers", "platforms": ["Browser"], "difficulty": "Medium",
         "time": "Endless",
         "why": "Top-down multiplayer shooter with tactical combat. Quick matches, destructible environments, and a great community.",
         "url": "https://www.warbrokers.io"},
        {"title": "Garena Free Fire", "platforms": ["Mobile", "Browser"], "difficulty": "Medium",
         "time": "Endless",
         "why": "A battle royale that runs on nearly any device. 10-minute matches, 50 players, and surprisingly polished.",
         "url": "https://ff.garena.com"},
        {"title": "Retro Bowl", "platforms": ["Browser"], "difficulty": "Easy",
         "time": "Endless",
         "why": "Manage an American football team with retro graphics and simple but addictive gameplay. One of the best browser sports games.",
         "url": "https://retrobowl.com"},
        {"title": "Rooftop Snipers", "platforms": ["Browser"], "difficulty": "Easy",
         "time": "Endless",
         "why": "Absurd two-player sniper duel on rooftops. Physics-based wackiness and instant fun. Great for quick sessions with a friend.",
         "url": "https://poki.com/en/search/rooftop-snipers"},
        {"title": "ZombsRoyale", "platforms": ["Browser"], "difficulty": "Easy-Medium",
         "time": "Endless",
         "why": "A 2D battle royale with building mechanics. Fast matches, simple controls, and surprisingly tactical gameplay.",
         "url": "https://zombsroyale.io"},
        {"title": "Stickman Hook", "platforms": ["Browser"], "difficulty": "Easy",
         "time": "Endless",
         "why": "Swing through levels as a stickman using a grappling hook. Physics-based platforming perfection. One-more-try vibes.",
         "url": "https://poki.com/en/search/stickman-hook"},
        {"title": "Smash Karts", "platforms": ["Browser"], "difficulty": "Easy-Medium",
         "time": "Endless",
         "why": "Mario Kart meets arena combat in your browser. Collect power-ups, destroy opponents, and race to victory.",
         "url": "https://smashkarts.io"},
    ],
    "adventure": [
        {"title": "OneShot", "platforms": ["Steam (free)"], "difficulty": "Easy",
         "time": "4-6 hours",
         "why": "A meta-narrative adventure where the game knows it's a game. Solve puzzles to guide a child through a dying world. Hauntingly beautiful.",
         "url": "https://store.steampowered.com/app/420530"},
        {"title": "Crypt of the NecroDancer", "platforms": ["Steam (limited)"], "difficulty": "Medium",
         "time": "10-20 hours",
         "why": "Dungeon crawling to the beat. Every action must match the rhythm. Incredibly creative hybrid of rhythm and roguelike.",
         "url": "https://store.steampowered.com/app/247080"},
        {"title": "Before Your Eyes", "platforms": ["Steam (demo)"], "difficulty": "Easy",
         "time": "1-2 hours",
         "why": "A narrative game where blinking controls the story. You literally can't look away. A brief but deeply emotional experience.",
         "url": "https://store.steampowered.com/app/1173620"},
        {"title": "When Rivers Were Trails", "platforms": ["itch.io"], "difficulty": "Easy",
         "time": "1-2 hours",
         "why": "An educational adventure about Anishinaabeg displacement in the 1890s. Important perspective delivered through engaging gameplay.",
         "url": "https://aiiros.itch.io/when-rivers-were-trails"},
        {"title": "Desktop Dungeons", "platforms": ["itch.io"], "difficulty": "Medium",
         "time": "10-20 hours",
         "why": "A distilled roguelike adventure that condenses hours of exploration into 10-minute sessions. Strategy meets puzzle meets adventure.",
         "url": "https://www.qcfdesign.com"},
        {"title": "Emerald City Confidential", "platforms": ["Steam (free)"], "difficulty": "Easy",
         "time": "3-5 hours",
         "why": "A noir mystery set in Oz. A clever, dark take on the Wizard of Oz universe as a point-and-click adventure.",
         "url": "https://store.steampowered.com/app/10950"},
        {"title": "Way", "platforms": ["Browser", "Kongregate"], "difficulty": "Easy",
         "time": "1-2 hours",
         "why": "A wordless adventure where you cooperate with strangers to solve environmental puzzles. Proof that online gaming can be beautiful.",
         "url": "https://www.kongregate.com/games/chrisb/way"},
        {"title": "The Company of Myself", "platforms": ["Browser"], "difficulty": "Medium",
         "time": "30-60 min",
         "why": "A platformer where your past selves become platforms. Clever mechanics wrapped in a touching story about loneliness.",
         "url": "https://www.kongregate.com/games/2DArray/the-company-of-myself"},
    ],
    "simulation": [
        {"title": "Celeste Classic", "platforms": ["itch.io", "Browser"], "difficulty": "Hard",
         "time": "1-3 hours",
         "why": "The free precursor to the full Celeste. Tight platforming, beautiful pixel art, and an emotional story about overcoming anxiety.",
         "url": "https://mattthorson.itch.io/celeste-classic"},
        {"title": "Stardew Valley (open-source demake)", "platforms": ["itch.io"], "difficulty": "Easy",
         "time": "5-10 hours",
         "why": "A fan-made demake of Stardew Valley in Game Boy style. Capture the farming charm in retro graphics. Surprisingly complete.",
         "url": "https:// concernedape.com/stardewvalley"},
        {"title": "Townscaper", "platforms": ["itch.io (demo)"], "difficulty": "Easy",
         "time": "Endless",
         "why": "Build colorful island towns with zero rules. No objectives, no stress \u2014 just pure creative city-building therapy.",
         "url": "https://oskarstaalberg.itch.io/townscaper"},
        {"title": "Flight of the Amazon Queen", "platforms": ["Steam"], "difficulty": "Easy",
         "time": "5-10 hours",
         "why": "A classic point-and-click adventure remade for modern systems. Indiana Jones-style jungle adventure with humor and heart.",
         "url": "https://store.steampowered.com/app/730050"},
        {"title": "Voxel Farm", "platforms": ["Browser"], "difficulty": "Easy",
         "time": "Endless",
         "why": "Build with voxels in your browser. Create anything from simple houses to complex cities. Satisfying and meditative.",
         "url": "https://www.kongregate.com/games/MrShifrin/voxelfarm"},
        {"title": "Eco", "platforms": ["Steam (free)"], "difficulty": "Medium",
         "time": "20-100 hours",
         "why": "A multiplayer survival game with an ecosystem. Everything you do affects the world. Build civilization without destroying nature.",
         "url": "https://store.steampowered.com/app/739530"},
        {"title": "Party Animals Demo", "platforms": ["Steam"], "difficulty": "Easy",
         "time": "5-10 hours",
         "why": "Wobbly physics-based party game with adorable animals. Wrestle, throw, and tackle friends in absurd arenas.",
         "url": "https://store.steampowered.com/app/702060"},
        {"title": "Euro Truck Simulator 2 (demo)", "platforms": ["Steam"], "difficulty": "Easy",
         "time": "5-10 hours",
         "why": "Drive trucks across Europe in surprising detail. The demo captures the zen-like appeal of the full game perfectly.",
         "url": "https://store.steampowered.com/app/227300"},
    ],
    "cozy": [
        {"title": "Cozy Grove", "platforms": ["Steam (free weekend)"], "difficulty": "Easy",
         "time": "10-20 hours",
         "why": "A camping game where you befriend ghost bears and restore a haunted island. Stardew Valley meets Animal Crossing.",
         "url": "https://store.steampowered.com/app/1171840"},
        {"title": "Alba: a Wildlife Adventure", "platforms": ["Steam (free)"], "difficulty": "Easy",
         "time": "2-4 hours",
         "why": "Explore a Mediterranean island and photograph wildlife. Pure wholesome joy. Watch for free during Steam events.",
         "url": "https://store.steampowered.com/app/1245200"},
        {"title": "Dwarf Fortress (fortress mode)", "platforms": ["Bay12 Games"], "difficulty": "Medium-Hard",
         "time": "100+ hours",
         "why": "Build a dwarven fortress from scratch. Watch your dwarves live, love, and occasionally die in spectacular fashion. Stories generate themselves.",
         "url": "https://www.bay12games.com/dwarves"},
        {"title": "Unpacking (demo)", "platforms": ["Steam"], "difficulty": "Easy",
         "time": "1-2 hours",
         "why": "Unpack belongings and arrange a room to reveal a life story. The most therapeutic game on this list. The demo is complete.",
         "url": "https://store.steampowered.com/app/1173040"},
        {"title": "Wanderlust: Travel Stories", "platforms": ["itch.io"], "difficulty": "Easy",
         "time": "3-5 hours",
         "why": "Interactive travel stories with beautiful photography. The perfect game for when you can't travel but want to explore.",
         "url": "https://store.steampowered.com/app/1090890"},
        {"title": "Dorfromantik (demo)", "platforms": ["Steam"], "difficulty": "Easy",
         "time": "3-5 hours",
         "why": "Build a hexagonal landscape puzzle. Relaxing, beautiful, and endlessly replayable. The demo gives hours of content.",
         "url": "https://store.steampowered.com/app/1124680"},
        {"title": "Calm Waters", "platforms": ["itch.io"], "difficulty": "Easy",
         "time": "2-4 hours",
         "why": "A point-and-click mystery set in a small town. Charming visuals and a relaxing pace perfect for a rainy afternoon.",
         "url": "https://talestoridestudios.itch.io/calm-waters-demo"},
        {"title": "Garden Paws", "platforms": ["itch.io (demo)"], "difficulty": "Easy",
         "time": "5-10 hours",
         "why": "Run a shop, garden, and explore as cute animals. Stardew Valley vibes with a cozy animal village setting.",
         "url": "https://eft.itch.io/garden-paws"},
    ],
}

# ---------------------------------------------------------------------------
# Platform data
# ---------------------------------------------------------------------------
PLATFORM_DATA = {
    "pc": {
        "label": "PC (Windows/Mac/Linux)",
        "sources": ["itch.io", "Steam F2P", "Epic Games (free giveaways)"],
        "notes": "Most games run on Windows. Check itch.io pages for Mac/Linux support.",
    },
    "mac": {
        "label": "Mac",
        "sources": ["itch.io (filter: Mac)", "Steam F2P (filter: Mac)", "Epic Games"],
        "notes": "Smaller selection than PC but growing. Apple Arcade has free trials.",
    },
    "mobile": {
        "label": "Mobile (iOS/Android)",
        "sources": ["App Store free games", "Google Play", "itch.io (Android)"],
        "notes": "Many browser games also work on mobile browsers. Watch for pay-to-win mechanics.",
    },
    "browser": {
        "label": "Browser (No Download)",
        "sources": ["Poki", "CrazyGames", "Kongregate", "itch.io (HTML5)"],
        "notes": "No downloads needed. Works on any device with a modern browser. Best for casual sessions.",
    },
}

PLATFORM_LINKS = {
    "itch.io": "https://itch.io",
    "Steam F2P": "https://store.steampowered.com/genre/Free%20to%20Play",
    "Epic Games (free giveaways)": "https://store.epicgames.com/free",
    "Poki": "https://poki.com",
    "CrazyGames": "https://crazygames.com",
    "Kongregate": "https://kongregate.com",
}


def generate_guide(platform, genres):
    """Generate the free gaming guide as markdown."""
    now = datetime.now().strftime("%B %d, %Y")

    lines = []
    lines.append(f"# \U0001f3ae Free Gaming Guide")
    lines.append(f"*Curated free games for your platform \u2014 generated {now}*\n")

    # Platform info
    plat_key = platform.lower()
    plat_info = PLATFORM_DATA.get(plat_key, PLATFORM_DATA["pc"])

    lines.append("## \U0001f3c6 Your Platform\n")
    lines.append(f"**Selected:** {plat_info['label']}\n")
    lines.append(f"> {plat_info['notes']}\n")
    lines.append("**Free Game Sources:**\n")
    for src in plat_info["sources"]:
        link = PLATFORM_LINKS.get(src, "#")
        lines.append(f"- [{src}]({link})")
    lines.append("")

    # All platform links
    lines.append("## \U0001f517 All Free Gaming Platforms\n")
    lines.append("| Platform | URL | Best For |")
    lines.append("|----------|-----|----------|")
    lines.append("| [itch.io]({}) | itch.io | Indie games, demos, game jams |".format("https://itch.io"))
    lines.append("| [Steam F2P]({}) | steampowered.com | Premium-quality free games |".format("https://store.steampowered.com/genre/Free%20to%20Play"))
    lines.append("| [Epic Free Games]({}) | epicgames.com/free | Weekly premium giveaways |".format("https://store.epicgames.com/free"))
    lines.append("| [Poki]({}) | poki.com | Browser games, no downloads |".format("https://poki.com"))
    lines.append("| [CrazyGames]({}) | crazygames.com | HTML5 browser games |".format("https://crazygames.com"))
    lines.append("| [Kongregate]({}) | kongregate.com | Classic browser gaming, badges |".format("https://kongregate.com"))
    lines.append("| [GOG Free]({}) | gog.com | DRM-free classics (check sales) |".format("https://gog.com"))
    lines.append("")

    # Filter games by platform relevance
    browser_only = plat_key == "browser"
    relevant_genres = [g for g in genres if g in GAMES]
    if not relevant_genres:
        relevant_genres = list(GAMES.keys())

    total_games = 0

    # Games by genre
    lines.append("## \U0001f3af Game Recommendations by Genre\n")

    for genre in sorted(relevant_genres):
        if genre not in GAMES:
            continue

        games = GAMES[genre]

        # Filter by platform if browser
        if browser_only:
            games = [g for g in games if "Browser" in g["platforms"]]

        if not games:
            continue

        total_games += len(games)
        genre_label = genre.replace("-", " ").title()
        genre_emojis = {
            "puzzle": "\U0001f9e9", "rpg": "\u2694\ufe0f", "strategy": "\U0001f571",
            "action": "\U0001f525", "adventure": "\U0001f30d", "simulation": "\U0001f3ed",
            "cozy": "\U0001f33f",
        }
        emoji = genre_emojis.get(genre, "\U0001f3ae")

        lines.append(f"### {emoji} {genre_label}\n")
        lines.append("| # | Game | Platforms | Difficulty | Time |")
        lines.append("|---|------|-----------|-----------|------|")

        for i, game in enumerate(games, 1):
            plat_str = ", ".join(game["platforms"])
            lines.append(f"| {i} | [{game['title']}]({game['url']}) | {plat_str} | {game['difficulty']} | {game['time']} |")
        lines.append("")

        # Why play section
        lines.append(f"**Why these games are worth your time:**\n")
        for game in games:
            lines.append(f"- **{game['title']}:** {game['why']}")
        lines.append("")

    # Weekly gaming schedule
    lines.append("---\n")
    lines.append("## \U0001f4c5 Weekly Gaming Schedule\n")
    lines.append("| Day | Session | Suggested Activity | Time |")
    lines.append("|-----|---------|-------------------|------|")
    lines.append("| \u2600\ufe0f Monday | Quick session | Browser puzzle game during lunch | 20 min |")
    lines.append("| \U0001f3ae Monday | Evening play | RPG or adventure game deep dive | 60 min |")
    lines.append("| \u2615 Tuesday | Coffee break | Cozy browser game | 15 min |")
    lines.append("| \U0001f3ae Tuesday | Main session | Strategy or action game | 45 min |")
    lines.append("| \U0001f3ae Wednesday | Mid-week unwind | Puzzle game session | 30 min |")
    lines.append("| \U0001f3ae Wednesday | Evening | Continue RPG/adventure story | 60 min |")
    lines.append("| \U0001f3ae Thursday | Quick session | Browser action game | 20 min |")
    lines.append("| \U0001f3ae Thursday | Cozy evening | Relaxing simulation game | 45 min |")
    lines.append("| \U0001f3ae Friday | Friday fun | Try something completely new | 60 min |")
    lines.append("| \U0001f3ae Saturday | Marathon session | Deep RPG or strategy | 2-3 hours |")
    lines.append("| \U0001f3ae Saturday | Break | Cozy or browser game | 30 min |")
    lines.append("| \U0001f3ae Sunday | Wrap up | Finish the week's game or story | 60 min |")
    lines.append("| \U0001f3ae Sunday | Discovery | Browse itch.io for hidden gems | 20 min |")
    lines.append("")

    # Tips
    lines.append("---\n")
    lines.append("## \U0001f4a1 Free Gaming Tips\n")
    lines.append("- **Claim Epic Games freebies weekly** \u2014 premium games like GTA V and Subnautica have been free.")
    lines.append("- **Check itch.io game jams** \u2014 these produce incredible free games on specific themes.")
    lines.append("- **Use Steam's category filters** \u2014 sort by 'Overwhelmingly Positive' reviews for quality.")
    lines.append("- **Bookmark Poki for quick sessions** \u2014 no downloads, no accounts, instant play.")
    lines.append("- **Watch for Steam free weekends** \u2014 try premium games before deciding to buy.")
    lines.append("- **Join indie game communities** \u2014 Discord servers and Reddit for recommendations.")
    lines.append("- **Set time limits** \u2014 especially for 'endless' games. Use a timer to avoid rabbit holes.")
    lines.append("")

    lines.append(f"*\U0001f3ae {total_games} games curated across {len(relevant_genres)} genres \u2014 Generated {now}*\n")

    return "\n".join(lines)


def main():
    """Parse arguments and generate the gaming guide."""
    parser = argparse.ArgumentParser(
        description="Discover free games across platforms with personalized recommendations.",
        epilog="Example: python gaming_guide.py --platform browser --genres 'puzzle,action,cozy'",
    )
    parser.add_argument(
        "--platform",
        choices=["pc", "mac", "mobile", "browser"],
        default="pc",
        help="Gaming platform (default: pc)",
    )
    parser.add_argument(
        "--genres",
        default="puzzle,rpg,strategy,action,adventure,simulation,cozy",
        help="Comma-separated game genres (default: all)",
    )
    parser.add_argument(
        "--output",
        default="gaming_guide.md",
        help="Output markdown file path (default: gaming_guide.md)",
    )

    args = parser.parse_args()

    genres = [g.strip().lower() for g in args.genres.split(",") if g.strip()]

    valid = list(GAMES.keys())
    invalid = [g for g in genres if g not in valid]
    if invalid:
        print(f"Warning: Unknown genres ignored: {', '.join(invalid)}", file=sys.stderr)
        genres = [g for g in genres if g in valid]

    if not genres:
        genres = valid

    try:
        content = generate_guide(platform=args.platform, genres=genres)

        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)

        abs_path = os.path.abspath(args.output)
        total_games = sum(
            len([g for g in GAMES[genre] if (args.platform.lower() != "browser" or "Browser" in g["platforms"])])
            for genre in genres if genre in GAMES
        )

        print(f"\n{'='*60}")
        print(f"  \U0001f3ae Free Gaming Guide Generated Successfully!")
        print(f"{'='*60}")
        print(f"  \U0001f4c4 File:      {abs_path}")
        print(f"  \U0001f3c6 Platform:  {args.platform}")
        print(f"  \U0001f3af Genres:    {len(genres)}")
        print(f"  \U0001f3ae Games:     {total_games}")
        print(f"  \U0001f4c5 Schedule:  Weekly gaming plan included")
        print(f"{'='*60}\n")

    except PermissionError:
        print(f"Error: Permission denied writing to '{args.output}'.", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: Could not write file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
