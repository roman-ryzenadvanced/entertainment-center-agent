#!/usr/bin/env python3
"""
Book & Podcast Discovery Tool
===============================
Finds free books from Project Gutenberg, Open Library, Librivox, and Smashwords.
Discovers free podcasts from Spotify, Apple Podcasts, and YouTube. Generates a
curated reading list and listening guide with a weekly schedule.

Usage:
    python book_podcast_finder.py --genres "science-fiction,mystery,history"
    python book_podcast_finder.py --output my_reads.md
"""

import argparse
import sys
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Free book database by genre
# Each entry: title, author, platform, description, link, format, page_est
# ---------------------------------------------------------------------------
BOOKS = {
    "science-fiction": [
        {"title": "The War of the Worlds", "author": "H.G. Wells",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The original alien invasion novel. Martians land in Victorian England and humanity faces annihilation. Wells' scientific imagination remains thrilling.",
         "link": "https://gutenberg.org/ebooks/36", "pages": 180},
        {"title": "The Time Machine", "author": "H.G. Wells",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A scientist travels to the year 802,701 and discovers a divided humanity. The grandfather of all time travel fiction.",
         "link": "https://gutenberg.org/ebooks/35", "pages": 130},
        {"title": "Twenty Thousand Leagues Under the Sea", "author": "Jules Verne",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Captain Nemo takes readers on an underwater odyssey aboard the Nautilus. Adventure and wonder on every page.",
         "link": "https://gutenberg.org/ebooks/164", "pages": 380},
        {"title": "Frankenstein", "author": "Mary Shelley",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The first science fiction novel. A creature assembled from dead tissue seeks meaning and revenge. Profoundly human.",
         "link": "https://gutenberg.org/ebooks/84", "pages": 280},
        {"title": "A Journey to the Center of the Earth", "author": "Jules Verne",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A German professor leads an expedition into a volcanic passage to the Earth's core. Pure Victorian adventure.",
         "link": "https://gutenberg.org/ebooks/18857", "pages": 250},
        {"title": "The Invisible Man", "author": "H.G. Wells",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A scientist discovers invisibility but loses his sanity. A cautionary tale about power and isolation.",
         "link": "https://gutenberg.org/ebooks/5230", "pages": 170},
        {"title": "From the Earth to the Moon", "author": "Jules Verne",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The Baltimore Gun Club plans to fire a projectile to the Moon. Remarkably prescient about space travel.",
         "link": "https://gutenberg.org/ebooks/83", "pages": 180},
        {"title": "The Island of Doctor Moreau", "author": "H.G. Wells",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A shipwrecked man finds an island where a doctor creates human-animal hybrids. Disturbing and thought-provoking.",
         "link": "https://gutenberg.org/ebooks/159", "pages": 160},
        {"title": "Flatland", "author": "Edwin A. Abbott",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A story set in a two-dimensional world that explores dimensions and perception. A mathematical classic disguised as fiction.",
         "link": "https://gutenberg.org/ebooks/201", "pages": 100},
        {"title": "The Lost World", "author": "Arthur Conan Doyle",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Professor Challenger leads an expedition to a plateau where dinosaurs still exist. The original Jurassic Park.",
         "link": "https://gutenberg.org/ebooks/139", "pages": 220},
        {"title": "We", "author": "Yevgeny Zamyatin",
         "platform": "Open Library", "format": "Borrow (digital)",
         "desc": "The precursor to 1984 and Brave New World. Life in a totalitarian society where individuality is outlawed.",
         "link": "https://openlibrary.org/works/OL27493W/We", "pages": 230},
        {"title": "The Mysterious Island", "author": "Jules Verne",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Castaways use ingenuity and science to survive on an uncharted island. Part Robinson Crusoe, part engineering manual.",
         "link": "https://gutenberg.org/ebooks/1268", "pages": 600},
    ],
    "mystery": [
        {"title": "The Hound of the Baskervilles", "author": "Arthur Conan Doyle",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Holmes investigates a spectral hound haunting the Baskerville family. The greatest Sherlock Holmes novel.",
         "link": "https://gutenberg.org/ebooks/2852", "pages": 260},
        {"title": "The Mystery of Edwin Drood", "author": "Charles Dickens",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Dickens' unfinished final novel. The mystery of who killed Edwin Drood has never been solved \u2014 readers get to speculate!",
         "link": "https://gutenberg.org/ebooks/564", "pages": 350},
        {"title": "The Thirty-Nine Steps", "author": "John Buchan",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A man is wrongly accused of murder and must uncover a spy ring. The blueprint for the modern thriller.",
         "link": "https://gutenberg.org/ebooks/558", "pages": 160},
        {"title": "The Secret Adversary", "author": "Agatha Christie",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Tommy and Tuppence launch a detective agency and stumble into a conspiracy. Christie at her most playful.",
         "link": "https://gutenberg.org/ebooks/1155", "pages": 300},
        {"title": "The Moonstone", "author": "Wilkie Collins",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Widely considered the first English detective novel. A stolen diamond, a country house, and multiple unreliable narrators.",
         "link": "https://gutenberg.org/ebooks/1555", "pages": 450},
        {"title": "A Study in Scarlet", "author": "Arthur Conan Doyle",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The first Sherlock Holmes story. Holmes and Watson meet and solve a murder rooted in Mormon Utah.",
         "link": "https://gutenberg.org/ebooks/244", "pages": 170},
        {"title": "The Lady of the Shroud", "author": "Bram Stoker",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Stoker's non-vampire mystery about a veiled woman on a haunted ship. Atmospheric and suspenseful.",
         "link": "https://gutenberg.org/ebooks/3106", "pages": 380},
        {"title": "The Big Sleep", "author": "Raymond Chandler",
         "platform": "Open Library", "format": "Borrow (digital)",
         "desc": "Philip Marlowe navigates a web of blackmail and murder in 1930s Los Angeles. Hard-boiled noir at its finest.",
         "link": "https://openlibrary.org/works/OL27440W/The_Big_Sleep", "pages": 230},
        {"title": "The Circular Staircase", "author": "Mary Roberts Rinehart",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A spinster rents a country house and encounters mysterious happenings. A pioneering female-authored mystery.",
         "link": "https://gutenberg.org/ebooks/1941", "pages": 280},
        {"title": "The Woman in White", "author": "Wilkie Collins",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A man encounters a mysterious woman in white on a moonlit road, setting off a chain of dark discoveries.",
         "link": "https://gutenberg.org/ebooks/583", "pages": 550},
        {"title": "The Phantom of the Opera", "author": "Gaston Leroux",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The iconic tale beneath the Paris Opera House. More mystery and suspense than the musical adaptation.",
         "link": "https://gutenberg.org/ebooks/175", "pages": 300},
        {"title": "Murder in the Cathedral", "author": "T.S. Eliot",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A poetic drama about the murder of Thomas Becket. A mystery of faith, power, and martyrdom.",
         "link": "https://gutenberg.org/ebooks/28568", "pages": 80},
    ],
    "history": [
        {"title": "The Art of War", "author": "Sun Tzu",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Ancient Chinese military treatise that remains relevant for business, sports, and life strategy.",
         "link": "https://gutenberg.org/ebooks/132", "pages": 80},
        {"title": "The Decline and Fall of the Roman Empire (abridged)", "author": "Edward Gibbon",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The monumental history of Rome's collapse. Start with Volume 1 for the rise through the fall.",
         "link": "https://gutenberg.org/ebooks/25717", "pages": 1200},
        {"title": "The Autobiography of Benjamin Franklin", "author": "Benjamin Franklin",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Franklin's own story \u2014 printer, inventor, diplomat, founding father. Practical wisdom and American spirit.",
         "link": "https://gutenberg.org/ebooks/20203", "pages": 200},
        {"title": "Narrative of the Life of Frederick Douglass", "author": "Frederick Douglass",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The powerful first-hand account of an enslaved man's journey to freedom. Essential American history.",
         "link": "https://gutenberg.org/ebooks/23", "pages": 120},
        {"title": "The Souls of Black Folk", "author": "W.E.B. Du Bois",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Foundational work of sociology and civil rights. Du Bois introduces the concept of 'double consciousness.'",
         "link": "https://gutenberg.org/ebooks/408", "pages": 200},
        {"title": "On the Origin of Species", "author": "Charles Darwin",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The book that changed how humanity understands life. Surprisingly readable and compellingly argued.",
         "link": "https://gutenberg.org/ebooks/2009", "pages": 460},
        {"title": "A Short History of the World", "author": "H.G. Wells",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A concise overview of human history from prehistory to WWI. Perfect entry point for world history.",
         "link": "https://gutenberg.org/ebooks/11278", "pages": 260},
        {"title": "The Communist Manifesto", "author": "Karl Marx & Friedrich Engels",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "One of the most influential political documents in history. Essential for understanding modern politics.",
         "link": "https://gutenberg.org/ebooks/61", "pages": 60},
        {"title": "The Prince", "author": "Niccolò Machiavelli",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The classic treatise on political power and leadership. Still studied by politicians and CEOs worldwide.",
         "link": "https://gutenberg.org/ebooks/1232", "pages": 120},
        {"title": "The Interesting Narrative of Olaudah Equiano", "author": "Olaudah Equiano",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "An enslaved African's journey across the Atlantic and his fight for freedom. A powerful eyewitness account.",
         "link": "https://gutenberg.org/ebooks/49308", "pages": 300},
        {"title": "Meditations", "author": "Marcus Aurelius",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The Roman emperor's personal journal of Stoic philosophy. Timeless wisdom on resilience and virtue.",
         "link": "https://gutenberg.org/ebooks/2680", "pages": 140},
        {"title": "The Anglo-Saxon Chronicle", "author": "Various (trans. James Ingram)",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A year-by-year account of English history from the earliest times to 1154. Fascinating primary source.",
         "link": "https://gutenberg.org/ebooks/657", "pages": 350},
    ],
    "fantasy": [
        {"title": "The Wonderful Wizard of Oz", "author": "L. Frank Baum",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Dorothy's journey through Oz is darker and more imaginative than the movie. A timeless American fairy tale.",
         "link": "https://gutenberg.org/ebooks/55", "pages": 180},
        {"title": "Alice's Adventures in Wonderland", "author": "Lewis Carroll",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Alice falls down the rabbit hole into a world of nonsense and wonder. Lewis Carroll's masterpiece of imagination.",
         "link": "https://gutenberg.org/ebooks/11", "pages": 160},
        {"title": "Through the Looking-Glass", "author": "Lewis Carroll",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Alice steps through the mirror into a chessboard world. Jabberwocky, Tweedledee, and the Red Queen await.",
         "link": "https://gutenberg.org/ebooks/12", "pages": 170},
        {"title": "The Princess and the Goblin", "author": "George MacDonald",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A princess discovers goblins living beneath her castle. A foundational fantasy that influenced Tolkien and Lewis.",
         "link": "https://gutenberg.org/ebooks/709", "pages": 200},
        {"title": "A Journey to the Interior of the Earth", "author": "Jules Verne",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Prehistoric creatures, underground seas, and subterranean wonders in Verne's most fantastical adventure.",
         "link": "https://gutenberg.org/ebooks/18857", "pages": 250},
        {"title": "The Legends of King Arthur and His Knights", "author": "James Knowles",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The definitive retelling of Arthurian legend \u2014 Excalibur, Guinevere, Lancelot, and the Round Table.",
         "link": "https://gutenberg.org/ebooks/32437", "pages": 350},
        {"title": "Phantastes", "author": "George MacDonald",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A young man enters a fairy world where books come alive and shadows have minds. Surreal and haunting.",
         "link": "https://gutenberg.org/ebooks/788", "pages": 220},
        {"title": "The Water-Babies", "author": "Charles Kingsley",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A chimney sweep transforms into a water-baby and embarks on moral adventures underwater. Victorian fantasy.",
         "link": "https://gutenberg.org/ebooks/1077", "pages": 260},
        {"title": "Peter Pan", "author": "J.M. Barrie",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The boy who wouldn't grow up takes Wendy to Neverland. Much darker and richer than you remember.",
         "link": "https://gutenberg.org/ebooks/16", "pages": 200},
        {"title": "The Wood Beyond the World", "author": "William Morris",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A proto-fantasy novel about a man who discovers a magical land beyond an enchanted forest. Influenced Tolkien.",
         "link": "https://gutenberg.org/ebooks/34723", "pages": 200},
        {"title": "The Book of Wonder", "author": "Lord Dunsany",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Imaginative fantasy tales of gods, heroes, and magical worlds. Dunsany invented an entire mythos.",
         "link": "https://gutenberg.org/ebooks/7156", "pages": 140},
        {"title": "Fifty-One Tales", "author": "Lord Dunsany",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Brief, beautiful fantasy micro-stories. Perfect for quick reading with enormous imaginative scope.",
         "link": "https://gutenberg.org/ebooks/7527", "pages": 90},
    ],
    "philosophy": [
        {"title": "The Republic", "author": "Plato",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Plato's dialogue on justice, the ideal state, and the philosopher-king. The Allegory of the Cave is here.",
         "link": "https://gutenberg.org/ebooks/1497", "pages": 380},
        {"title": "Meditations", "author": "Marcus Aurelius",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Personal reflections from a Roman emperor on Stoic philosophy. Practical wisdom for modern life.",
         "link": "https://gutenberg.org/ebooks/2680", "pages": 140},
        {"title": "Beyond Good and Evil", "author": "Friedrich Nietzsche",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Nietzsche challenges conventional morality and questions the foundations of Western philosophy. Provocative.",
         "link": "https://gutenberg.org/ebooks/5217", "pages": 240},
        {"title": "Civil Disobedience", "author": "Henry David Thoreau",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Thoreau's essay on individual conscience versus unjust laws. Influenced Gandhi and Martin Luther King Jr.",
         "link": "https://gutenberg.org/ebooks/71", "pages": 30},
        {"title": "Walden", "author": "Henry David Thoreau",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Two years living simply at Walden Pond. A meditation on nature, simplicity, and deliberate living.",
         "link": "https://gutenberg.org/ebooks/205", "pages": 300},
        {"title": "The Critique of Pure Reason", "author": "Immanuel Kant",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Kant's revolutionary work on human knowledge and experience. Challenging but transformative for patient readers.",
         "link": "https://gutenberg.org/ebooks/4280", "pages": 600},
        {"title": "Thus Spoke Zarathustra", "author": "Friedrich Nietzsche",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A philosophical novel about the Übermensch and the eternal recurrence. Nietzsche's most literary work.",
         "link": "https://gutenberg.org/ebooks/5221", "pages": 300},
        {"title": "Self-Reliance", "author": "Ralph Waldo Emerson",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Emerson's essay on trusting your inner voice and nonconformity. The American individualist manifesto.",
         "link": "https://gutenberg.org/ebooks/16643", "pages": 40},
        {"title": "The Symposium", "author": "Plato",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A drinking party where guests deliver speeches on the nature of love. Aristophanes, Socrates, and more.",
         "link": "https://gutenberg.org/ebooks/1599", "pages": 120},
        {"title": "The Problems of Philosophy", "author": "Bertrand Russell",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Russell's accessible introduction to philosophical questions about knowledge, reality, and truth.",
         "link": "https://gutenberg.org/ebooks/48256", "pages": 130},
    ],
    "classic-literature": [
        {"title": "Pride and Prejudice", "author": "Jane Austen",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Elizabeth Bennet and Mr. Darcy navigate manners, misunderstanding, and love in Regency England. Witty and wonderful.",
         "link": "https://gutenberg.org/ebooks/1342", "pages": 350},
        {"title": "Jane Eyre", "author": "Charlotte Brontë",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "An orphan girl grows up to become a governess and falls for the brooding Mr. Rochester. Gothic romance at its best.",
         "link": "https://gutenberg.org/ebooks/1260", "pages": 450},
        {"title": "Great Expectations", "author": "Charles Dickens",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Young Pip rises from poverty to gentleman status, only to discover what truly matters. Dickens at his most personal.",
         "link": "https://gutenberg.org/ebooks/1400", "pages": 400},
        {"title": "Wuthering Heights", "author": "Emily Brontë",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Heathcliff and Catherine's destructive passion on the Yorkshire moors. Wild, dark, and unforgettable.",
         "link": "https://gutenberg.org/ebooks/768", "pages": 350},
        {"title": "Moby-Dick", "author": "Herman Melville",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Captain Ahab's obsessive hunt for the great white whale. An epic of obsession, nature, and the American spirit.",
         "link": "https://gutenberg.org/ebooks/2701", "pages": 600},
        {"title": "Anna Karenina", "author": "Leo Tolstoy",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Tolstoy's masterpiece of love, betrayal, and Russian society. 'Happy families are all alike.'",
         "link": "https://gutenberg.org/ebooks/1399", "pages": 800},
        {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Murder, faith, family, and philosophy intertwined in Dostoevsky's final and greatest novel.",
         "link": "https://gutenberg.org/ebooks/21818", "pages": 800},
        {"title": "Middlemarch", "author": "George Eliot",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Described by Virginia Woolf as 'one of the few English novels written for grown-up people.' A masterwork.",
         "link": "https://gutenberg.org/ebooks/145", "pages": 900},
        {"title": "Les Misérables", "author": "Victor Hugo",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Jean Valjean's journey from convict to saint through revolutionary France. One of the greatest stories ever told.",
         "link": "https://gutenberg.org/ebooks/135", "pages": 1200},
        {"title": "Adventures of Huckleberry Finn", "author": "Mark Twain",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Huck and Jim float down the Mississippi. Twain's satirical masterpiece on race and freedom in America.",
         "link": "https://gutenberg.org/ebooks/76", "pages": 350},
        {"title": "The Age of Innocence", "author": "Edith Wharton",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A love triangle in Gilded Age New York. Wharton dissects society with surgical precision and deep empathy.",
         "link": "https://gutenberg.org/ebooks/541", "pages": 340},
        {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A beautiful man remains young while his portrait ages and shows his sins. Wilde's only novel is a masterpiece.",
         "link": "https://gutenberg.org/ebooks/174", "pages": 250},
    ],
    "horror": [
        {"title": "Dracula", "author": "Bram Stoker",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "The original vampire novel. Jonathan Harker's visit to Count Dracula's castle begins a Gothic horror odyssey.",
         "link": "https://gutenberg.org/ebooks/345", "pages": 400},
        {"title": "Frankenstein", "author": "Mary Shelley",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A scientist creates life and is destroyed by his creation. Horror, philosophy, and tragedy in one.",
         "link": "https://gutenberg.org/ebooks/84", "pages": 280},
        {"title": "The Strange Case of Dr. Jekyll and Mr. Hyde", "author": "Robert Louis Stevenson",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A respectable doctor transforms into a murderous alter ego. The definitive duality-of-man story.",
         "link": "https://gutenberg.org/ebooks/43", "pages": 120},
        {"title": "The Turn of the Screw", "author": "Henry James",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A governess sees ghostly figures at a country estate. Are they real, or is she losing her mind?",
         "link": "https://gutenberg.org/ebooks/209", "pages": 170},
        {"title": "The Haunted House", "author": "Charles Dickens",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Dickens' collaborative ghost story from 'All the Year Round.' Spooky and entertaining Victorian hauntings.",
         "link": "https://gutenberg.org/ebooks/23842", "pages": 100},
        {"title": "The Willows", "author": "Algernon Blackwood",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Two men camp on an island and encounter malevolent supernatural forces. H.P. Lovecraft called it the finest horror tale.",
         "link": "https://gutenberg.org/ebooks/10832", "pages": 50},
        {"title": "Carmilla", "author": "Sheridan Le Fanu",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A female vampire preys on a young woman in a remote castle. predates Dracula by 26 years. Lesbian Gothic horror.",
         "link": "https://gutenberg.org/ebooks/10042", "pages": 120},
        {"title": "The House of the Seven Gables", "author": "Nathaniel Hawthorne",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A cursed family inhabits a decaying mansion. Hawthorne's Gothic romance of sin and redemption.",
         "link": "https://gutenberg.org/ebooks/77", "pages": 350},
        {"title": "The Machine Stops", "author": "E.M. Forster",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Humanity lives underground, communicating through machines. When the machine stops... prescient technological horror.",
         "link": "https://gutenberg.org/ebooks/19784", "pages": 40},
        {"title": "The Yellow Wallpaper", "author": "Charlotte Perkins Gilman",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A woman confined to her room slowly descends into madness. A searing critique of the 'rest cure' and female oppression.",
         "link": "https://gutenberg.org/ebooks/1952", "pages": 20},
    ],
    "adventure": [
        {"title": "Treasure Island", "author": "Robert Louis Stevenson",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Young Jim Hawkins finds a pirate's treasure map and sails for Treasure Island. Long John Silver is unforgettable.",
         "link": "https://gutenberg.org/ebooks/120", "pages": 250},
        {"title": "The Count of Monte Cristo", "author": "Alexandre Dumas",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Wrongfully imprisoned, Edmond Dantès escapes and transforms into the Count for an elaborate revenge. Epic!",
         "link": "https://gutenberg.org/ebooks/1184", "pages": 1200},
        {"title": "Robinson Crusoe", "author": "Daniel Defoe",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Shipwrecked on a desert island for 28 years. The original survival story. Practical, spiritual, and gripping.",
         "link": "https://gutenberg.org/ebooks/521", "pages": 350},
        {"title": "The Three Musketeers", "author": "Alexandre Dumas",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "D'Artagnan joins Athos, Porthos, and Aramis for swashbuckling adventure. 'All for one, one for all!'",
         "link": "https://gutenberg.org/ebooks/1257", "pages": 500},
        {"title": "Around the World in Eighty Days", "author": "Jules Verne",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Phileas Fogg bets he can circumnavigate the globe in 80 days. A globetrotting adventure full of obstacles.",
         "link": "https://gutenberg.org/ebooks/103", "pages": 220},
        {"title": "Kidnapped", "author": "Robert Louis Stevenson",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A young man is kidnapped and sent to the American colonies but escapes through the Scottish Highlands.",
         "link": "https://gutenberg.org/ebooks/460", "pages": 280},
        {"title": "The Prisoner of Zenda", "author": "Anthony Hope",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "An Englishman is roped into impersonating a king in the fictional country of Ruritania. Ruritanian romance.",
         "link": "https://gutenberg.org/ebooks/1660", "pages": 200},
        {"title": "Captain Blood", "author": "Rafael Sabatini",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "A doctor wrongfully convicted of treason becomes a legendary pirate. Swashbuckling at its finest.",
         "link": "https://gutenberg.org/ebooks/1563", "pages": 350},
        {"title": "The Last of the Mohicans", "author": "James Fenimore Cooper",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Hawkeye and his Mohican friends during the French and Indian War. America's first adventure novel.",
         "link": "https://gutenberg.org/ebooks/933", "pages": 400},
        {"title": "King Solomon's Mines", "author": "H. Rider Haggard",
         "platform": "Project Gutenberg", "format": "EPUB/Kindle/HTML",
         "desc": "Allan Quatermain leads an expedition to find a lost diamond mine in uncharted Africa. The first lost-world adventure.",
         "link": "https://gutenberg.org/ebooks/1265", "pages": 300},
    ],
}

