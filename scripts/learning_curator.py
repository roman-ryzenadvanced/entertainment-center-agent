#!/usr/bin/env python3
"""
Documentary & Learning Curator
===============================
Finds free documentaries on YouTube and ad-supported platforms. Recommends free
courses from Khan Academy, Coursera (audit mode), MIT OCW, and YouTube Edu.
Generates a weekly learning schedule with topic progression paths.

Usage:
    python learning_curator.py --topics "history,science,programming"
    python learning_curator.py --level intermediate --output learn_plan.md
"""

import argparse
import sys
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Documentary database by topic
# Each entry: title, platform, duration, description, url, subtopics
# ---------------------------------------------------------------------------
DOCUMENTARIES = {
    "history": [
        {"title": "The Vietnam War (Ken Burns)", "platform": "YouTube", "duration": "18 hours (series)",
         "desc": "Ken Burns' definitive documentary on the Vietnam War. Personal accounts from all sides, stunning footage, and an unflinching look at America's most divisive conflict.",
         "url": "https://youtube.com/results?search_query=ken+burns+vietnam+war+documentary",
         "subtopics": ["Cold War", "Military History", "Asian History"]},
        {"title": "13th", "platform": "YouTube", "duration": "1h 40m",
         "desc": "Ava DuVernay's powerful documentary exploring the intersection of race, justice, and mass incarceration in the United States. Essential viewing.",
         "url": "https://youtube.com/watch?v=K6IXSb9TTMA",
         "subtopics": ["Civil Rights", "Criminal Justice", "African American History"]},
        {"title": "Civilisation (Kenneth Clark)", "platform": "YouTube", "duration": "9 hours (series)",
         "desc": "The landmark 1969 BBC series on Western art and culture. Clark traces civilization from the Dark Ages to the 20th century. A masterclass in cultural history.",
         "url": "https://youtube.com/results?search_query=civilisation+kenneth+clark+bbc",
         "subtopics": ["Art History", "Western Civilization", "Culture"]},
        {"title": "The World at War", "platform": "Tubi", "duration": "22 hours (series)",
         "desc": "The definitive documentary on World War II. 26 episodes covering every major theater and perspective. Made with extraordinary access to survivors and archives.",
         "url": "https://tubitv.com",
         "subtopics": ["World War II", "Military History", "European History"]},
        {"title": "The Ascent of Man", "platform": "YouTube", "duration": "8 hours (series)",
         "desc": "Jacob Bronowski's beautiful 1973 series on the history of science and human achievement. A philosophical journey through human discovery.",
         "url": "https://youtube.com/results?search_query=ascent+of+man+bronowski",
         "subtopics": ["History of Science", "Human Civilization", "Philosophy"]},
        {"title": "Hiroshima", "platform": "YouTube", "duration": "90 minutes",
         "desc": "BBC documentary on the atomic bombing of Hiroshima. Combines survivor testimonies with CGI reconstruction. Devastating and essential.",
         "url": "https://youtube.com/results?search_query=hiroshima+bbc+documentary",
         "subtopics": ["World War II", "Nuclear History", "Japanese History"]},
        {"title": "The Civil War (Ken Burns)", "platform": "YouTube", "duration": "11 hours (series)",
         "desc": "The documentary that made Ken Burns famous. The American Civil War told through letters, diaries, and photographs. Unforgettable narration by David McCullough.",
         "url": "https://youtube.com/results?search_query=ken+burns+civil+war+documentary",
         "subtopics": ["American History", "Civil War", "Military History"]},
        {"title": "Roman Empire in the First Century", "platform": "YouTube", "duration": "4 hours (series)",
         "desc": "PBS series covering the rise and early years of the Roman Empire. Augustus, Tiberius, Caligula, and Claudius brought to life.",
         "url": "https://youtube.com/results?search_query=roman+empire+first+century+pbs",
         "subtopics": ["Ancient Rome", "Classical History", "European History"]},
        {"title": "Ancient Apocalypse", "platform": "Netflix (trailer free on YouTube) / YouTube", "duration": "6 hours (series)",
         "desc": "Graham Hancock explores evidence of lost civilizations. Controversial but thought-provoking examination of prehistoric human achievement.",
         "url": "https://youtube.com/results?search_query=ancient+apocalypse+documentary",
         "subtopics": ["Archaeology", "Prehistoric", "Ancient Civilizations"]},
        {"title": "The Great War Channel", "platform": "YouTube", "duration": "Ongoing series",
         "desc": "Week-by-week coverage of World War I, exactly 100 years after events occurred. Incredibly detailed and engaging.",
         "url": "https://youtube.com/@TheGreatWar",
         "subtopics": ["World War I", "Military History", "European History"]},
    ],
    "science": [
        {"title": "Cosmos: A Spacetime Odyssey", "platform": "YouTube", "duration": "13 hours (series)",
         "desc": "Neil deGrasse Tyson hosts this stunning update of Carl Sagan's classic. The universe explained with breathtaking visual effects and infectious wonder.",
         "url": "https://youtube.com/results?search_query=cosmos+spacetime+odyssey+neil",
         "subtopics": ["Astronomy", "Physics", "Space"]},
        {"title": "Planet Earth II", "platform": "YouTube", "duration": "6 hours (series)",
         "desc": "David Attenborough narrates this breathtaking nature series. From islands to mountains, cities to jungles. The camerawork is miraculous.",
         "url": "https://youtube.com/results?search_query=planet+earth+ii+attenborough",
         "subtopics": ["Nature", "Biology", "Ecology"]},
        {"title": "Particle Fever", "platform": "YouTube", "duration": "1h 39m",
         "desc": "Follows the inside story of six scientists during the launch of the Large Hadron Collider and the discovery of the Higgs boson. Science as drama.",
         "url": "https://youtube.com/results?search_query=particle+fever+documentary",
         "subtopics": ["Physics", "Particle Physics", "CERN"]},
        {"title": "The Code", "platform": "YouTube", "duration": "3 hours (series)",
         "desc": "Marcus du Sautoy explores how numbers, shapes, and patterns underpin the universe. Mathematics revealed as the hidden language of reality.",
         "url": "https://youtube.com/results?search_query=marcus+du+sautoy+the+code",
         "subtopics": ["Mathematics", "Patterns", "Information Theory"]},
        {"title": "Your Inner Fish", "platform": "YouTube", "duration": "3 hours (series)",
         "desc": "Neil Shubin traces human anatomy back to our fish ancestors. An evolutionary detective story that will change how you see your own body.",
         "url": "https://youtube.com/results?search_query=your+inner+fish+documentary",
         "subtopics": ["Evolution", "Biology", "Anatomy"]},
        {"title": "Wonders of the Solar System", "platform": "YouTube", "duration": "5 hours (series)",
         "desc": "Professor Brian Cox tours the solar system's most spectacular phenomena. Science communication at its most visually stunning.",
         "url": "https://youtube.com/results?search_query=wonders+of+the+solar+system+brian+cox",
         "subtopics": ["Astronomy", "Planetary Science", "Geology"]},
        {"title": "My Octopus Teacher", "platform": "Netflix (clip on YouTube) / YouTube", "duration": "1h 25m",
         "desc": "A filmmaker forms an unlikely friendship with a wild octopus. A meditation on nature, connection, and the intelligence of other species.",
         "url": "https://youtube.com/results?search_query=my+octopus+teacher",
         "subtopics": ["Marine Biology", "Nature", "Animal Intelligence"]},
        {"title": "The Brain with David Eagleman", "platform": "YouTube", "duration": "6 hours (series)",
         "desc": "Neuroscientist David Eagleman explores how the brain constructs reality. Time, reality, decision-making, and the future explained.",
         "url": "https://youtube.com/results?search_query=brain+david+eagleman+pbs",
         "subtopics": ["Neuroscience", "Psychology", "Consciousness"]},
        {"title": "Human Universe", "platform": "YouTube", "duration": "5 hours (series)",
         "desc": "Brian Cox asks why we exist. From the Big Bang to consciousness, this series connects physics, biology, and philosophy.",
         "url": "https://youtube.com/results?search_query=human+universe+brian+cox",
         "subtopics": ["Physics", "Biology", "Consciousness"]},
        {"title": "Apollo 11 (2019)", "platform": "YouTube", "duration": "1h 53m",
         "desc": "Composed entirely of archival footage from the Apollo 11 mission. The Moon landing in real-time. No narration, just the awe of the event.",
         "url": "https://youtube.com/results?search_query=apollo+11+2019+documentary",
         "subtopics": ["Space Exploration", "NASA", "Engineering"]},
    ],
    "technology": [
        {"title": "AlphaGo", "platform": "YouTube", "duration": "1h 30m",
         "desc": "The story of DeepMind's AI defeating the world champion Go player. Humanity vs. machine intelligence told with genuine drama.",
         "url": "https://youtube.com/results?search_query=alphago+documentary",
         "subtopics": ["AI", "Machine Learning", "Go"]},
        {"title": "The Social Dilemma", "platform": "YouTube", "duration": "1h 34m",
         "desc": "Tech insiders reveal how social media is reprogramming civilization. Essential for understanding the attention economy and its costs.",
         "url": "https://youtube.com/results?search_query=social+dilemma+documentary",
         "subtopics": ["Social Media", "AI", "Tech Ethics"]},
        {"title": "Lo and Behold: Reveries of the Connected World", "platform": "YouTube", "duration": "1h 28m",
         "desc": "Werner Herzog explores the internet and connected technology with his unique philosophical lens. Ten chapters on our digital existence.",
         "url": "https://youtube.com/results?search_query=lo+and+behold+herzog",
         "subtopics": ["Internet", "Digital Culture", "Philosophy of Technology"]},
        {"title": "The Inventor: Out for Blood in Silicon Valley", "platform": "YouTube", "duration": "1h 59m",
         "desc": "The Theranos story \u2014 Elizabeth Holmes' rise and fall. A cautionary tale about Silicon Valley's fake-it-till-you-make-it culture.",
         "url": "https://youtube.com/results?search_query=theranos+inventor+documentary",
         "subtopics": ["Startups", "Fraud", "Biotech"]},
        {"title": "Code: Debugging the Gender Gap", "platform": "YouTube", "duration": "1h 18m",
         "desc": "Explores the gender gap in tech, its causes, and the women working to close it. Eye-opening for anyone in the industry.",
         "url": "https://youtube.com/results?search_query=code+debugging+gender+gap",
         "subtopics": ["Gender", "Tech Industry", "Education"]},
        {"title": "Coded Bias", "platform": "YouTube", "duration": "1h 25m",
         "desc": "MIT Media Lab researcher Joy Buolamwini discovers racial bias in facial recognition algorithms. A call for algorithmic accountability.",
         "url": "https://youtube.com/results?search_query=coded+bias+documentary",
         "subtopics": ["AI Ethics", "Bias", "Facial Recognition"]},
        {"title": "Inside the Mind of Google", "platform": "YouTube", "duration": "45 minutes",
         "desc": "CNBC documentary exploring Google's data empire, search algorithms, and the implications of organizing all the world's information.",
         "url": "https://youtube.com/results?search_query=inside+mind+of+google+documentary",
         "subtopics": ["Google", "Data", "Search"]},
        {"title": "The Internet's Own Boy", "platform": "YouTube", "duration": "1h 45m",
         "desc": "The story of Aaron Swartz \u2014 programmer, activist, and co-founder of Reddit. A tragic tale of information freedom vs. government power.",
         "url": "https://youtube.com/results?search_query=internets+own+boy+aaron+swartz",
         "subtopics": ["Internet Freedom", "Open Access", "Activism"]},
    ],
    "nature": [
        {"title": "Blue Planet II", "platform": "YouTube", "duration": "6 hours (series)",
         "desc": "David Attenborough explores the ocean depths. Captures creatures and behaviors never before filmed. A love letter to the sea.",
         "url": "https://youtube.com/results?search_query=blue+planet+ii+attenborough",
         "subtopics": ["Marine Biology", "Ocean", "Ecology"]},
        {"title": "Our Planet", "platform": "Netflix (clips on YouTube) / YouTube", "duration": "8 hours (series)",
         "desc": "Netflix's nature documentary with Attenborough. Focuses on the impact of climate change on ecosystems. Visually spectacular.",
         "url": "https://youtube.com/results?search_query=our+planet+netflix+nature",
         "subtopics": ["Climate Change", "Ecology", "Wildlife"]},
        {"title": "March of the Penguins", "platform": "YouTube", "duration": "1h 25m",
         "desc": "Emperor penguins' extraordinary Antarctic journey to breed. Morgan Freeman narrates this Oscar-winning nature film.",
         "url": "https://youtube.com/results?search_query=march+of+the+penguins",
         "subtopics": ["Antarctica", "Birds", "Animal Behavior"]},
        {"title": "The Hidden Life of Trees", "platform": "YouTube", "duration": "45 minutes",
         "desc": "Based on Peter Wohlleben's book. Explores how trees communicate through fungal networks. Will change how you see forests.",
         "url": "https://youtube.com/results?search_query=hidden+life+of+trees+documentary",
         "subtopics": ["Botany", "Ecology", "Fungi"]},
        {"title": "Microcosmos", "platform": "YouTube", "duration": "1h 22m",
         "desc": "A microscopic journey through a French meadow. Insects become epic heroes. The cinematography is beyond belief.",
         "url": "https://youtube.com/results?search_query=microcosmos+documentary+insects",
         "subtopics": ["Insects", "Microbiology", "Nature"]},
        {"title": "Earth: The Nature of Our Planet", "platform": "YouTube", "duration": "6 hours (series)",
         "desc": "Explores the forces that shaped Earth \u2014 volcanoes, oceans, weather, and ice. National Geographic at its finest.",
         "url": "https://youtube.com/results?search_query=national+geographic+earth+documentary",
         "subtopics": ["Geology", "Climate", "Earth Science"]},
    ],
    "psychology": [
        {"title": "The Mind, Explained", "platform": "YouTube", "duration": "3 hours (series)",
         "desc": "Vox's series on how the mind works \u2014 dreams, anxiety, mindfulness, memory. Clean animation and clear explanations.",
         "url": "https://youtube.com/results?search_query=vox+mind+explained+netflix",
         "subtopics": ["Mental Health", "Neuroscience", "Consciousness"]},
        {"title": "The Century of the Self", "platform": "YouTube", "duration": "4 hours (series)",
         "desc": "Adam Curtis explores how Freud's theories were used by corporations and governments to control people. A foundational documentary on propaganda.",
         "url": "https://youtube.com/results?search_query=century+of+the+self+adam+curtis",
         "subtopics": ["Freud", "Propaganda", "Consumer Culture"]},
        {"title": "Three Identical Strangers", "platform": "YouTube", "duration": "1h 36m",
         "desc": "Triplets separated at birth discover each other at age 19. A story about nature vs. nurture that takes a dark turn.",
         "url": "https://youtube.com/results?search_query=three+identical+strangers+documentary",
         "subtopics": ["Nature vs. Nurture", "Psychology", "Ethics"]},
        {"title": "The Power of Nightmares", "platform": "YouTube", "duration": "3 hours (series)",
         "desc": "Adam Curtis examines how politicians used fear to gain power. Compares neoconservatism and Islamic fundamentalism as parallel movements.",
         "url": "https://youtube.com/results?search_query=power+of+nightmares+adam+curtis",
         "subtopics": ["Political Psychology", "Fear", "Ideology"]},
        {"title": "HyperNormalisation", "platform": "YouTube", "duration": "2h 46m",
         "desc": "Adam Curtis' most acclaimed documentary on how politicians, financiers, and technological utopians built a fake world. Profound.",
         "url": "https://youtube.com/results?search_query=hypernormalisation+adam+curtis",
         "subtopics": ["Post-Truth", "Politics", "Media"]},
        {"title": "Stress: Portrait of a Killer", "platform": "YouTube", "duration": "56 minutes",
         "desc": "National Geographic explores how chronic stress damages the body and brain. Stanford's Robert Sapolsky is the guide.",
         "url": "https://youtube.com/results?search_query=stress+portrait+of+a+killer",
         "subtopics": ["Stress", "Health", "Neuroscience"]},
    ],
    "economics": [
        {"title": "Inside Job", "platform": "YouTube", "duration": "1h 49m",
         "desc": "Oscar-winning documentary on the 2008 financial crisis. Interviews, archival footage, and a clear explanation of systemic fraud.",
         "url": "https://youtube.com/results?search_query=inside+job+documentary+2008",
         "subtopics": ["Financial Crisis", "Banking", "Regulation"]},
        {"title": "The Corporation", "platform": "YouTube", "duration": "2h 25m",
         "desc": "If a corporation were a person, what kind of person would it be? A chilling diagnosis of corporate behavior and power.",
         "url": "https://youtube.com/results?search_query=the+corporation+documentary",
         "subtopics": ["Corporate Power", "Capitalism", "Ethics"]},
        {"title": "Inequality for All", "platform": "YouTube", "duration": "1h 29m",
         "desc": "Robert Reich explains America's growing wealth inequality with clarity, humor, and urgency. A perfect introduction to the topic.",
         "url": "https://youtube.com/results?search_query=inequality+for+all+documentary",
         "subtopics": ["Inequality", "Labor", "Policy"]},
        {"title": "Capitalism: A Love Story", "platform": "YouTube", "duration": "2h 7m",
         "desc": "Michael Moore's exploration of the 2008 financial crisis and capitalism's impact on ordinary Americans. Provocative and accessible.",
         "url": "https://youtube.com/results?search_query=capitalism+love+story+michael+moore",
         "subtopics": ["Capitalism", "Financial Crisis", "American Economy"]},
        {"title": "The Big Short (real story)", "platform": "YouTube / Tubi", "duration": "1h 30m+",
         "desc": "Multiple documentaries explain the real events behind the housing bubble. Watch for the context the movie couldn't fully cover.",
         "url": "https://youtube.com/results?search_query=2008+housing+crisis+explained+documentary",
         "subtopics": ["Housing", "Finance", "Regulation"]},
        {"title": "Enron: The Smartest Guys in the Room", "platform": "Tubi", "duration": "1h 50m",
         "desc": "The inside story of Enron's spectacular collapse. Corporate fraud, hubris, and the human cost of unchecked greed.",
         "url": "https://tubitv.com",
         "subtopics": ["Corporate Fraud", "Accounting", "Business Ethics"]},
    ],
}

