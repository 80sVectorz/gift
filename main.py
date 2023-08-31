from iflib import noun,location,verb, game_loop, player,world,verb_parameter_type
from keywi import identifier

func_data = {}
object_library = {}

test_room = location("Concrete cell", 
"""
A small concrete prison cell. A metal shelf is attached to the wall. A reinforced steel door keeps you from leaving.
""",objects=[
	noun(identifier("metal shelf", "shelf"), """
A robust metal shelf it lacks any visual flare.			 
""", "a",location_specific=True),
	noun(identifier("reinforced steel door", "door"), """
A reinforced steel door. It looks to be of the horizontal sliding type. 
			 """, "a",location_specific=True)
	
])

object_library["apple"] = noun("apple", 
"""
A red apple that looks very appetizing.
""", "an",tags=["consumable"])

def verb_look(a,func_data,plr):
	if len(a) == 0:
		print("You look around the room.")
		return
	try:
		print(f"""
You take a look at the {a[0].identifier.name}.
{"-"*len(a[0].identifier.name)}
{a[0].identifier.name}
{a[0].description}
""")
	except:
		print("You have no idea what you are looking at.")
			
def verb_summon(a,func_data,plr):	
	if len(a) < 2:
		print("You fail to comprehend the meaning of nothing.")
		return
	for obj in a[1:]:
		if obj.lower() in func_data["verb_summon"]["synonym_map"].keys():
				object = func_data["verb_summon"]["summonable_objects"][ func_data["verb_summon"]["synonym_map"][obj.lower()]]
				print(f"You channel your magic to summon {object.indefinite_article} {object.name}")	
				object.clone(plr.location)
		else:
			print(f"You don't even know what {get_indefinite_article(obj)} {obj} is...")

func_data["verb_summon"] = {"synonym_map":{"apple":"apple"},"summonable_objects":{"apple":object_library["apple"]}}

def verb_eat(a,func_data,plr):
	if len(a) < 2:
		print("You fail to comprehend the meaning of nothing.")
		return
	target_obj= a[1].lower()
	for i,obj in enumerate(plr.location.objects):
		if obj.name.lower() == target_obj:
			if "consumable" in obj.tags:
				try:
					obj.tag_data["consumable"]["output"](a,func_data,plr,obj)
				except:
					print(f"You eat the {obj.name}.")
				plr.location.objects.pop(i)
				del obj
			else:
				print(f"You cannot eat {obj.indefinite_article} {obj.name}.")
			return
	print(f"There is no {target_obj} nearby.")
				
verbs_synonym_map = {}
verbs = {"look":verb(verb_look,["look","inspect"],verb_parameter_type.object),
				"summon":verb(verb_summon, ["spawn","summon","conjure","manifest"],verb_parameter_type.custom),
				 "eat":verb(verb_eat,["eat","consume"],verb_parameter_type.object)	
				}

test_world = world(
[test_room]
)

plr = player("Subject 4",test_room)

game = game_loop(verbs,world,plr,func_data)

game.run()