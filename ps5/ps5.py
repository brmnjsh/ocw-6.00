# 6.00 Problem Set 5
# RSS Feed Filter
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import feedparser
import string
import time
import re
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
	def __init__(self, guid, title, subject, summary, link):
		self.guid = guid
		self.title = title
		self.subject = subject
		self.summary = summary
		self.link = link

	def get_guid(self):
		return self.guid

	def get_title(self):
		return self.title

	def get_subject(self):
		return self.subject

	def get_summary(self):
		return self.summary

	def get_link(self):
		return self.link

# n = NewsStory('1','2','3','4','5')
# print n.get_link()
# raise SystemExit(0)
#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
	def __init__(self, word):
		self.word = word

	def is_word_in(self, text):
		for d in list(string.punctuation):
			text = text.replace(d, ' ')

		if (self.word in text.lower().split()):
			return True
		return False

# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
	def __init__(self, word):
		self.word = word.lower()
		WordTrigger.__init__(self, self.word)

	def evaluate(self, story):
		return WordTrigger.is_word_in(self, story.get_title())

# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
	def __init__(self, word):
		self.word = word.lower()
		WordTrigger.__init__(self, self.word)

	def evaluate(self, story):
		return WordTrigger.is_word_in(self, story.get_subject())

# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
	def __init__(self, word):
		self.word = word.lower()
		WordTrigger.__init__(self, self.word)

	def evaluate(self, story):
		return WordTrigger.is_word_in(self, story.get_summary())

# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
	def __init__(self, t):
		self.t = t

	def evaluate(self, story):
		return not self.t.evaluate(story)


# TODO: AndTrigger
class AndTrigger(Trigger):
	def __init__(self, t1, t2):
		self.t1 = t1
		self.t2 = t2

	def evaluate(self, story):
		return self.t1.evaluate(story) and self.t2.evaluate(story)

# TODO: OrTrigger
class OrTrigger(Trigger):
	def __init__(self, t1, t2):
		self.t1 = t1
		self.t2 = t2

	def evaluate(self, story):
		return self.t1.evaluate(story) or self.t2.evaluate(story)

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
	def __init__(self, phrase):
		self.phrase = phrase

	def evaluate(self, story):
		if (self.phrase in story.get_subject() or self.phrase in story.get_title() or self.phrase in story.get_summary()):
			return True
		return False

#======================
# Part 3
# Filtering
#======================
#76

def filter_stories(stories, triggers):
	"""
	Takes in a list of NewsStory-s.
	Returns only those stories for whom
	a trigger in triggerlist fires.
	"""
	storiesList = []
	for s in stories:
		for t in triggers:
			if t.evaluate(s) == True:
				storiesList.append(s)
				break
	return storiesList


#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    finalTriggers =  []
    triggers = {}
    for l in lines:
        l = l.split()
        if ('TITLE' in l):
            triggers[l[0]] = TitleTrigger(''.join(l[2:]))
        elif ('SUBJECT' in l):
            triggers[l[0]] = SubjectTrigger(''.join(l[2:]))
        elif ('PHRASE' in l):
            triggers[l[0]] = PhraseTrigger(''.join(l[2:]))
        elif ('AND' in l):
            triggers[l[0]] = AndTrigger(triggers[l[2]], triggers[l[3]])
        elif ('SUMMARY' in l):
            triggers[l[0]] = SummaryTrigger(''.join(l[2:]))
        elif ('NOT' in l):
            triggers[l[0]] = NotTrigger(triggers[l[2]], triggers[l[3]])
        elif ('OR' in l):
            triggers[l[0]] = AndTrigger(triggers[l[2]], triggers[l[3]])
        elif ('ADD' in l):
            for fl in l[1:]:
                finalTriggers.append(triggers[fl])
    return finalTriggers

import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Trump")
    t2 = SummaryTrigger("Olympics")
    t3 = PhraseTrigger("Vote")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]

    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []

    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)

        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)

        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()