# ---------------------------------------------------------------------------
# Free podcast database by genre
# Each entry: name, platform, description, episode_type, link
# ---------------------------------------------------------------------------
PODCASTS = {
    "true-crime": [
        {"name": "True Crime Brewery", "platform": "Spotify", "desc": "True crime discussed over a beer selection. Knowledgeable hosts, great storytelling.", "link": "https://open.spotify.com/show/0whEE60FdkH8hNw5UZlIFH", "type": "Episode (~45 min)"},
        {"name": "Casefile True Crime", "platform": "Spotify / YouTube", "desc": "Fact-based, unbiased narrative of real crimes. The anonymous host's delivery is hypnotic.", "link": "https://open.spotify.com/show/2CUsmCbVRPJ6dMqosVSI39", "type": "Episode (~50 min)"},
        {"name": "Criminal", "platform": "Spotify / Apple", "desc": "Stories about people who've done wrong, been wronged, or been caught somewhere in the middle.", "link": "https://open.spotify.com/show/2pD2kxhaZuKMwRvYjUxvQL", "type": "Episode (~30 min)"},
        {"name": "Small Town Murder", "platform": "Spotify / YouTube", "desc": "True crime + comedy. Two comedians break down small-town murder cases with genuine interest.", "link": "https://open.spotify.com/show/7aJ5aE1EeCUkiVX0tL9ZVV", "type": "Episode (~90 min)"},
        {"name": "The Trail Went Cold", "platform": "Spotify", "desc": "Deep dives into unsolved cases and missing persons investigations.", "link": "https://open.spotify.com/show/4rLb5Bc7sRm0G5I7KPhYX7", "type": "Deep Dive (~60 min)"},
        {"name": "RedHanded", "platform": "Spotify / Apple", "desc": "Two British women discuss true crime and paranormal stories with wit and empathy.", "link": "https://open.spotify.com/show/6gWmJ1sPYpJKGhoPewNI8B", "type": "Episode (~60 min)"},
    ],
    "science": [
        {"name": "Science Vs", "platform": "Spotify / YouTube", "desc": "Pitting facts against popular myths. Fun, well-researched, and accessible science.", "link": "https://open.spotify.com/show/6sJCMKQgwBiBWj0z9TTNbf", "type": "Episode (~35 min)"},
        {"name": "Ologies with Alie Ward", "platform": "Spotify / Apple", "desc": "Alie Ward interviews experts about every '-ology' you can imagine. Enthusiastic and charming.", "link": "https://open.spotify.com/show/1a2zvFlWki1TYbUJcWGFjk", "type": "Episode (~60 min)"},
        {"name": "The Infinite Monkey Cage", "platform": "Spotify / BBC", "desc": "Brian Cox and Robin Ince with comedians and scientists. Funny, smart, British science chat.", "link": "https://open.spotify.com/show/6yn5iXSaerlAOn2kWQCJcA", "type": "Episode (~30 min)"},
        {"name": "StarTalk Radio", "platform": "Spotify / YouTube", "desc": "Neil deGrasse Tyson explores the universe with comedians and co-hosts. Space and science made fun.", "link": "https://open.spotify.com/show/4J81X2HPpFE0I13VxzNz8a", "type": "Episode (~50 min)"},
        {"name": "Radiolab", "platform": "Spotify / Apple", "desc": "Deeply produced explorations of scientific and philosophical questions. Audio storytelling at its best.", "link": "https://open.spotify.com/show/35kXbOvnqpMZNLmfjnXS5A", "type": "Episode (~50 min)"},
        {"name": "Stuff You Should Know", "platform": "Spotify / Apple", "desc": "Josh and Chuck explain how everything works. The Swiss Army knife of educational podcasts.", "link": "https://open.spotify.com/show/3WgIh6uRE2lr2l6eZWCGmV", "type": "Episode (~40 min)"},
    ],
    "comedy": [
        {"name": "Comedy Bang Bang", "platform": "Spotify / Apple", "desc": "Scott Aukerman interviews comedians and characters. Improv, nonsense, and recurring bits.", "link": "https://open.spotify.com/show/5uCXlYzoJxgnLmCBHcLMdA", "type": "Episode (~60 min)"},
        {"name": "My Brother, My Brother and Me", "platform": "Spotify / YouTube", "desc": "Three brothers give advice to Yahoo Answers questions. Absurd and hilarious.", "link": "https://open.spotify.com/show/2kijZSBUlE1f7dK2VRbdex", "type": "Episode (~60 min)"},
        {"name": "Conan O'Brien Needs a Friend", "platform": "Spotify / YouTube", "desc": "Conan interviews celebrities with genuine warmth and zero pretension. Bonus: assistant Sona is a star.", "link": "https://open.spotify.com/show/6i1WfJjPUnwGHCnsnDxPZS", "type": "Episode (~60 min)"},
        {"name": "Off Menu with Ed Gamble and James Acaster", "platform": "Spotify / Apple", "desc": "Guests choose their dream menu courses. Sounds simple, but it's consistently hilarious.", "link": "https://open.spotify.com/show/6tPoNlrTjaEYgG1DZGzXZI", "type": "Episode (~60 min)"},
        {"name": "How Did This Get Made?", "platform": "Spotify / YouTube", "desc": "Paul Scheer, June Diane Raphael, and Jason Mantzoukas break down terrible movies. Pure joy.", "link": "https://open.spotify.com/show/6FtcYgdGVnO9Fy3zX4Zlhf", "type": "Episode (~90 min)"},
        {"name": "The Doghouse", "platform": "Spotify / Apple", "desc": "James Acaster and Ed Gamble discuss things that belong in 'the doghouse.' Inventive comedy format.", "link": "https://open.spotify.com/show/0jqM6KMKZRF2C6jmokdJ2V", "type": "Episode (~45 min)"},
    ],
    "news": [
        {"name": "The Daily", "platform": "Spotify / Apple", "desc": "The New York Times' flagship news podcast. One story per episode, deeply reported.", "link": "https://open.spotify.com/show/2Xs4gBCrnGnRPAa7U0ZNYk", "type": "Daily (~25 min)"},
        {"name": "Up First", "platform": "Spotify / Apple", "desc": "NPR's morning news briefing. Three essential stories in under 15 minutes.", "link": "https://open.spotify.com/show/3bBREkgGD0L5GNqItJIYD9", "type": "Daily (~12 min)"},
        {"name": "BBC Global News", "platform": "Spotify / Apple", "desc": "BBC's world news coverage. Reliable, international perspective on current events.", "link": "https://open.spotify.com/show/1Tz7sdAGQ4YM8bZUqU0Vka", "type": "Daily (~30 min)"},
        {"name": "Planet Money", "platform": "Spotify / Apple", "desc": "NPR makes economics entertaining. Understanding the economy through stories, not jargon.", "link": "https://open.spotify.com/show/0R0D2Jt36DNBFNvjt4e1E7", "type": "Episode (~20 min)"},
        {"name": "Recode Decode", "platform": "Spotify / YouTube", "desc": "Kara Swisher interviews tech leaders. Insightful, sometimes confrontational, always informed.", "link": "https://open.spotify.com/show/7mDeP3HRKtib1SdzvIgu0u", "type": "Interview (~45 min)"},
        {"name": "Today, Explained", "platform": "Spotify / Apple", "desc": "Vox explains one big news topic per episode. Clear, concise, and well-produced.", "link": "https://open.spotify.com/show/5sSM3SPmX2k21VLjDOus4v", "type": "Daily (~20 min)"},
    ],
    "history": [
        {"name": "Hardcore History", "platform": "Spotify / YouTube", "desc": "Dan Carlin's epic deep dives into history. Multi-hour episodes that are worth every minute.", "link": "https://open.spotify.com/show/7m2cB1pGbOYP6LFuQ2dRZx", "type": "Deep Dive (2-6 hours)"},
        {"name": "You're Dead To Me", "platform": "Spotify / BBC", "desc": "Greg Jenner with a comedian and historian. Funny and educational history on diverse topics.", "link": "https://open.spotify.com/show/4ILfja04mHGSMlE0dXvIFi", "type": "Episode (~50 min)"},
        {"name": "The Rest is History", "platform": "Spotify / Apple", "desc": "Tom Holland and Dominic Sandbrook discuss historical questions with humor and depth.", "link": "https://open.spotify.com/show/4uXph6D2yYn4XhOWw10jPw", "type": "Episode (~45 min)"},
        {"name": "Revolutions", "platform": "Spotify / Apple", "desc": "Mike Duncan's season-by-season history of revolutions. From the English Civil War to the Arab Spring.", "link": "https://open.spotify.com/show/5GDLnLZiqjo6R7cPTGw4kT", "type": "Episode (~45 min)"},
        {"name": "Behind the Bastards", "platform": "Spotify / YouTube", "desc": "Robert Evans tells the stories of terrible people throughout history. Darkly funny and deeply researched.", "link": "https://open.spotify.com/show/4sYHXX9tJm2sPsbZOJMTtJ", "type": "Episode (~60 min)"},
        {"name": "The History of Rome", "platform": "Spotify / Apple", "desc": "Mike Duncan's complete history of Rome from founding to fall. The definitive podcast on the subject.", "link": "https://open.spotify.com/show/6AyCLBPVWPmTiXnoM2kpJh", "type": "Episode (~25 min)"},
    ],
    "self-improvement": [
        {"name": "The Huberman Lab", "platform": "Spotify / YouTube", "desc": "Dr. Andrew Huberman breaks down neuroscience for practical life optimization.", "link": "https://open.spotify.com/show/5oRBpU2i3zPFngLcxYiB4M", "type": "Episode (~90 min)"},
        {"name": "The Tim Ferriss Show", "platform": "Spotify / YouTube", "desc": "Tim interviews world-class performers to extract their habits, routines, and strategies.", "link": "https://open.spotify.com/show/0noi8aPUtBSLgBUUFkiNGd", "type": "Interview (~60 min)"},
        {"name": "10% Happier", "platform": "Spotify / Apple", "desc": "Dan Harris brings meditation to skeptics. Practical mindfulness without the woo-woo.", "link": "https://open.spotify.com/show/0nvBFvq5qHUG3BY0NfVnS0", "type": "Episode (~30 min)"},
        {"name": "How I Built This", "platform": "Spotify / Apple", "desc": "Guy Raz interviews founders of major companies. Startup stories and entrepreneurial wisdom.", "link": "https://open.spotify.com/show/5gT2kNGuCtXBUf3MGVMHQo", "type": "Interview (~50 min)"},
        {"name": "The Minimalists", "platform": "Spotify / YouTube", "desc": "Joshua Fields Millburn and Ryan Nicodemus discuss simple living and letting go.", "link": "https://open.spotify.com/show/6WvOb6pCXmIK5mxU00Fbu0", "type": "Episode (~50 min)"},
        {"name": "Note to Self", "platform": "Spotify / Apple", "desc": "Manoush Zomorodi explores technology's impact on our behavior and how to use it better.", "link": "https://open.spotify.com/show/5hflzOLIAFRaLkKsWPNWm4", "type": "Episode (~25 min)"},
    ],
}