# ---------------------------------------------------------------------------
# Free course database by topic and level
# Each entry: title, provider, duration, description, url, level
# ---------------------------------------------------------------------------
COURSES = {
    "programming": [
        {"title": "CS50: Introduction to Computer Science", "provider": "Harvard (via freeCodeCamp mirror)",
         "duration": "12 weeks", "level": "beginner",
         "desc": "The most popular intro CS course in the world. Covers C, Python, SQL, HTML/CSS, and more. Real problem sets, real learning.",
         "url": "https://freecodecamp.org/learn/scientific-computing-with-python",
         "path": "Start here if you have zero programming experience"},
        {"title": "Python for Everybody", "provider": "University of Michigan (Coursera audit)",
         "duration": "8 months", "level": "beginner",
         "desc": "Dr. Charles Severance's beloved Python course. Gentle introduction to programming through data processing and web scraping.",
         "url": "https://coursera.org/specializations/python",
         "path": "Take after CS50 or as a standalone Python introduction"},
        {"title": "Introduction to Computer Science and Programming", "provider": "MIT OCW",
         "duration": "1 semester", "level": "beginner",
         "desc": "MIT's 6.00SC course. Learn computation through Python. Lectures, assignments, and exams all available free.",
         "url": "https://ocw.mit.edu/courses/6-00sc-introduction-to-computer-science-and-programming-spring-2011",
         "path": "Alternative to CS50 with a more academic approach"},
        {"title": "JavaScript Algorithms and Data Structures", "provider": "freeCodeCamp",
         "duration": "300 hours", "level": "intermediate",
         "desc": "Complete JavaScript curriculum with projects. Earn a certification. Covers algorithms, regex, OOP, and functional programming.",
         "url": "https://freecodecamp.org/learn/javascript-algorithms-and-data-structures",
         "path": "After Python basics, add JavaScript to your toolkit"},
        {"title": "Introduction to Algorithms", "provider": "MIT OCW",
         "duration": "1 semester", "level": "advanced",
         "desc": "MIT's legendary 6.006 course. Covers sorting, searching, graph algorithms, dynamic programming. The gold standard.",
         "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011",
         "path": "After programming basics, study algorithm design"},
        {"title": "Computer Architecture", "provider": "MIT OCW",
         "duration": "1 semester", "level": "advanced",
         "desc": "MIT's 6.004 course. How computers work from transistors up. Essential for understanding performance optimization.",
         "url": "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-004-computation-structures-spring-2017",
         "path": "After algorithms, understand the hardware layer"},
    ],
    "mathematics": [
        {"title": "Khan Academy: Algebra I", "provider": "Khan Academy",
         "duration": "Self-paced", "level": "beginner",
         "desc": "Complete algebra curriculum with exercises, practice problems, and mastery tracking. The best free math education available.",
         "url": "https://khanacademy.org/math/algebra",
         "path": "Start your math journey here"},
        {"title": "Khan Academy: Calculus", "provider": "Khan Academy",
         "duration": "Self-paced", "level": "intermediate",
         "desc": "Limits, derivatives, integrals, and applications. Visual, intuitive, and complete. Goes from basic to advanced step by step.",
         "url": "https://khanacademy.org/math/calculus-1",
         "path": "After algebra, move to calculus"},
        {"title": "3Blue1Brown: Essence of Calculus", "provider": "YouTube",
         "duration": "3 hours", "level": "intermediate",
         "desc": "Grant Sanderson's visual calculus series. See the intuition behind derivatives and integrals through stunning animations.",
         "url": "https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr",
         "path": "Watch alongside Khan Academy for deeper understanding"},
        {"title": "MIT: Single Variable Calculus", "provider": "MIT OCW",
         "duration": "1 semester", "level": "intermediate",
         "desc": "MIT's 18.01 course with David Jerison. Rigorous calculus education with complete lectures and problem sets.",
         "url": "https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010",
         "path": "After visual calculus, study the formal proofs"},
        {"title": "MIT: Linear Algebra", "provider": "MIT OCW",
         "duration": "1 semester", "level": "intermediate",
         "desc": "Gilbert Strang's legendary 18.06 course. Applications in computer science, physics, and engineering. Watch the lectures on YouTube.",
         "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010",
         "path": "After calculus, linear algebra is the next pillar"},
        {"title": "Discrete Mathematics", "provider": "MIT OCW (242J) / YouTube",
         "duration": "1 semester", "level": "advanced",
         "desc": "Logic, sets, counting, graph theory. Essential for computer science and mathematical reasoning.",
         "url": "https://youtube.com/results?search_query=MIT+discrete+mathematics+lectures",
         "path": "After linear algebra, tackle discrete math"},
    ],
    "science": [
        {"title": "Khan Academy: Physics", "provider": "Khan Academy",
         "duration": "Self-paced", "level": "beginner",
         "desc": "Mechanics, electricity, magnetism, and more. Interactive exercises and video explanations. Start from zero.",
         "url": "https://khanacademy.org/science/physics",
         "path": "Begin your physics education here"},
        {"title": "Walter Lewin Physics Lectures", "provider": "MIT OCW (YouTube)",
         "duration": "1 semester", "level": "beginner",
         "desc": "Legendary MIT lectures with spectacular demonstrations. Lewin makes physics visceral and unforgettable.",
         "url": "https://youtube.com/results?search_query=walter+lewin+physics+lectures",
         "path": "Watch alongside Khan Academy for a complete experience"},
        {"title": "CrashCourse Chemistry", "provider": "YouTube",
         "duration": "11 hours", "level": "beginner",
         "desc": "Hank Green's energetic chemistry course. Atoms, bonds, reactions, and everything in between. Fast-paced and engaging.",
         "url": "https://youtube.com/playlist?list=PL8bPuZa3L9I5apj5KEsHIy6kr3lIpqSKv",
         "path": "Complement physics with chemistry basics"},
        {"title": "Khan Academy: Organic Chemistry", "provider": "Khan Academy",
         "duration": "Self-paced", "level": "intermediate",
         "desc": "Complete organic chemistry curriculum. Functional groups, reaction mechanisms, and synthesis strategies.",
         "url": "https://khanacademy.org/science/organic-chemistry",
         "path": "After general chemistry, specialize in organic"},
        {"title": "MIT: Biology", "provider": "MIT OCW",
         "duration": "1 semester", "level": "intermediate",
         "desc": "MIT's 7.01SC introductory biology. Molecular biology, genetics, cell biology with problem sets and exams.",
         "url": "https://ocw.mit.edu/courses/7-01sc-fundamentals-of-biology-fall-2011",
         "path": "After chemistry basics, study molecular biology"},
        {"title": "Khan Academy: AP Chemistry", "provider": "Khan Academy",
         "duration": "Self-paced", "level": "advanced",
         "desc": "College-level chemistry with AP-style questions. Thermodynamics, equilibrium, electrochemistry, and more.",
         "url": "https://khanacademy.org/science/ap-chemistry",
         "path": "Preparation for college chemistry or AP exams"},
    ],
    "history": [
        {"title": "CrashCourse World History", "provider": "YouTube",
         "duration": "15 hours", "level": "beginner",
         "desc": "John Green's rapid-fire world history from agricultural revolution to globalization. The perfect overview.",
         "url": "https://youtube.com/playlist?list=PLBDA2E52FB1EF80C9",
         "path": "Start here for a world history foundation"},
        {"title": "CrashCourse US History", "provider": "YouTube",
         "duration": "12 hours", "level": "beginner",
         "desc": "American history from pre-Columbian civilizations to the Obama era. Fast, funny, and surprisingly deep.",
         "url": "https://youtube.com/playlist?list=PL8dPuuaLjXtMwmep6j7g7eh6ggBTOFzNZ",
         "path": "After world history, focus on American history"},
        {"title": "Yale: The Civil War and Reconstruction Era", "provider": "Yale OYC",
         "duration": "1 semester", "level": "intermediate",
         "desc": "Professor David Blight's acclaimed course on the Civil War. Deep analysis of the conflict that shaped modern America.",
         "url": "https://oyc.yale.edu/courses/civil-war-and-reconstruction-era-1845-1877",
         "path": "After US history overview, deep-dive into the Civil War"},
        {"title": "Coursera: The Ancient Greeks", "provider": "Wesleyan University (audit)",
         "duration": "7 weeks", "level": "intermediate",
         "desc": "Greek history from Bronze Age to Alexander the Great. Philosophy, democracy, and the foundations of Western thought.",
         "url": "https://coursera.org/learn/ancient-greeks",
         "path": "After world history, specialize in ancient civilizations"},
        {"title": "MIT: US History since 1877", "provider": "MIT OCW",
         "duration": "1 semester", "level": "advanced",
         "desc": "MIT's American history course from Reconstruction to the present. Academic rigor applied to recent history.",
         "url": "https://ocw.mit.edu/courses/history/21h-187j-us-history-since-1865-spring-2018",
         "path": "After ancient and US history, study modern American history"},
        {"title": "Harvard: ChinaX", "provider": "Harvard (edX audit)",
         "duration": "10 weeks", "level": "advanced",
         "desc": "Comprehensive Chinese civilization from ancient times to today. Ten parts covering 5,000 years of history.",
         "url": "https://www.edx.org/learn/china/harvard-university-chinax",
         "path": "After Western history, broaden to Eastern civilizations"},
    ],
    "art": [
        {"title": "Khan Academy: Art History", "provider": "Khan Academy",
         "duration": "Self-paced", "level": "beginner",
         "desc": "From prehistoric art to modern movements. Smarthistory videos cover every major period and artist with context.",
         "url": "https://khanacademy.org/humanities/art-history",
         "path": "Start your art education here"},
        {"title": "CrashCourse Art History", "provider": "YouTube",
         "duration": "8 hours", "level": "beginner",
         "desc": "A fast tour through art history from cave paintings to contemporary art. Great for building a mental timeline.",
         "url": "https://youtube.com/results?search_query=crashcourse+art+history",
         "path": "Watch alongside Khan Academy for breadth"},
        {"title": "MoMA: What Is Contemporary Art?", "provider": "Coursera (audit)",
         "duration": "5 weeks", "level": "intermediate",
         "desc": "The Museum of Modern Art's course exploring contemporary art through its collection. Artists, themes, and techniques.",
         "url": "https://coursera.org/learn/what-is-contemporary-art",
         "path": "After art history basics, understand the contemporary scene"},
        {"title": "Coursera: Modern Art and Ideas", "provider": "MoMA (audit)",
         "duration": "5 weeks", "level": "intermediate",
         "desc": "Explore art themes \u2014 Places & Spaces, Art & Identity, Transforming Everyday Objects, and Art & Society.",
         "url": "https://coursera.org/learn/modern-art-ideas",
         "path": "After contemporary art overview, explore themes"},
        {"title": "Yale: Roman Architecture", "provider": "Yale OYC",
         "duration": "1 semester", "level": "advanced",
         "desc": "Professor Diana Kleiner's comprehensive course on Roman architecture from Romulus to Constantine.",
         "url": "https://oyc.yale.edu/courses/roman-architecture",
         "path": "After general art history, specialize in architecture"},
        {"title": "Khan Academy: Music Theory", "provider": "Khan Academy",
         "duration": "Self-paced", "level": "beginner",
         "desc": "Basic music theory from notes and scales to chords and composition. Learn to read and understand music.",
         "url": "https://khanacademy.org/humanities/music",
         "path": "Complement art studies with music fundamentals"},
    ],
}

