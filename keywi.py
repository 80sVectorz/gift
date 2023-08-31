############################
# Keyword interpreter (keywi)
############################

from enum import Enum

class identifier:
	def __init__(self, name, essence, synonyms=[]):
		self.name = name
		self.essence = essence
		self.synonyms = synonyms
		if not self.essence in self.synonyms:
			self.synonyms.append(essence)

class keyword_type(Enum):
	junk = 1
	verb = 2
	object_reference = 3
	verb_modifier = 4
	reversed_verb_modifier = 5
	reversed_verb_modifier_split = 6
	filter = 8
	addition = 9
	verb_specific_junk = 10

junk = [
	"a","an",
	"the"
]

def clean(splitted,verb):
	global junk
	cleaned = []
	for word in splitted:
		if word in junk or word in verb.junk:
			continue
		cleaned.append(word)
	return cleaned