# ---------------------------------------------------------------------------
# Genre aliases for flexible matching
# ---------------------------------------------------------------------------
GENRE_ALIASES = {
    "scifi": "science-fiction", "sci-fi": "science-fiction", "science fiction": "science-fiction",
    "sf": "science-fiction", "speculative": "science-fiction",
    "mystery": "mystery", "thriller": "mystery", "crime": "mystery", "detective": "mystery",
    "noir": "mystery",
    "history": "history", "historical": "history", "nonfiction": "history",
    "fantasy": "fantasy", "mythology": "fantasy", "fairy-tale": "fantasy",
    "philosophy": "philosophy", "philosophical": "philosophy", "thinkers": "philosophy",
    "classic": "classic-literature", "classics": "classic-literature", "literature": "classic-literature",
    "fiction": "classic-literature", "novels": "classic-literature", "novel": "classic-literature",
    "horror": "horror", "gothic": "horror", "spooky": "horror", "ghost": "horror",
    "adventure": "adventure", "action": "adventure", "survival": "adventure",
    "true-crime": "true-crime", "true crime": "true-crime", "crime-stories": "true-crime",
    "science": "science", "tech": "science", "stem": "science",
    "comedy": "comedy", "funny": "comedy", "humor": "comedy", "humour": "comedy",
    "news": "news", "current-events": "news", "politics": "news",
    "self-help": "self-improvement", "self-improvement": "self-improvement",
    "selfhelp": "self-improvement", "productivity": "self-improvement",
}


