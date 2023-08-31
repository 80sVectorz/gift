########################################
# interactive fiction library (iflib)
########################################

import copy, keywi
from difflib import SequenceMatcher
from enum import Enum

VOWELS = set("aeiou")
CONSONANTS = set("bcdfghjklmnpqrstvwxyz")


def get_indefinite_article(word):
    """Get the indefinite article of a given noun."""

    if word[0].lower() in VOWELS:
        return "an"
    return "a"


class verb_parameter_type(Enum):
    object = 1
    custom = 2
	
class optional_verb_parameter_type(verb_parameter_type):
	pass

class location:
    def __init__(self, title, description, objects=[]):
        self.title = title
        self.description = description
        self.objects = objects


class direction:
    def __init__(self, destination, link, title=None, description=None):
        self.destination = destination
        if link == None or link == False:
            self.link = False
            self.title = title
            self.description = description
        else:
            self.link = link
            self.title = None
            self.description = None


class noun:
    def __init__(self,
                 identifier,
                 description,
                 indefinite_article,
                 location_specific=False,
                 tags=[],
                 tag_data={}):
        if isinstance(identifier, keywi.identifier):
            self.identifier = identifier
        elif isinstance(identifier, str):
            self.identifier = keywi.identifier(identifier, identifier)
        self.description = description
        self.indefinite_article = indefinite_article
        self.location = None
        self.location_specific = location_specific
        self.tags = tags
        self.tag_data = tag_data

    def clone(self, destination):
        cpy = copy.deepcopy(self)
        cpy.location = destination
        destination.objects.append(cpy)


class verb:
    def __init__(self, definition, synonyms, parameter_type, junk=[]):
        self.definition = definition
        self.synonyms = synonyms
        self.parameter_type = parameter_type
        self.junk = junk


class world:
    def __init__(self, map):
        self.map = map


class player:
    def __init__(self, name, start_location):
        self.name = name
        self.location = start_location


class language_module:
    def __init__(self, junk_words):
        self.junk_words = junk_words


class game_loop:
    def __init__(self, verbs, world, player, func_data):
        self.verbs = {"DEFINITIONS": verbs}
        self.map = world
        self.player = player
        self.func_data = func_data
        self.verbs["SYNONYMS"] = {}
        for key in self.verbs["DEFINITIONS"].keys():
            for synonym in self.verbs["DEFINITIONS"][key].synonyms:
                self.verbs["SYNONYMS"][synonym] = key

    def output_location(self):
        current_location = self.player.location
        objects = []
        objects_count = {}
        ignored_indexes = []
        i = 0
        for obj in current_location.objects:
            if obj.location_specific == False:
                if obj.identifier.name in objects_count.keys():
                    objects_count[obj.identifier.name] += 1
                    ignored_indexes.append(i)
                else:
                    objects_count[obj.identifier.name] = 1
            i += 1
        i = 0
        for obj in current_location.objects:
            if obj.location_specific == False:
                if not i in ignored_indexes:
                    objects.append(
                        f"{objects_count[obj.identifier.name]}x {obj.identifier.name}"
                    )
            i += 1

        object_list = '\n'.join(objects)
        if len(object_list) > 0:
            print(f"""
{"-"*len(current_location.title)}
{current_location.title}	
{current_location.description}

The objects in this location are:
{object_list}
""")
        else:
            print(f"""
{"-"*len(current_location.title)}
{current_location.title}	
{current_location.description}
""")

    def get_local_object(self, object_string):
        current_location = self.player.location

        for obj in current_location.objects:
            if (SequenceMatcher(obj.identifier.name.strip(" "),
                                object_string.lower().strip(" ")).ratio() > 0.8
                    or SequenceMatcher(
                        obj.identifier.essence.strip(" "),
                        object_string.lower().strip(" ")).ratio() > 0.8):
                return obj
        return None

    def parse_input(self, x):
        splitted = x.lower().split(" ")
        verb = None
        for i in range(len(splitted)):
            word = " ".join(splitted[:i + 1])
            if word in self.verbs["SYNONYMS"].keys():
                verb = self.verbs["DEFINITIONS"][self.verbs["SYNONYMS"][word]]
                splitted = splitted[i:]
            elif word == x:
                print("Could not understand input.")
                return
        if verb:
            splitted = keywi.clean(splitted, verb)
            if verb.parameter_type == verb_parameter_type.object:
                objs = []
                for i in range(len(splitted)):
                    for j in range(i, len(splitted)):
                        word = " ".join(splitted[i:j])
                        obj = self.get_local_object(word)
                        if obj:
                            objs.append(obj)
                if len(objs) > 0:
                    verb.definition(objs, self.func_data, self.player)
        else:
            print("Could not understand input.")

    def run(self):
        running = True
        while running:
            self.output_location()
            action = input("> ")
            self.parse_input(action)
