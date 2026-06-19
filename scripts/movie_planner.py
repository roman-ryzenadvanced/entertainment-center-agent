#!/usr/bin/env python3
"""
Movie Night Planner
===================
Generates personalized movie night recommendations from free streaming
platforms. Supports multiple moods, provides backup options for each pick,
and outputs a beautifully formatted markdown plan.

Supported moods: funny, scary, romantic, action, slow, deep

Usage:
    python movie_planner.py --mood funny --count 5
    python movie_planner.py --mood deep --count 15 --output deep_movies.md
"""

import argparse
import sys
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Movie database organized by mood
# Each entry: title, platform, year, why, best_for, backup_title, backup_platform
# ---------------------------------------------------------------------------
MOVIES = {
    "funny": [
        {"title": "Spaceballs", "platform": "Tubi", "year": 1987,
         "why": "Mel Brooks' brilliant Star Wars parody is laugh-out-loud from start to finish with endless quotable lines.",
         "best_for": "Fans of absurd humor and sci-fi spoofs",
         "backup": "Young Frankenstein", "backup_platform": "Tubi"},
        {"title": "The Great Dictator", "platform": "Tubi", "year": 1940,
         "why": "Charlie Chaplin's timeless satire of fascism. The final speech remains one of cinema's most powerful moments.",
         "best_for": "Classic comedy lovers and history buffs",
         "backup": "Modern Times", "backup_platform": "Tubi"},
        {"title": "Superbad", "platform": "Crackle", "year": 2007,
         "why": "The definitive teen comedy of its era. Jonah Hill and Michael Cera deliver perfectly awkward performances.",
         "best_for": "Friend groups and anyone who survived high school",
         "backup": "Knocked Up", "backup_platform": "Freevee"},
        {"title": "Monty Python and the Holy Grail", "platform": "Tubi", "year": 1975,
         "why": "The gold standard of British absurdism. Every scene is iconic \u2014 from the Knights of Ni to the Bridge of Death.",
         "best_for": "Fans of clever, ridiculous humor",
         "backup": "Life of Brian", "backup_platform": "Tubi"},
        {"title": "What We Do in the Shadows", "platform": "Freevee", "year": 2014,
         "why": "A mockumentary about vampire roommates in modern New Zealand. Deadpan humor at its finest.",
         "best_for": "Fans of The Office and dry comedy",
         "backup": "Hunt for the Wilderpeople", "backup_platform": "Tubi"},
        {"title": "Hot Fuzz", "platform": "Tubi", "year": 2007,
         "why": "Edgar Wright's action-comedy masterpiece set in a quaint English village with a dark secret.",
         "best_for": "Action and comedy fans alike",
         "backup": "Shaun of the Dead", "backup_platform": "Tubi"},
        {"title": "Rango", "platform": "Pluto TV", "year": 2011,
         "why": "Johnny Depp voices a chameleon sheriff in this visually stunning animated Western comedy with surprising depth.",
         "best_for": "Adults and kids who appreciate clever animated films",
         "backup": "The Emperor's New Groove", "backup_platform": "YouTube"},
        {"title": "Dr. Strangelove", "platform": "Tubi", "year": 1964,
         "why": "Stanley Kubrick's cold war satire about nuclear annihilation. Peter Sellers plays three roles brilliantly.",
         "best_for": "Dark comedy fans and political satire lovers",
         "backup": "The Great Dictator", "backup_platform": "Tubi"},
        {"title": "Team America: World Police", "platform": "Tubi", "year": 2004,
         "why": "Trey Parker and Matt Stone's puppet action-comedy skewering American foreign policy. Brutally funny.",
         "best_for": "South Park fans and anyone who appreciates outrageous satire",
         "backup": "Baseketball", "backup_platform": "Tubi"},
        {"title": "Clue", "platform": "Crackle", "year": 1985,
         "why": "Based on the board game, this cult classic murder mystery comedy has three alternate endings and perfect comedic timing.",
         "best_for": "Mystery lovers who enjoy a good laugh",
         "backup": "Murder by Death", "backup_platform": "Tubi"},
        {"title": "Galaxy Quest", "platform": "Tubi", "year": 1999,
         "why": "A loving parody of Star Trek fandom starring Tim Allen and Sigourney Weaver. Surprisingly heartfelt.",
         "best_for": "Sci-fi fans who can laugh at themselves",
         "backup": "Spaceballs", "backup_platform": "Tubi"},
        {"title": "Tucker & Dale vs. Evil", "platform": "Tubi", "year": 2010,
         "why": "A hilarious flip on the horror genre \u2014 the 'hillbillies' are the good guys and the college kids are the menace.",
         "best_for": "Horror-comedy fans tired of predictable slasher films",
         "backup": "Cabin in the Woods", "backup_platform": "Freevee"},
        {"title": "Office Space", "platform": "Freevee", "year": 1999,
         "why": "Mike Judge's satire of corporate drone life. Milton's stapler, the printer scene \u2014 all iconic.",
         "best_for": "Anyone who has ever worked in an office",
         "backup": "Idiocracy", "backup_platform": "Tubi"},
        {"title": "The Big Lebowski", "platform": "Tubi", "year": 1998,
         "why": "The Coen Brothers' stoner noir comedy. Jeff Bridges as The Dude is one of cinema's most lovable characters.",
         "best_for": "Fans of quirky characters and bowling",
         "backup": "O Brother, Where Art Thou?", "backup_platform": "Tubi"},
        {"title": " Coming to America", "platform": "Crackle", "year": 1988,
         "why": "Eddie Murphy at his absolute best as an African prince searching for love in Queens, New York.",
         "best_for": "80s comedy fans and Eddie Murphy lovers",
         "backup": "Trading Places", "backup_platform": "Tubi"},
    ],
    "scary": [
        {"title": "Night of the Living Dead", "platform": "Tubi", "year": 1968,
         "why": "George A. Romero invented the modern zombie genre. Gritty, terrifying, and groundbreaking.",
         "best_for": "Horror purists and fans of cinema history",
         "backup": "Dawn of the Dead (1978)", "backup_platform": "Tubi"},
        {"title": "Carnival of Souls", "platform": "YouTube", "year": 1962,
         "why": "An eerie, atmospheric cult classic about a woman haunted after a car accident. Massive influence on David Lynch.",
         "best_for": "Fans of psychological horror and arthouse chills",
         "backup": "Eraserhead", "backup_platform": "Tubi"},
        {"title": "The Cabinet of Dr. Caligari", "platform": "YouTube", "year": 1920,
         "why": "German Expressionist masterpiece. The twisted set design and unsettling atmosphere still creep out viewers 100+ years later.",
         "best_for": "Silent film fans and lovers of visual horror",
         "backup": "Nosferatu", "backup_platform": "Tubi"},
        {"title": "Nosferatu", "platform": "Tubi", "year": 1922,
         "why": "The original vampire film. Max Schreck's Count Orlok is genuinely one of the scariest characters in cinema history.",
         "best_for": "Horror historians and Halloween movie nights",
         "backup": "Shadow of the Vampire", "backup_platform": "YouTube"},
        {"title": "Hellraiser", "platform": "Tubi", "year": 1987,
         "why": "Clive Barker's twisted vision of pleasure and pain. Pinhead is one of horror's most iconic villains.",
         "best_for": "Fans of visceral, body-horror cinema",
         "backup": "Hellbound: Hellraiser II", "backup_platform": "Tubi"},
        {"title": "The Birds", "platform": "Tubi", "year": 1963,
         "why": "Hitchcock's nature-gone-wrong thriller. Ordinary birds become an inexplicable terror. Masterful suspense.",
         "best_for": "Hitchcock fans and creature-feature lovers",
         "backup": "Rear Window", "backup_platform": "Tubi"},
        {"title": "House on Haunted Hill", "platform": "YouTube", "year": 1959,
         "why": "Vincent Price stars in this classic haunted house chiller. Five strangers are offered $10,000 to survive the night.",
         "best_for": "Old-school haunted house fans",
         "backup": "The Pit and the Pendulum", "backup_platform": "Tubi"},
        {"title": "Invasion of the Body Snatchers", "platform": "Tubi", "year": 1956,
         "why": "Paranoia at its finest \u2014 pod people replace humans while they sleep. A chilling allegory for conformity.",
         "best_for": "Sci-fi horror fans and paranoia thriller lovers",
         "backup": "The Thing from Another World", "backup_platform": "YouTube"},
        {"title": "White Zombie", "platform": "YouTube", "year": 1932,
         "why": "Bela Lugosi stars in the first feature-length zombie film. Atmospheric and genuinely creepy voodoo horror.",
         "best_for": "Classic horror completists and Lugosi fans",
         "backup": "Island of Lost Souls", "backup_platform": "YouTube"},
        {"title": "Night of the Hunter", "platform": "Tubi", "year": 1955,
         "why": "Robert Mitchum delivers one of cinema's most unsettling performances as a murderous preacher. Visually stunning.",
         "best_for": "Fans of Southern Gothic and psychological suspense",
         "backup": "Cape Fear (1962)", "backup_platform": "Tubi"},
        {"title": "Cat People", "platform": "Tubi", "year": 1942,
         "why": "A woman fears she'll transform into a panther when aroused. Atmospheric and ahead of its time in exploring fear and sexuality.",
         "best_for": "Fans of atmospheric, suggestive horror",
         "backup": "I Walked with a Zombie", "backup_platform": "Tubi"},
        {"title": "The Phantom of the Opera", "platform": "YouTube", "year": 1925,
         "why": "Lon Chaney's iconic makeup and the stunning Technicolor masquerade sequence. A foundational horror landmark.",
         "best_for": "Silent film enthusiasts and musical horror fans",
         "backup": "The Hunchback of Notre Dame (1923)", "backup_platform": "YouTube"},
        {"title": "Nightmare Alley", "platform": "Tubi", "year": 1947,
         "why": "A dark noir about a carnival mentalist who rises and falls. Tyrone Power in an against-type role.",
         "best_for": "Film noir fans who like their noir creepy",
         "backup": "Freaks", "backup_platform": "Tubi"},
        {"title": "Freaks", "platform": "YouTube", "year": 1932,
         "why": "Tod Browning's controversial classic starring real carnival performers. Shocking, moving, and unforgettable.",
         "best_for": "Those who want horror that challenges and provokes",
         "backup": "Sideshow", "backup_platform": "Tubi"},
        {"title": "Dementia 13", "platform": "Tubi", "year": 1963,
         "why": "Francis Ford Coppola's directorial debut \u2014 a low-budget slasher with genuine chills and a great axe murder scene.",
         "best_for": "Coppola completists and slasher fans",
         "backup": "The Masque of the Red Death", "backup_platform": "Tubi"},
    ],
    "romantic": [
        {"title": "His Girl Friday", "platform": "Tubi", "year": 1940,
         "why": "Cary Grant and Rosalind Russell deliver the fastest dialogue in film history in this screwball comedy masterpiece.",
         "best_for": "Fans of sharp wit and chemistry-driven romance",
         "backup": "Bringing Up Baby", "backup_platform": "Tubi"},
        {"title": "Roman Holiday", "platform": "Tubi", "year": 1953,
         "why": "Audrey Hepburn and Gregory Peck in Rome. A princess escapes her duties for one magical day. Timeless and charming.",
         "best_for": "Dreamers and anyone who loves European settings",
         "backup": "Sabrina", "backup_platform": "Tubi"},
        {"title": "The Apartment", "platform": "Tubi", "year": 1960,
         "why": "Jack Lemmon and Shirley MacLaine in Billy Wilder's bittersweet masterpiece about loneliness and connection in corporate America.",
         "best_for": "Fans of smart, adult romance with real emotional depth",
         "backup": "The Odd Couple", "backup_platform": "Tubi"},
        {"title": "It Happened One Night", "platform": "Tubi", "year": 1934,
         "why": "Clark Gable and Claudette Colbert hitchhike across America. Won all five major Oscars. The blueprint for romantic comedies.",
         "best_for": "Classic Hollywood buffs and rom-com fans",
         "backup": "You Can't Take It With You", "backup_platform": "Tubi"},
        {"title": "Pride and Prejudice (1940)", "platform": "YouTube", "year": 1940,
         "why": "Greer Garson and Laurence Olivier bring Austen's beloved novel to life. Elegant and charming.",
         "best_for": "Jane Austen fans and period drama lovers",
         "backup": "Sense and Sensibility", "backup_platform": "Tubi"},
        {"title": "Brief Encounter", "platform": "Tubi", "year": 1945,
         "why": "David Lean's achingly beautiful tale of a married woman's brief, doomed affair. Rachel Roberts' performance is devastating.",
         "best_for": "Those who appreciate romance steeped in real emotion and restraint",
         "backup": "The Way We Were", "backup_platform": "Tubi"},
        {"title": "City Lights", "platform": "YouTube", "year": 1931,
         "why": "Charlie Chaplin's final silent film. The Tramp falls for a blind flower girl. The final scene will break your heart.",
         "best_for": "Silent film fans and anyone who loves pure, wordless emotion",
         "backup": "Modern Times", "backup_platform": "Tubi"},
        {"title": "Marty", "platform": "Tubi", "year": 1955,
         "why": "A humble butcher finds unexpected love. A beautiful, simple story about ordinary people. Won Best Picture.",
         "best_for": "Anyone who believes love finds you when you least expect it",
         "backup": "The Quiet Man", "backup_platform": "Tubi"},
        {"title": "Harvey", "platform": "Tubi", "year": 1950,
         "why": "James Stewart believes his best friend is a six-foot invisible rabbit. Gentle, warm, and profoundly kind.",
         "best_for": "Fans of gentle humor and eccentric characters",
         "backup": "It's a Wonderful Life", "backup_platform": "Tubi"},
        {"title": "The Lady Eve", "platform": "Tubi", "year": 1941,
         "why": "Barbara Stanwyck as a con artist who falls for her mark. Preston Sturges directs this sparkling screwball comedy.",
         "best_for": "Fans of sophisticated romantic comedy",
         "backup": "Sullivan's Travels", "backup_platform": "Tubi"},
        {"title": "Amélie", "platform": "Tubi", "year": 2001,
         "why": "A shy Parisian waitress orchestrates the happiness of those around her while struggling to find her own love story.",
         "best_for": "Dreamers, introverts, and anyone who loves Paris",
         "backup": "Paris, je t'aime", "backup_platform": "YouTube"},
        {"title": "Before Sunrise", "platform": "Freevee", "year": 1995,
         "why": "Two strangers meet on a train and spend one night walking through Vienna. Dialogue-driven romance at its finest.",
         "best_for": "Deep talkers and hopeless romantics",
         "backup": "Before Sunset", "backup_platform": "Freevee"},
        {"title": "Pillow Talk", "platform": "Tubi", "year": 1959,
         "why": "Rock Hudson and Doris Day share a party line and fall in love. The quintessential 50s romantic comedy.",
         "best_for": "Fans of classic Hollywood glamour and clean comedy",
         "backup": "Lover Come Back", "backup_platform": "Tubi"},
        {"title": "An Affair to Remember", "platform": "Tubi", "year": 1957,
         "why": "Cary Grant and Deborah Kerr agree to meet at the Empire State Building in six months. A romance classic.",
         "best_for": "Those who love grand romantic gestures and beautiful locations",
         "backup": "Love Affair (1939)", "backup_platform": "YouTube"},
        {"title": "Splendor in the Grass", "platform": "Tubi", "year": 1961,
         "why": "Warren Beatty and Natalie Wood in Elia Kazan's searing drama about first love and class in 1920s Kansas.",
         "best_for": "Fans of intense, emotionally raw romance",
         "backup": "East of Eden", "backup_platform": "Tubi"},
    ],
    "action": [
        {"title": "The General", "platform": "YouTube", "year": 1926,
         "why": "Buster Keaton's silent masterpiece featuring real stunt work that still shocks. A locomotive chase scene that rivals any modern action film.",
         "best_for": "Action fans who appreciate the roots of physical cinema",
         "backup": "Steamboat Bill, Jr.", "backup_platform": "YouTube"},
        {"title": "Enter the Dragon", "platform": "Tubi", "year": 1973,
         "why": "Bruce Lee's final completed film. Martial arts cinema at its absolute peak. Iconic tournament fights and style.",
         "best_for": "Martial arts fans and Bruce Lee completists",
         "backup": "Fist of Fury", "backup_platform": "Tubi"},
        {"title": "Seven Samurai", "platform": "Tubi", "year": 1954,
         "why": "Akira Kurosawa's epic about samurai defending a village. The template for action storytelling. 3.5 hours of perfection.",
         "best_for": "Patient viewers who want to see where modern action began",
         "backup": "Yojimbo", "backup_platform": "Tubi"},
        {"title": "The Magnificent Seven", "platform": "Tubi", "year": 1960,
         "why": "The Western remake of Seven Samurai with Steve McQueen, Yul Brynner, and Charles Bronson. Pure adventure.",
         "best_for": "Western fans who love ensemble casts",
         "backup": "The Great Escape", "backup_platform": "Tubi"},
        {"title": "District B13", "platform": "Tubi", "year": 2004,
         "why": "French parkour action film. David Belle and Cyril Raffaelli perform jaw-dropping stunts. Non-stop adrenaline.",
         "best_for": "Parkour fans and action junkies",
         "backup": "District B13: Ultimatum", "backup_platform": "Tubi"},
        {"title": "The Street Fighter", "platform": "Tubi", "year": 1974,
         "why": "Sonny Chiba's brutal martial arts classic. Raw, uncompromising fight choreography that influenced Quentin Tarantino.",
         "best_for": "Hardcore martial arts enthusiasts",
         "backup": "Return of the Street Fighter", "backup_platform": "Tubi"},
        {"title": "Bullitt", "platform": "Tubi", "year": 1968,
         "why": "Steve McQueen's car chase through San Francisco is the gold standard for vehicular action. Cool personified.",
         "best_for": "Car chase fans and 70s action cinema lovers",
         "backup": "The French Connection", "backup_platform": "Tubi"},
        {"title": "Hard Boiled", "platform": "Tubi", "year": 1992,
         "why": "John Woo's Hong Kong action masterpiece. Chow Yun-Fat with two guns in a hospital shootout scene is legendary.",
         "best_for": "Gun-fu fans and Hong Kong cinema enthusiasts",
         "backup": "The Killer", "backup_platform": "Tubi"},
        {"title": "Ong-Bak", "platform": "Tubi", "year": 2003,
         "why": "Tony Jaa performs incredible Muay Thai stunts without wires or CGI. A landmark in action choreography.",
         "best_for": "Martial arts fans craving raw, real stunt work",
         "backup": "Tom Yum Goong", "backup_platform": "Tubi"},
        {"title": "Gladiator (1992)", "platform": "Tubi", "year": 1992,
         "why": "Cuba Gooding Jr. and James Marshall in an underground boxing drama. Gritty and intense with a pumping soundtrack.",
         "best_for": "Boxing and underground fighting fans",
         "backup": "Bloodsport", "backup_platform": "Tubi"},
        {"title": "Akira", "platform": "Tubi", "year": 1988,
         "why": "The anime that introduced the West to Japanese animation. Cyberpunk motorcycle battles and psychic powers in Neo-Tokyo.",
         "best_for": "Anime fans and cyberpunk enthusiasts",
         "backup": "Ghost in the Shell (1995)", "backup_platform": "Tubi"},
        {"title": "Fist of Fury", "platform": "Tubi", "year": 1972,
         "why": "Bruce Lee takes on an oppressive martial arts school in Shanghai. The nunchaku fight scene is iconic.",
         "best_for": "Bruce Lee fans who want pure martial arts action",
         "backup": "Way of the Dragon", "backup_platform": "Tubi"},
        {"title": "The Good, the Bad and the Ugly", "platform": "Tubi", "year": 1966,
         "why": "Clint Eastwood in Leone's Spaghetti Western masterpiece. The three-way Mexican standoff is cinema perfection.",
         "best_for": "Western fans and Ennio Morricone score lovers",
         "backup": "For a Few Dollars More", "backup_platform": "Tubi"},
        {"title": "Ip Man", "platform": "Freevee", "year": 2008,
         "why": "Donnie Yen portrays Bruce Lee's Wing Chun master. Gorgeous fight choreography and a compelling historical story.",
         "best_for": "Martial arts fans who also appreciate a good story",
         "backup": "Ip Man 2", "backup_platform": "Freevee"},
        {"title": "Police Story", "platform": "Tubi", "year": 1985,
         "why": "Jackie Chan at his stunt-obsessed peak. The shopping mall fight scene is one of the greatest action sequences ever filmed.",
         "best_for": "Jackie Chan fans and practical stunt enthusiasts",
         "backup": "Police Story 2", "backup_platform": "Tubi"},
    ],
    "slow": [
        {"title": "Stalker", "platform": "YouTube", "year": 1979,
         "why": "Tarkovsky's meditative sci-fi masterpiece. Three men journey to a mysterious room where wishes come true. Hypnotic.",
         "best_for": "Patient viewers who want cinema as meditation",
         "backup": "Solaris (1972)", "backup_platform": "YouTube"},
        {"title": "Tokyo Story", "platform": "Tubi", "year": 1953,
         "why": "Ozu's heartbreaking tale of aging parents visiting their indifferent children in Tokyo. Profoundly human and beautiful.",
         "best_for": "Fans of quiet, contemplative family drama",
         "backup": "Late Spring", "backup_platform": "Tubi"},
        {"title": "The Seventh Seal", "platform": "Tubi", "year": 1957,
         "why": "Bergman's iconic tale of a knight playing chess with Death. Existential, beautiful, and deeply philosophical.",
         "best_for": "Philosophy lovers and arthouse cinema fans",
         "backup": "Wild Strawberries", "backup_platform": "Tubi"},
        {"title": "Wings of Desire", "platform": "Tubi", "year": 1987,
         "why": "Wenders' angels watch over Cold War Berlin. Poetic, visually breathtaking, and achingly romantic in the quietest way.",
         "best_for": "Poetry lovers and those who find beauty in observation",
         "backup": "Paris, Texas", "backup_platform": "Tubi"},
        {"title": "Breathless", "platform": "Tubi", "year": 1960,
         "why": "Godard's French New Wave landmark. A petty criminal and an American girl drift through Paris. Revolution in every frame.",
         "best_for": "Cinema history buffs and style enthusiasts",
         "backup": "The 400 Blows", "backup_platform": "Tubi"},
        {"title": "Persona", "platform": "Tubi", "year": 1966,
         "why": "Bergman's psychological study of two women merging identities. Liv Ullmann and Bibi Andersson are extraordinary.",
         "best_for": "Fans of psychological depth and experimental film",
         "backup": "Cries and Whispers", "backup_platform": "Tubi"},
        {"title": "Au Hasard Balthazar", "platform": "YouTube", "year": 1966,
         "why": "Bresson's deceptively simple story of a donkey's life becomes one of cinema's most profound meditations on suffering.",
         "best_for": "Minimalist cinema fans and animal lovers with strong stomachs",
         "backup": "Mouchette", "backup_platform": "YouTube"},
        {"title": "The Mirror", "platform": "YouTube", "year": 1975,
         "why": "Tarkovsky's autobiographical poem in film. Non-linear, dreamlike, and visually ravishing. Cinema at its most artistic.",
         "best_for": "Those who treat film as fine art",
         "backup": "Ivan's Childhood", "backup_platform": "YouTube"},
        {"title": "Yi Yi", "platform": "Tubi", "year": 2000,
         "why": "Edward Yang's portrait of a Taipei family over three years. Observes life's small moments with extraordinary tenderness.",
         "best_for": "Fans of intimate, observational cinema",
         "backup": "A Brighter Summer Day", "backup_platform": "Tubi"},
        {"title": "Taste of Cherry", "platform": "Tubi", "year": 1997,
         "why": "Kiarostami's meditative film about a man looking for someone to bury him after his planned suicide. Winner of the Palme d'Or.",
         "best_for": "Viewers comfortable with ambiguity and moral complexity",
         "backup": "Close-Up", "backup_platform": "Tubi"},
        {"title": "Dersu Uzala", "platform": "YouTube", "year": 1975,
         "why": "Kurosawa's Siberian wilderness epic about a hunter and his relationship with nature. Quiet, vast, and deeply moving.",
         "best_for": "Nature lovers and fans of Kurosawa's less known works",
         "backup": "Dreams", "backup_platform": "YouTube"},
        {"title": "The Turin Horse", "platform": "Tubi", "year": 2011,
         "why": "Béla Tarr's bleak, beautiful, black-and-white epic. Six days in the life of a farmer and his daughter as their world slowly collapses.",
         "best_for": "Brave viewers who want cinema at its most uncompromising",
         "backup": "Werckmeister Harmonies", "backup_platform": "Tubi"},
        {"title": "Ordet", "platform": "YouTube", "year": 1955,
         "why": "Dreyer's austere tale of faith and miracles in a Danish village. The final sequence is one of cinema's most transcendent moments.",
         "best_for": "Those interested in faith, doubt, and the power of cinema",
         "backup": "The Passion of Joan of Arc", "backup_platform": "YouTube"},
        {"title": "Jeanne Dielman", "platform": "YouTube", "year": 1975,
         "why": "Chantal Akerman's 3.5-hour study of a woman's daily routine is a landmark of feminist cinema. Riveting in its stillness.",
         "best_for": "Experimental cinema fans willing to slow down completely",
         "backup": "News from Home", "backup_platform": "YouTube"},
        {"title": "Pather Panchali", "platform": "Tubi", "year": 1955,
         "why": "Ray's debut \u2014 a boy's childhood in a Bengali village. Lyrical, humane, and visually stunning. One of the greatest first films ever.",
         "best_for": "World cinema fans and lovers of lyrical storytelling",
         "backup": "Aparajito", "backup_platform": "Tubi"},
    ],
    "deep": [
        {"title": "12 Angry Men", "platform": "Tubi", "year": 1957,
         "why": "One room, twelve men, one verdict. Sidney Lumet's claustrophobic masterpiece about prejudice, justice, and human nature.",
         "best_for": "Everyone \u2014 this is essential viewing",
         "backup": "12 Angry Men (1997)", "backup_platform": "Freevee"},
        {"title": "Paths of Glory", "platform": "Tubi", "year": 1957,
         "why": "Kubrick's devastating anti-war film about soldiers court-martialed for cowardice. Kirk Douglas delivers a searing performance.",
         "best_for": "Anti-war film fans and Kubrick completists",
         "backup": "Dr. Strangelove", "backup_platform": "Tubi"},
        {"title": "Do the Right Thing", "platform": "Tubi", "year": 1989,
         "why": "Spike Lee's incendiary portrait of racial tension on a hot Brooklyn day. More relevant now than ever. Sal's pizzeria monologue is unforgettable.",
         "best_for": "Anyone who wants cinema to challenge their perspective",
         "backup": "Malcolm X", "backup_platform": "Tubi"},
        {"title": "On the Waterfront", "platform": "Tubi", "year": 1954,
         "why": "Brando's legendary performance as a boxer turned longshoreman fighting corruption. 'I coulda been a contender.'",
         "best_for": "Fans of raw, Method acting performances",
         "backup": "A Streetcar Named Desire", "backup_platform": "Tubi"},
        {"title": "The Grapes of Wrath", "platform": "Tubi", "year": 1940,
         "why": "Ford's adaptation of Steinbeck's novel. The Joad family's journey from Dust Bowl to California. America's story.",
         "best_for": "Fans of American literature and social realism",
         "backup": "How Green Was My Valley", "backup_platform": "Tubi"},
        {"title": "Schindler's List", "platform": "Tubi", "year": 1993,
         "why": "Spielberg's unflinching Holocaust drama. Liam Neeson's transformation from war profiteer to savior is devastating.",
         "best_for": "Everyone \u2014 a duty to watch at least once",
         "backup": "The Pianist", "backup_platform": "Tubi"},
        {"title": "A Clockwork Orange", "platform": "Tubi", "year": 1971,
         "why": "Kubrick's disturbing satire on free will, violence, and state control. Malcolm McDowell's Alex is one of cinema's great monsters.",
         "best_for": "Viewers who can handle disturbing content for intellectual reward",
         "backup": "Full Metal Jacket", "backup_platform": "Tubi"},
        {"title": "The Great Dictator", "platform": "Tubi", "year": 1940,
         "why": "Chaplin's courageous satire of Hitler. The final speech \u2014 'We all want to help one another' \u2014 still brings tears.",
         "best_for": "Those who believe comedy can change the world",
         "backup": "Modern Times", "backup_platform": "Tubi"},
        {"title": "Guess Who's Coming to Dinner", "platform": "Tubi", "year": 1967,
         "why": "Sidney Poitier and Katharine Hepburn in a groundbreaking film about interracial marriage. Hepburn's tears were real.",
         "best_for": "Fans of progressive cinema and social drama",
         "backup": "In the Heat of the Night", "backup_platform": "Tubi"},
        {"title": "Dog Day Afternoon", "platform": "Tubi", "year": 1975,
         "why": "Al Pacino robs a bank to fund his lover's sex change operation. Based on a true story. Gripping from start to finish.",
         "best_for": "True crime fans and fans of intense character drama",
         "backup": "Serpico", "backup_platform": "Tubi"},
        {"title": "Network", "platform": "Tubi", "year": 1976,
         "why": "Paddy Chayefsky's prophetic satire of television news. 'I'm mad as hell, and I'm not going to take it anymore!' Still prescient.",
         "best_for": "Media critics and anyone frustrated with modern news",
         "backup": "Broadcast News", "backup_platform": "Tubi"},
        {"title": "Night and Fog", "platform": "YouTube", "year": 1955,
         "why": "Resnais' 32-minute documentary about Nazi concentration camps. Short, devastating, and essential. One of the most important films ever made.",
         "best_for": "Holocaust education and documentary film fans",
         "backup": "Shoah", "backup_platform": "YouTube"},
        {"title": "The Battle of Algiers", "platform": "YouTube", "year": 1966,
         "why": "Pontecorvo's documentary-style film about Algeria's fight for independence from France. Shown at the Pentagon as a training film.",
         "best_for": "History buffs and fans of politically engaged cinema",
         "backup": "Z", "backup_platform": "Tubi"},
        {"title": "Harlan County, USA", "platform": "YouTube", "year": 1976,
         "why": "Barbara Kopple's Oscar-winning documentary about Kentucky coal miners striking against unsafe conditions. Raw, real, and gripping.",
         "best_for": "Documentary fans and labor rights advocates",
         "backup": "American Factory", "backup_platform": "Freevee"},
        {"title": "I Am Not Your Negro", "platform": "Tubi", "year": 2016,
         "why": "James Baldwin's unfinished manuscript brought to life with Samuel L. Jackson's narration. A searing meditation on race in America.",
         "best_for": "Everyone \u2014 essential viewing on American history and race",
         "backup": "13th", "backup_platform": "YouTube"},
    ],
}