def normalize_genre(raw):
    """Normalize a genre string using aliases."""
    return GENRE_ALIASES.get(raw.lower().strip(), raw.lower().strip())


def generate_plan(genres):
    """Generate the reading list and podcast guide as markdown."""
    now = datetime.now().strftime("%B %d, %Y")
    lines = []

    lines.append(f"# \U0001f4da Books & Podcasts Discovery Guide")
    lines.append(f"*Free reading and listening recommendations \u2014 generated {now}*\n")

    # Normalize genres
    normalized_books = set()
    normalized_pods = set()
    for g in genres:
        key = normalize_genre(g)
        if key in BOOKS:
            normalized_books.add(key)
        if key in PODCASTS:
            normalized_pods.add(key)

    # If no matches, default to a few popular genres
    if not normalized_books:
        normalized_books = {"classic-literature", "science-fiction", "philosophy"}
    if not normalized_pods:
        normalized_pods = {"true-crime", "science", "comedy"}

    # --- Book Section ---
    lines.append("## \U0001f4f0 Free Book Sources\n")
    lines.append("| Platform | URL | What's Available |")
    lines.append("|----------|-----|------------------|")
    lines.append("| [Project Gutenberg]({}) | gutenberg.org | 70,000+ public domain ebooks |".format("https://gutenberg.org"))
    lines.append("| [Open Library]({}) | openlibrary.org | 4M+ borrowable ebooks |".format("https://openlibrary.org"))
    lines.append("| [Librivox]({}) | librivox.org | 16,000+ free audiobooks |".format("https://librivox.org"))
    lines.append("| [Smashwords Free]({}) | smashwords.com | Free indie ebooks |".format("https://smashwords.com"))
    lines.append("| [Standard Ebooks]({}) | standardebooks.org | Beautifully typeset classics |".format("https://standardebooks.org"))
    lines.append("")

    # --- Books by Genre ---
    lines.append("## \U0001f4d6 Book Recommendations\n")

    book_count = 0
    for genre in sorted(normalized_books):
        if genre not in BOOKS:
            continue
        books = BOOKS[genre][:10]
        book_count += len(books)
        genre_label = genre.replace("-", " ").title()
        lines.append(f"### {genre_label}\n")
        lines.append("| # | Title | Author | Platform | Pages | Format |")
        lines.append("|---|-------|--------|----------|-------|--------|")
        for i, b in enumerate(books, 1):
            lines.append(
                f"| {i} | [{b['title']}]({b['link']}) | {b['author']} | "
                f"{b['platform']} | ~{b['pages']} | {b['format']} |"
            )
        lines.append("")

        # Add descriptions as a separate table
        lines.append(f"**Why read these?**\n")
        for b in books:
            lines.append(f"- **{b['title']}:** {b['desc']}")
        lines.append("")

    # --- Podcast Section ---
    lines.append("---\n")
    lines.append("## \U0001f399\ufe0f Free Podcast Sources\n")
    lines.append("| Platform | URL | Notes |")
    lines.append("|----------|-----|-------|")
    lines.append("| [Spotify Podcasts]({}) | open.spotify.com/podcasts | Largest library, offline playback |".format("https://open.spotify.com"))
    lines.append("| [Apple Podcasts]({}) | podcasts.apple.com | Every podcast, web player available |".format("https://podcasts.apple.com"))
    lines.append("| [YouTube Podcasts]({}) | youtube.com/podcasts | Video podcasts, many free |".format("https://youtube.com"))
    lines.append("| [Pocket Casts Web]({}) | pocketcasts.com | Great player, free web access |".format("https://pocketcasts.com"))
    lines.append("| [iHeartRadio]({}) | iheart.com/podcasts | Free originals + directory |".format("https://iheart.com"))
    lines.append("")

    # --- Podcasts by Genre ---
    lines.append("## \U0001f399\ufe0f Podcast Recommendations\n")

    pod_count = 0
    for genre in sorted(normalized_pods):
        if genre not in PODCASTS:
            continue
        pods = PODCASTS[genre][:10]
        pod_count += len(pods)
        genre_label = genre.replace("-", " ").title()
        lines.append(f"### {genre_label}\n")
        lines.append("| # | Podcast | Platform | Episode Type | Link |")
        lines.append("|---|---------|----------|-------------|------|")
        for i, p in enumerate(pods, 1):
            lines.append(
                f"| {i} | **{p['name']}** | {p['platform']} | {p['type']} | [Listen]({p['link']}) |"
            )
        lines.append("")

        lines.append(f"**Why listen?**\n")
        for p in pods:
            lines.append(f"- **{p['name']}:** {p['desc']}")
        lines.append("")

    # --- Weekly Schedule ---
    lines.append("---\n")
    lines.append("## \U0001f4c5 Weekly Reading & Listening Schedule\n")
    lines.append("| Day | Activity | Suggested Content | Time |")
    lines.append("|-----|----------|------------------|------|")
    lines.append("| \u2600\ufe0f Monday | Morning podcast | A news or science podcast while commuting | 25 min |")
    lines.append("| \U0001f4da Monday | Evening reading | 2 chapters of a classic novel | 40 min |")
    lines.append("| \U0001f399\ufe0f Tuesday | Workout podcast | Comedy or science during exercise | 30 min |")
    lines.append("| \U0001f4da Tuesday | Evening reading | 1 chapter + 1 short story | 35 min |")
    lines.append("| \U0001f399\ufe0f Wednesday | Lunch podcast | True crime or history episode | 45 min |")
    lines.append("| \U0001f4da Wednesday | Evening reading | Continue current novel | 30 min |")
    lines.append("| \U0001f399\ufe0f Thursday | Commute podcast | Self-improvement or interview show | 25 min |")
    lines.append("| \U0001f4da Thursday | Evening reading | Audiobook via Librivox (20 min) | 20 min |")
    lines.append("| \U0001f399\ufe0f Friday | Deep dive | Long-form podcast episode | 60 min |")
    lines.append("| \U0001f4da Friday | Weekend reading kickoff | Start a new short book | 45 min |")
    lines.append("| \U0001f4da Saturday | Deep reading session | 3-4 chapters in comfortable setting | 90 min |")
    lines.append("| \U0001f399\ufe0f Saturday | Discovery episode | Try a new podcast from a different genre | 40 min |")
    lines.append("| \U0001f4da Sunday | Finish the book | Push through to complete your current read | 60 min |")
    lines.append("| \U0001f399\ufe0f Sunday | Reflective listening | Self-improvement or philosophy podcast | 30 min |")
    lines.append("")

    lines.append(f"*\U0001f4da {book_count} books + {pod_count} podcasts curated for you \u2014 Generated {now}*\n")

    return "\n".join(lines)