# ---------------------------------------------------------------------------
# Topic aliases
# ---------------------------------------------------------------------------
TOPIC_ALIASES = {
    "history": "history", "world-history": "history", "ancient": "history",
    "science": "science", "physics": "science", "chemistry": "science", "biology": "science",
    "tech": "technology", "technology": "technology", "ai": "technology", "computing": "technology",
    "nature": "nature", "wildlife": "nature", "environment": "nature", "ecology": "nature",
    "psychology": "psychology", "psych": "psychology", "mental-health": "psychology", "brain": "psychology",
    "economics": "economics", "econ": "economics", "finance": "economics", "money": "economics",
    "programming": "programming", "coding": "programming", "computer-science": "programming", "cs": "programming",
    "code": "programming", "python": "programming", "javascript": "programming",
    "math": "mathematics", "mathematics": "mathematics", "calculus": "mathematics", "algebra": "mathematics",
    "art": "art", "art-history": "art", "music": "art", "design": "art",
}

# ---------------------------------------------------------------------------
# Free learning platforms
# ---------------------------------------------------------------------------
LEARNING_PLATFORMS = {
    "Khan Academy": {"url": "https://khanacademy.org", "desc": "K-12 + college level. Math, science, computing, humanities. Exercises included."},
    "MIT OCW": {"url": "https://ocw.mit.edu", "desc": "Virtually all MIT courses. Lectures, notes, exams. University-level education."},
    "Coursera (audit)": {"url": "https://coursera.org", "desc": "Audit 7,000+ courses from top universities for free. No certificate unless paid."},
    "freeCodeCamp": {"url": "https://freecodecamp.org", "desc": "Full-stack web dev, Python, data science. Free certifications. Interactive."},
    "YouTube Edu": {"url": "https://youtube.com/education", "desc": "CrashCourse, TED-Ed, Kurzgesagt, 3Blue1Brown, and thousands more."},
    "Yale OYC": {"url": "https://oyc.yale.edu", "desc": "Yale's open courses. Literature, history, philosophy, science."},
    "OpenLearn (OU)": {"url": "https://open.edu/openlearn", "desc": "Open University's free courses. 1,000+ courses across all subjects."},
    "edX (audit)": {"url": "https://edx.org", "desc": "Harvard, MIT, and 160+ institutions. Audit courses for free."},
    "TED-Ed": {"url": "https://ed.ted.com", "desc": "Animated lessons on every topic. 5-10 minute lessons from great educators."},
    "NOVA (PBS)": {"url": "https://pbs.org/nova", "desc": "Free science documentaries from PBS. Full episodes available online."},
}