MOOD_EMOJIS = {
    "funny": "\U0001f602",
    "scary": "\U0001f47b",
    "romantic": "\U0001f495",
    "action": "\U0001f525",
    "slow": "\U0001f30c",
    "deep": "\U0001f52e",
}

PLATFORM_LINKS = {
    "Tubi": "https://tubitv.com",
    "Pluto TV": "https://pluto.tv",
    "YouTube": "https://youtube.com",
    "Crackle": "https://crackle.com",
    "Freevee": "https://amazon.com/freevee",
}


def generate_plan(mood, count):
    """Generate the movie night plan as markdown."""
    now = datetime.now().strftime("%B %d, %Y")
    emoji = MOOD_EMOJIS.get(mood, "\U0001f3ac")
    mood_title = mood.capitalize()

    if mood not in MOVIES:
        print(f"Error: Unknown mood '{mood}'. Choose from: {', '.join(MOVIES.keys())}", file=sys.stderr)
        sys.exit(1)

    available = MOVIES[mood]
    selected = available[:min(count, len(available))]
    actual_count = len(selected)

    lines = []
    lines.append(f"# {emoji} Movie Night \u2014 {mood_title} Picks")
    lines.append(f"*{actual_count} hand-picked movies from free streaming platforms \u2014 generated {now}*\n")

    # Quick-links table
    lines.append("## \U0001f4de Platform Quick Links\n")
    lines.append("| Platform | URL |")
    lines.append("|----------|-----|")
    for pname, purl in PLATFORM_LINKS.items():
        lines.append(f"| [{pname}]({purl}) | {purl} |")
    lines.append("")

    # Movies
    lines.append(f"## {emoji} {mood_title} Movie Recommendations\n")

    for i, movie in enumerate(selected, 1):
        platform_url = PLATFORM_LINKS.get(movie["platform"], "https://youtube.com")
        backup_url = PLATFORM_LINKS.get(movie["backup_platform"], "https://youtube.com")

        lines.append(f"### {i}. {movie['title']} ({movie['year']})")
        lines.append(f"**Platform:** [{movie['platform']}]({platform_url})")
        lines.append(f"\n**Why You'll Love It:** {movie['why']}")
        lines.append(f"\n**Best For:** {movie['best_for']}")
        lines.append(f"\n**\U0001f504 Backup Option:** [{movie['backup']}]({backup_url}) on {movie['backup_platform']}")
        lines.append("")

    # Tips section
    lines.append("---\n")
    lines.append("## \U0001f4a1 Movie Night Tips\n")
    lines.append("- **Check all platforms** \u2014 availability rotates. If your top pick isn't available, use the backup!")
    lines.append("- **Create an account** on Tubi and Pluto TV for watchlists and better recommendations.")
    lines.append("- **Use \"Free with Ads\" filters** on YouTube Movies to find free titles quickly.")
    lines.append("- **Mix decades** \u2014 pair an old classic with a newer title for variety.")
    lines.append("- **Snack pairing:** Make stovetop popcorn with real butter for the authentic experience.")
    lines.append("")

    lines.append(f"*\U0001f3ac Happy watching! \u2014 Generated {now}*\n")

    return "\n".join(lines)