def main():
    """Parse arguments and generate the reading list."""
    parser = argparse.ArgumentParser(
        description="Discover free books and podcasts with personalized recommendations.",
        epilog="Example: python book_podcast_finder.py --genres 'science-fiction,history,true-crime'",
    )
    parser.add_argument(
        "--genres",
        default="science-fiction,classic-literature,history,true-crime,science,comedy",
        help="Comma-separated genres for book and podcast recommendations (default: science-fiction,classic-literature,history,true-crime,science,comedy)",
    )
    parser.add_argument(
        "--output",
        default="reading_list.md",
        help="Output markdown file path (default: reading_list.md)",
    )

    args = parser.parse_args()

    genres = [g.strip() for g in args.genres.split(",") if g.strip()]

    try:
        content = generate_plan(genres=genres)

        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)

        abs_path = os.path.abspath(args.output)
        print(f"\n{'='*60}")
        print(f"  \U0001f4da Books & Podcasts Discovery Guide Generated!")
        print(f"{'='*60}")
        print(f"  \U0001f4c4 File:      {abs_path}")
        print(f"  \U0001f4d6 Genres:    {', '.join(genres)}")
        print(f"  \U0001f4f6 Sources:   Gutenberg, Open Library, Librivox, Smashwords")
        print(f"  \U0001f399\ufe0f Podcasts: Spotify, Apple Podcasts, YouTube")
        print(f"  \U0001f4c5 Schedule:  Weekly reading + listening plan included")
        print(f"{'='*60}\n")

    except PermissionError:
        print(f"Error: Permission denied writing to '{args.output}'.", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: Could not write file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