# ---------------------------------------------------------------------------
# Weekly schedule template
# ---------------------------------------------------------------------------
WEEK_SCHEDULE = [
    {"day": "Monday", "morning": "\U0001f52c New concept", "afternoon": "\U0001f4dd Practice exercises", "evening": "\U0001f3ac Documentary on topic"},
    {"day": "Tuesday", "morning": "\U0001f4da Reading / notes review", "afternoon": "\U0001f50d Deep-dive lecture", "evening": "\U0001f399\ufe0f Educational podcast"},
    {"day": "Wednesday", "morning": "\U0001f9e9 Problem solving", "afternoon": "\U0001f52c Continue new material", "evening": "\U0001f3ac Related documentary"},
    {"day": "Thursday", "morning": "\U0001f4dd Practice / exercises", "afternoon": "\U0001f9e9 Review & catch up", "evening": "\U0001f3ac Light documentary"},
    {"day": "Friday", "morning": "\U0001f50d Bonus lecture", "afternoon": "\U0001f4da Supplementary reading", "evening": "\U0001f525 Tackle a challenge"},
    {"day": "Saturday", "morning": "\U0001f3af Project work", "afternoon": "\U0001f3ae Educational game / simulation", "evening": "\U0001f3ac Movie/documentary on topic"},
    {"day": "Sunday", "morning": "\U0001f9d8 Rest & reflection", "afternoon": "\U0001f4cb Weekly review & planning", "evening": "\U0001f319 Light review / set next week"},
]