def main():
    """Parse arguments and generate the movie plan."""
    parser = argparse.ArgumentParser(
        description="Generate a personalized movie night plan from free streaming platforms.",
        epilog="Example: python movie_planner.py --mood funny --count 5 --output funny_night.md",
    )
    parser.add_argument(
        "--mood",
        choices=list(MOOD_EMOJIS.keys()),
        required=True,
        help="Mood for movie recommendations: funny, scary, romantic, action, slow, deep",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of movie recommendations (default: 10)",
    )
    parser.add_argument(
        "--output",
        default="movie_night.md",
        help="Output markdown file path (default: movie_night.md)",
    )

    args = parser.parse_args()

    if args.count < 1 or args.count > 50:
        print("Error: --count must be between 1 and 50.", file=sys.stderr)
        sys.exit(1)

    try:
        content = generate_plan(mood=args.mood, count=args.count)

        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)

        abs_path = os.path.abspath(args.output)
        emoji = MOOD_EMOJIS[args.mood]
        print(f"\n{'='*60}")
        print(f"  {emoji} Movie Night Plan Generated Successfully!")
        print(f"{'='*60}")
        print(f"  \U0001f4c4 File:     {abs_path}")
        print(f"  \U0001f4a1 Mood:    {args.mood}")
        print(f"  \U0001f3ac Movies:   {min(args.count, len(MOVIES[args.mood]))}")
        print(f"  \U0001f527 Backups:  Each movie has a backup option")
        print(f"{'='*60}\n")

    except PermissionError:
        print(f"Error: Permission denied writing to '{args.output}'.", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: Could not write file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