def generate_plan(topics, level):
    """Generate the learning plan as markdown."""
    now = datetime.now().strftime("%B %d, %Y")
    lines = []

    lines.append(f"# \U0001f393 Documentary & Learning Plan")
    lines.append(f"*Free documentaries and courses tailored to your interests \u2014 {now}*\n")

    # Normalize topics
    normalized_docs = set()
    normalized_courses = set()
    for t in topics:
        key = TOPIC_ALIASES.get(t.lower().strip(), t.lower().strip())
        if key in DOCUMENTARIES:
            normalized_docs.add(key)
        if key in COURSES:
            normalized_courses.add(key)

    if not normalized_docs and not normalized_courses:
        normalized_docs = {"science", "history", "technology"}
        normalized_courses = {"programming", "science", "history"}
        print("Info: No matching topics found. Using defaults: science, history, technology, programming.", file=sys.stderr)

    # --- Platform overview ---
    lines.append("## \U0001f3eb Free Learning Platforms\n")
    lines.append("| Platform | URL | Description |")
    lines.append("|----------|-----|-------------|")
    for name, info in LEARNING_PLATFORMS.items():
        lines.append(f"| [{name}]({info['url']}) | {info['url'].replace('https://', '')} | {info['desc']} |")
    lines.append("")

    # --- Documentary recommendations ---
    lines.append("## \U0001f3ac Documentary Recommendations\n")

    doc_count = 0
    for topic in sorted(normalized_docs):
        if topic not in DOCUMENTARIES:
            continue
        docs = DOCUMENTARIES[topic]
        doc_count += len(docs)
        topic_label = topic.replace("-", " ").title()
        topic_emojis = {
            "history": "\U0001f3db\ufe0f", "science": "\U0001f52c", "technology": "\U0001f4bb",
            "nature": "\U0001f30f", "psychology": "\U0001f9ec", "economics": "\U0001f4b0",
        }
        emoji = topic_emojis.get(topic, "\U0001f3ac")
        lines.append(f"### {emoji} {topic_label}\n")
        lines.append("| # | Title | Platform | Duration | Subtopics |")
        lines.append("|---|-------|----------|----------|----------|")

        for i, doc in enumerate(docs, 1):
            subtopics = ", ".join(doc["subtopics"][:3])
            lines.append(
                f"| {i} | [{doc['title']}]({doc['url']}) | {doc['platform']} | "
                f"{doc['duration']} | {subtopics} |"
            )
        lines.append("")

        lines.append(f"**Why watch:**\n")
        for doc in docs:
            lines.append(f"- **{doc['title']}:** {doc['desc']}")
        lines.append("")

    # --- Course recommendations ---
    lines.append("---\n")
    lines.append("## \U0001f4da Free Course Recommendations\n")

    course_count = 0
    for topic in sorted(normalized_courses):
        if topic not in COURSES:
            continue
        courses = COURSES[topic]
        # Filter by level
        level_courses = [c for c in courses if c["level"] == level]
        if not level_courses:
            level_courses = courses  # Show all if no match
        course_count += len(level_courses)

        topic_label = topic.replace("-", " ").title()
        lines.append(f"### {topic_label} ({level.title()})\n")
        lines.append("| # | Course | Provider | Duration | Progression Path |")
        lines.append("|---|--------|----------|----------|------------------|")

        for i, course in enumerate(level_courses, 1):
            lines.append(
                f"| {i} | [{course['title']}]({course['url']}) | "
                f"{course['provider']} | {course['duration']} | {course['path']} |"
            )
        lines.append("")

        lines.append(f"**Course details:**\n")
        for course in level_courses:
            lines.append(f"- **{course['title']}** ({course['provider']}): {course['desc']}")
        lines.append("")

    # --- Weekly learning schedule ---
    lines.append("---\n")
    lines.append("## \U0001f4c5 Weekly Learning Schedule\n")
    lines.append("| Day | Morning | Afternoon | Evening |")
    lines.append("|-----|---------|-----------|---------|")
    for day in WEEK_SCHEDULE:
        lines.append(f"| {day['day']} | {day['morning']} | {day['afternoon']} | {day['evening']} |")
    lines.append("")

    # --- Learning tips ---
    lines.append("---\n")
    lines.append("## \U0001f4a1 Learning Tips\n")
    lines.append("- **Follow progression paths** \u2014 the table above shows the recommended order for each subject.")
    lines.append("- **Audit on Coursera/edX** \u2014 you get all the video lectures and reading materials for free.")
    lines.append("- **Use the Feynman Technique** \u2014 explain what you learned in simple terms to solidify understanding.")
    lines.append("- **Space your learning** \u2014 study a topic over multiple days rather than cramming. Retention improves dramatically.")
    lines.append("- **Take real notes** \u2014 handwritten notes lead to better retention than highlighting or typing.")
    lines.append("- **Mix documentaries and courses** \u2014 documentaries build motivation; courses build skills. Use both.")
    lines.append("- **Join communities** \u2014 Reddit, Discord, and course forums provide support and accountability.")
    lines.append("- **Build projects** \u2014 apply what you learn immediately. Learning by doing is 10x more effective than watching alone.")
    lines.append("")

    total_items = doc_count + course_count
    lines.append(f"*\U0001f393 {total_items} learning resources curated ({doc_count} documentaries, {course_count} courses) \u2014 Generated {now}*\n")

    return "\n".join(lines)


def main():
    """Parse arguments and generate the learning plan."""
    parser = argparse.ArgumentParser(
        description="Discover free documentaries and courses with a weekly learning schedule.",
        epilog="Example: python learning_curator.py --topics 'science,history,programming' --level intermediate",
    )
    parser.add_argument(
        "--topics",
        default="science,history,technology",
        help="Comma-separated topics for documentaries and courses (default: science,history,technology)",
    )
    parser.add_argument(
        "--level",
        choices=["beginner", "intermediate", "advanced"],
        default="beginner",
        help="Difficulty level for course recommendations (default: beginner)",
    )
    parser.add_argument(
        "--output",
        default="learning_plan.md",
        help="Output markdown file path (default: learning_plan.md)",
    )

    args = parser.parse_args()

    topics = [t.strip() for t in args.topics.split(",") if t.strip()]

    try:
        content = generate_plan(topics=topics, level=args.level)

        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)

        abs_path = os.path.abspath(args.output)
        print(f"\n{'='*60}")
        print(f"  \U0001f393 Learning Plan Generated Successfully!")
        print(f"{'='*60}")
        print(f"  \U0001f4c4 File:      {abs_path}")
        print(f"  \U0001f52c Topics:    {', '.join(topics)}")
        print(f"  \U0001f3af Level:     {args.level}")
        print(f"  \U0001f3ac Sources:   Khan Academy, MIT OCW, Coursera, YouTube, freeCodeCamp")
        print(f"  \U0001f4c5 Schedule:  Weekly learning plan with progression paths")
        print(f"{'='*60}\n")

    except PermissionError:
        print(f"Error: Permission denied writing to '{args.output}'.", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: Could not write file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
