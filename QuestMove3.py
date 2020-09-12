import random as r
import QuestAssets1 as qa1
import QuestMonsters1 as qm1
import QuestEquip1 as qe1 


class Graphics():
	
	msg_decorator1 = "<<<<"
	msg_decorator2 = ""


class World():
	
	player_1 = None
	player_coordinates = {'x':0,'y':0}
	master_room_list = []
	global_torchlight = False
	current_world_level = 1
	potential_exits = 1
	potential_exits_threshhold = 4
	room_lock_numbers = [1,1,2,2,3,3,4,4,5,5]
	key_lock_numbers = [1,1,2,2,3,3,4,4,5,5]
	key_colors = ["red","green","blue","yellow","purple","orange","violet","grey","black"]
	monster_ID = 1 


class Player():
	
	def __init__(self,NME,HP,STR,ATK,DEX,DEF,base_DEF,DMG,INV,EQP,XP,status):
		self.NME = NME
		self.HP = HP
		self.STR = STR
		self.ATK = ATK
		self.DEX = DEX
		self.DEF = DEF
		self.base_DEF = base_DEF
		self.DMG = DMG
		self.INV = INV
		self.EQP = EQP
		self.XP = XP
		self.status = status
		
		
	def create_player():
		player_equip = {'head':0,'body':0,'hands':0,'legs':0,'feet':0,'main hand':0,'off hand':0}
		player_1 = Player("name",100,10,0,5,0,8,1,[],player_equip,0,[])
		World.player_1 = player_1	
		
		
class Monster:
	
	def __init__(self, name,HP,ATK,DEF,DEX,weapon,aggro,XP,DMG,night_vision,DMG_type,loot,ID,tactics):
		self.name = name
		self.HP = HP
		self.ATK = ATK
		self.DEF = DEF
		self.DEX = DEX
		self.weapon = weapon 
		self.aggro = aggro 
		self.XP = XP
		self.DMG = DMG 
		self.night_vision = night_vision
		self.DMG_type = DMG_type
		self.loot = loot
		self.ID = ID
		self.tactics = tactics
		
		
		
	def random_monster_generator(number,level):		
		name = r.choice(qm1.random_monster[number][level]["name"])
		HP = r.randint(level,qm1.random_monster[number][level]["HP"])
		ATK = r.randint(level,qm1.random_monster[number][level]["ATK"])
		DEF = r.randint(int(qm1.random_monster[number][level]["DEF"]/2),qm1.random_monster[number][level]["DEF"])
		DEX = r.randint(level,qm1.random_monster[number][level]["DEX"])
		weapon = r.choice(qm1.random_monster[number][level]["weapon"])
		aggro = r.choice(qm1.random_monster[number][level]["aggro"])
		XP = qm1.random_monster[number][level]["XP"]
		DMG = r.randint(level,qm1.random_monster[number][level]["DMG"])
		night_vision = qm1.random_monster[number][level]["night_vision"]
		DMG_type = qm1.random_monster[number][level]["DMG_type"]
		loot = qm1.random_monster[number][level]["loot"]
		ID = World.monster_ID
		tactics = r.choice(qm1.random_monster[number][level]["tactics"])
		
		if weapon == "random":
			monster_weapon = Equipment.random_equip_generator("weapon",level,r.randint(1,4))
		else:
			monster_weapon = Equipment.equip_monster(weapon)
			
		
		monster = Monster(name,HP,ATK,DEF,DEX,monster_weapon,aggro,XP,DMG,night_vision,DMG_type,loot,ID,tactics)		
		World.monster_ID += 1 	
		return monster 
		 		
		
		
class Items:
	
	def __init__(self, name, weight, type, contents, function):
		self.name = name
		self.weight = weight
		self.type = type
		self.slot = None
		self.contents = contents
		self.function = function
		
	def item_generator(item):		
		#key
		if item == "key":
			key_number = r.choice(World.key_lock_numbers)
			World.key_lock_numbers.remove(key_number)
			key_color = r.choice(World.key_colors)
			World.key_colors.remove(key_color)
			key_item = Items(key_color.title()+" Key",.5,"item", [key_number],"unlock")
			return key_item			
		#health potion
		if item == "minor health potion":
			minor_health_potion_item = Items("Minor Health Potion",2,"item",[r.randint(1,5)],"heal")
			return minor_health_potion_item
		#trap disarm kit	
		if item == "trap disarm kit":
			trap_disarm_kit_item = Items("Trap Disarm Kit",3,"item",[r.randint(1,2)],"disarm trap")
			return trap_disarm_kit_item
			
		
	def corpse_generator(name,weight,loot,level):
		corpse_name = name.title() + "'s bloody corpse"
		corpse_loot = []		
		for potential_loot in loot:
			d20 = r.randint(1,20)
			print("test loot corpse roll",d20)
			if d20+level >= 15:
				print("test score loot!")
				if  "armor" in potential_loot:
					corpse_loot.append(Equipment.random_equip_generator("armor",level,r.randint(1,4)))
				else:
					corpse_loot.append(Items.item_generator(potential_loot))								
		corpse_item = Items(corpse_name,weight,"corpse",corpse_loot,None)
		return corpse_item	
			
		
class Equipment:
	
	def __init__(self,name,ATK,DEF,weight,HP,slot,type,DMG,tactics):
		self.name = name	
		self.ATK = ATK
		self.DEF = DEF
		self.weight = weight 
		self.HP = HP
		self.slot = slot
		self.type = type
		self.DMG = DMG
		self.tactics = tactics
		self.contents = [] 
	
	def start_equip():			 		
		global nothing_equip
		nothing_equip = Equipment("Nothing",0,0,0,0,"all","nothing",0,None)				
		for slot in World.player_1.EQP:
			World.player_1.EQP[slot] = nothing_equip	
		World.player_1.EQP["body"] = Equipment("Dirty Torn Robe",0,0,.5,1,"body","armor",0,None)
		World.player_1.EQP["feet"] = Equipment("Dirty Sandals",0,0,.5,1,"feet","armor",0,None)
		World.player_1.EQP["legs"] = Equipment("Shitty Torn Pants",0,0,.5,1,"legs","armor",0,None)
		
	
	def equip_monster(name):
		monster_weapon = Equipment(name,0,0,0,0,0,"monster",0,None)
		return monster_weapon
		
		
	def equip_generator(equip): 	 
		# name /ATK /DEF /weight /HP /slot /type /DMG / Tactics
		#Torch
		if equip == "Torch":
			torch_equip = Equipment("Torch",0,0,3,15,"off hand","torch",1,None)
			return torch_equip
			
	def random_equip_generator(type,level,number):		
		name = r.choice(qe1.random_equip[type][level][number]["name"])		
		weight = qe1.random_equip[type][level][number]["weight"]
		HP = r.randint(level,qe1.random_equip[type][level][number]["HP"])
		slot = qe1.random_equip[type][level][number]["slot"]
		type = qe1.random_equip[type][level][number]["type"]
		DEF = r.randint(level,qe1.random_equip[type][level][number]["DEF"])
		if type == "weapon":
			ATK = r.randint(level,qe1.random_equip[type][level][number]["ATK"])	
			DMG = r.randint(level,qe1.random_equip[type][level][number]["DMG"])
			tactics = qe1.random_equip[type][level][number]["tactics"]
		else:
			ATK = 0
			DMG = 0	
			tactics = None	
		equipment = Equipment(name,ATK,DEF,weight,HP,slot,type,DMG,tactics)
		return equipment
	
			
			
class RoomFeature():
	
	def __init__(self,name,description,action,contents,searched):
		self.name = name
		self.description = description
		self.action = action
		self.contents = contents
		self.searched = searched
		
		
	def feature_generator(feature):
		pass
	
	
class Room():	
	
	def __init__(self,coordinates,description,name,contents,feature,exits,door_type,conditions,items,monsters,lock_number):
		self.coordinates = coordinates
		self.description = description
		self.name = name
		self.contents = contents
		self.feature = feature
		self.exits = exits
		self.door_type = door_type
		self.conditions = conditions 
		self.items = items 
		self.monsters = monsters 
		self.lock_number = lock_number
		
		
	def starting_room():
		#key_item = Items.item_generator("key")
		coordinates = (0,0)
		description = "a giant"
		name = "tomb"
		contents = "with hieroglyphics written on the walls. Large statues flank the passage in front of you."
		feature = ""
		exits = {"North":"2","East":False,"South":False,"West":False}
		door_type = "huge stone"
		conditions = {"dark":False,"searched":True}
		items = [Equipment.random_equip_generator(r.choice(["weapon","armor"]),1,r.randint(1,4)),Items.item_generator("key"),Items.item_generator("minor health potion"),Items.item_generator("trap disarm kit")]
		monsters = []
		lock_number = 0
		# things to add to start room:
		items.append(Equipment.equip_generator("Torch"))
		#items.append(Equipment.random_equip_generator(r.choice(["weapon","armor"]),1,r.randint(1,4)))
		#monsters.append(Monster.random_monster_generator(r.randint(1,3),1))
		#generate room:
		room = Room(coordinates,description,name,contents,feature,exits,door_type,conditions,items,monsters,lock_number)
		World.master_room_list.append(room)
		
	
	def roll_random_exits(direction,entrance_door):		
		bordering_rooms,connected_exit = Checks.bordering_rooms_check()
		if World.potential_exits >= World.potential_exits_threshhold:
			print("\nTEST too many PEs! make a DE!")
			possible_room_exits = [False]
		else:
			possible_room_exits = qa1.possible_room_exits[World.current_world_level]
		exit = r.choice(possible_room_exits)		
		if direction in bordering_rooms:		
			exit = connected_exit[direction]	
		return exit		
		
		
	def new_room_generator(level):						
		(x,y) = World.player_coordinates["x"],World.player_coordinates["y"]
		coordinates = (x,y)
		darkness = r.choice(qa1.potential_room_darkness[level])
		description = r.choice(qa1.possible_room_descriptions[level])
		name = r.choice(qa1.possible_room_names[level])
		contents = r.choice(qa1.possible_room_contents[level])
		feature = ""
		exits = {"North":Room.roll_random_exits("North","North door"),"East":Room.roll_random_exits("East","East door"),"South":Room.roll_random_exits("South","South door"),"West":Room.roll_random_exits("West","West door")}
		door_type = r.choice(qa1.possible_room_door_types[level]) 
		conditions = {"dark":darkness,"searched":False}
		items = []
		monsters = Game.monster_spawn(World.current_world_level)		
		#DEAD END CHECK		
		if Room.dead_end_check(exits)[0] == 0 and (Room.dead_end_check(exits)[1] - 1) == 0:
			#print("\nROOM RE-ROLL!!!")
			Room.new_room_generator(World.current_world_level)
		else:
			has_locked_door = False
			for direction in exits:
				if exits[direction] == "0":					
					has_locked_door = True				
					break
			if has_locked_door == True:
				lock_number = r.choice(World.room_lock_numbers)
				World.room_lock_numbers.remove(lock_number)							
			else:
				lock_number = 0	
			# GENERATE ROOM			
			room = Room(coordinates,description,name,contents,feature,exits,door_type,conditions,items,monsters,lock_number)
			World.master_room_list.append(room)		
			World.potential_exits -= 1 
			for e in exits:
				if int(exits[e]) != 0:
					World.potential_exits += 1  
	
	
	def dead_end_check(exits):
		room_exits = 0 
		temp_potential_exits = World.potential_exits - 1
		for e in exits:
			if int(exits[e]) != 0:
				temp_potential_exits += 1 
			room_exits += int(exits[e])		
		return temp_potential_exits,room_exits
		
		
	def unlock_special_room_generator(direction):
		level = World.current_world_level
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		(x,y) = location.coordinates		
		print("TEST generate special room!")
		south = False
		west = False
		north = False
		east = False 
		if direction == "North":
			x += 1 
			south = "1"
		elif direction == "East":
			y += 1
			west = "1"
		elif direction == "South":
			x += -1
			north = "1"
		elif direction == "West":
			y += -1 
			east = "1"
		description = "a very"
		name = "special room"
		contents = "with neat stuff!"
		feature = ""
		exits = {"North":north,"East":east,"South":south,"West":west}
		door_type = r.choice(qa1.possible_room_door_types[level]) 
		conditions = {"dark":False,"searched":False}
		items = []
		monsters = []
		lock_number = 0 			
		room = Room((x,y),description,name,contents,feature,exits,door_type,conditions,items,monsters,lock_number)
		World.master_room_list.append(room)
		

class Display():
	
	def determine_room_exits(current_room_index):
		location = World.master_room_list[current_room_index]
		room_exits_pathways = []
		room_exits_doors = []
		for exit in location.exits:			
			if location.exits[exit] == True: 	
				room_exits_pathways.append(exit)
			if location.exits[exit] == "1": 	
				room_exits_doors.append(exit + " (open)")
			if location.exits[exit] == "2": 	
				room_exits_doors.append(exit + " (closed)")
			if location.exits[exit] == "3": #trapped
				room_exits_doors.append(exit + " (closed)")
			if location.exits[exit] == "0":
				room_exits_doors.append(exit + " (locked)")	
		return room_exits_pathways,room_exits_doors			
			
	
	def display_room(current_room_index):	
		location = World.master_room_list[current_room_index]	
		if World.player_1.EQP['off hand'].type == "torch":
			notorchlight = False		
		else:
			notorchlight = True	   
		if location.conditions["dark"] + notorchlight > 1:
			World.global_torchlight = False 		
			print('\n{}It is pitch black...you see nothing'.format(Graphics.msg_decorator2))
		else:		
			exits_pathways = Display.determine_room_exits(current_room_index)[0]
			exits_doors = Display.determine_room_exits(current_room_index)[1]			
			doors = ""
			pathways = ""
			door_type = location.door_type
			if len(exits_doors) > 0:			
				if len(exits_doors) == 1:
					doors = "there is a " + door_type + " door to the " + exits_doors[0].lower()
				elif len(exits_doors) == 2: 
					doors = "there are " + door_type + " doors to the " + exits_doors[0].lower() + " and " + exits_doors[1].lower()
				elif len(exits_doors) == 3: 
					doors = "there are " + door_type + " doors to the " + exits_doors[0].lower() + ", " + exits_doors[1].lower() + " and " + exits_doors[2].lower()
				elif len(exits_doors) == 4: 
					doors = "there are " + door_type + " doors to the " + exits_doors[0].lower() + ", " + exits_doors[1].lower() + ", " + exits_doors[2].lower() + " and "+exits_doors[3].lower()					
			else:
				pathways = "there "			
			if len(exits_pathways) > 0:
				if len(exits_doors) > 0:
					pathways = " and there "			
				if len(exits_pathways) == 1:
					pathways += "is an open passageway to the " + exits_pathways[0].lower()
				elif len(exits_pathways) == 2:
					pathways += "are open passageways to the " + exits_pathways[0].lower() + " and " + exits_pathways[1].lower()
				elif len(exits_pathways) == 3:
					pathways += "are open passageways to the " + exits_pathways[0].lower() + ", " + exits_pathways[1].lower() + " and " + exits_pathways[2].lower()
				elif len(exits_pathways) == 4:
					pathways += "are passageways to the " + exits_pathways[0].lower() + ", " + exits_pathways[1].lower() + ", " + exits_pathways[2].lower() + " and " + exits_pathways[3].lower()							
			print("{}You find yourself in {} {} {} ".format(Graphics.msg_decorator2,location.description,location.name,location.contents,location.feature) + "You can see {}{}.".format(doors,pathways))
			#OBJECTS		
			if len(location.items) != 0:
				if len(location.items) == 1:
					print("There is an object in the room:")
					for item in (location.items):
						print("\t(",item.name,")")
				else:
					print("There are some objects in the room:")
					for item in (location.items):
						print("\t(",item.name,")")
			#MONSTERS	
			temp_monster_list = []
			for monster in location.monsters:
				temp_monster_list.append([monster.name,monster.aggro,monster.HP,monster.ATK,monster.DEF,monster.DMG])	
			if len(temp_monster_list) == 0:
				pass
			else:
				print("MONSTER(S) in the room:")
				for monster in sorted(temp_monster_list):
					aggro = "is minding it's own business"
					if monster[1] == True:
						aggro = "aggressive"
					else:
						pass				
					print("\t({}) *{}*".format(monster[0],aggro),"<HP:{} ATK:{} DEF:{} DMG:{}>".format(monster[2],monster[3],monster[4],monster[5]))	
				


class Game():
	
	def dashboard():				
		print('\n --[HP:{}] [ATK:{}] [DEF:{}] [DEX:{}] [MAX WEP DMG:{}] [XP:{}] (unexplored exits:{} total rooms:{})--'.format(World.player_1.HP,World.player_1.ATK,World.player_1.DEF,World.player_1.DEX,World.player_1.DMG,World.player_1.XP,World.potential_exits,len(World.master_room_list)))		
								
	
	def determine_room_index(): 
		global current_room_index 
		for room in World.master_room_list:
			room_coordinates = room.coordinates
			if World.player_coordinates['x'] == room_coordinates[0] and World.player_coordinates['y'] == room_coordinates[1]:
				current_room_index = World.master_room_list.index(room)
				
				
	def update():
		Checks.torchlight_burn()
		Game.dashboard()
		Checks.player_atack_defense()
		Checks.aggro_monster()
		Checks.check_weight()
		Checks.status_effects()		
		
		
	def action():
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		action = input('\n{} What would you like to do? ("?" for help) '.format(Graphics.msg_decorator1)).lower()
		InputParser.action_input_parser(action)		
		
			
	def new_room():		
		World.potential_exits -= 1
		#World.potential_exits_threshhold -= 1 	
		Room.new_room_generator(World.current_world_level)
		new_room_index = len(World.master_room_list) - 1
		Display.display_room(new_room_index)
		
		
	def trigger_door_trap():
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		trap = r.choice(qa1.possible_room_trap_types[World.current_world_level])
		trap_description = trap[0]
		trap_damage_type = trap[1]
		trap_max_damage = trap[2]		
		trap_damage = r.randint(1,trap_max_damage)
		World.player_1.HP -= trap_damage
		print("\n[TRAP!] As you motion your hand forward to open the door {} <YOU TAKE {} {} DAMAGE> as the {} door opens.".format(trap_description,trap_damage,trap_damage_type.upper(),location.door_type))
		
			
	def monster_spawn(level):
		spawn_list = []
		d6 = r.randint(1,6)
		if d6 <= 3:
			pass
		elif d6	== 6:
			spawn_list.append(Monster.random_monster_generator(r.randint(1,3),level))
			spawn_list.append(Monster.random_monster_generator(r.randint(1,3),level))
		elif d6 in [4,5]:
			spawn_list.append(Monster.random_monster_generator(r.randint(1,3),level))
		return spawn_list
		
		
class InputParser():
	
	def action_input_parser(input):
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]				
		input_split = input.split()
		try:
			action = input_split[0]
		except:
			action = ""
		try:
			arg_1 = input_split[1]
		except:
			pass
		try:
			arg_2 = input_split[2]
		except:
			pass
		try:
			arg_3 = input_split[3]
		except:
			pass						
		
		#open
		if action in ("open", "op"):
			try:				
				Commands.open_door(arg_1)
			except:				
				print("\n[-] Open what direction?\n")	
				
		#close
		if action in ("close", "cl"):
			try:
				Commands.close_door(arg_1)
			except:				
				print("\n[-] Close what direction?\n")	
				
		#unlock
		if action in ("unl", "ul", "unlock"):
			#try:
			Commands.unlock_door(arg_1)
			#except:				
				#print("\n[-] Unlock what direction?\n")	
		
		#search
		if action in ("search", "se","sea"):
			try:
				Commands.search_room(arg_1)
			except:
				print("\n[-] Search what?")			
				
		#movement		
		if action in ("north","n"):						
			Movement.move("North","South","x",1)
		if action in ("east","e"):
			Movement.move("East","West","y",1)
		if action in ("south","s"):
			Movement.move("South","North","x",-1)
		if action in ("west","w"):
			Movement.move("West","East","y",-1)	
			
		#view inventory
		if action in ("i","inventory","inv"):
			Commands.view_inventory()
			
		#pickup
		if action in ("g","ge","get"):			
			try:
				try:
					input = arg_1 + " " + arg_2
				except:
					input = arg_1				
				Commands.get(input)
			except:
				print("\n[-] Get what?")
				
		#drop
		if action in ("dr","drop"):
			try:
				try:
					input = arg_1 + " " + arg_2
				except:
					input = arg_1			
				Commands.drop(input)
			except:
				print("\n[-] Drop what?")
				
		#use
		if action in ("use","us"):
			#try:
			try:
				input = arg_1 + " " + arg_2
			except:
				input = arg_1			
			Commands.use(input)
			#except:
				#print("\n[-] Use what?")
				
		#equip
		if action in ("eq","equip"):
			try:
				try:
					input = arg_1 + " " + arg_2
				except:
					input = arg_1			
				Commands.equip(input)
			except:
				print("\n[-] Equip what?")
				
		#unequip
		if action in ("unequip","un","une"):
			try:
				try:
					input = arg_1 + " " + arg_2
				except:
					input = arg_1			
				Commands.unequip(input)
			except:
				print("\n[-] Unequip what?")
				
		#look
		if action in ("l","look"):
			Commands.look()	
			
		#attack
		if action in ("a","at","attack"):
			#try:
			try:
				input = arg_1 + " " + arg_2
			except:
				input = arg_1			
			Combat.engage_combat(input)
			#except:
				#print("\n[-] Attack what?")
				
		#loot
		if action in ("lo","loo","loot"):
			#try:
			try:
				input = arg_1 + " " + arg_2
			except:
				input = arg_1
			Commands.loot(input)
			#except:
				#print("\n[-] Loot what?")
				
		#spawn a monster
		if action == ("spawn"):
			location.monsters.append(Monster.random_monster_generator(r.randint(1,3),1))
			
		#disarm trap
		if action in ("di","dis","disarm"):
			Commands.disarm_trap(arg_1)
			
		#name equipment
		if action == ("name"):
			try:
				equip = arg_1
				name = arg_2
				Commands.name_equip(equip,name)
			except:
				pass
			
			
				
		
		
class Checks():
		
	def bordering_rooms_check():
		Game.determine_room_index()		
		(x,y) = (World.player_coordinates['x'],World.player_coordinates['y'])	
		bordering_rooms = []	
		connecting_exit = {} 	
		for room in World.master_room_list:
			if room.coordinates == (x+1,y):					
				bordering_rooms.append("North")									
				connecting_exit["North"] = room.exits["South"]						
			if room.coordinates == (x,y+1):					
				bordering_rooms.append("East")				
				connecting_exit["East"] = room.exits["West"]				
			if room.coordinates == (x-1,y):				
				bordering_rooms.append("South")					
				connecting_exit["South"] = room.exits["North"]				
			if room.coordinates == (x,y-1):					
				bordering_rooms.append("West")				
				connecting_exit["West"] = room.exits["East"]				
		return bordering_rooms,connecting_exit
		
		
	def open_door_check():		
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		for exit in location.exits:
			if location.exits[exit] in ["2","3","0"]:				
				if exit in new_room_entrance:					
					location.exits[exit] = "1"
					
					
	def player_atack_defense():		
		attack = 0
		defence = 0 
		damage = 1
		for slot in World.player_1.EQP:
			equip = World.player_1.EQP[slot]
			if equip.type == 'weapon':
				attack += equip.ATK 
				defence += equip.DEF
				damage += equip.DMG
			elif equip.type == 'armor':
				defence += equip.DEF
		World.player_1.ATK = attack
		World.player_1.DEF = defence
		World.player_1.DMG = damage 
		
		
	def torchlight_burn():
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		global has_torchlight
		has_torchlight = False		
		torch = 0 
		if World.player_1.EQP["off hand"].type == "torch":
			has_torchlight = True			
			if World.player_1.EQP["off hand"].HP <= 0:
				print("\n(((Your {} RUNS OUT!!)))".format(World.player_1.EQP["off hand"].name))
				World.player_1.EQP['off hand'] = nothing_equip
			elif World.player_1.EQP["off hand"].HP <= 4:
				World.player_1.EQP["off hand"].HP -= 1
				print('\n)))Your {} is running low but still lights the area((('.format(World.player_1.EQP["off hand"].name),World.player_1.EQP["off hand"].HP)				
			else:
				World.player_1.EQP["off hand"].HP -= 1
				if location.conditions["dark"] == True:
					print('\n)))Your {} glows bright and lights the dark area!((('.format(World.player_1.EQP["off hand"].name),World.player_1.EQP["off hand"].HP)		
				else:
					print('\n)))Your {} is wasting away ...the area is already lit!((('.format(World.player_1.EQP["off hand"].name),World.player_1.EQP["off hand"].HP)					
					
					
	def aggro_monster():
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		start_battle = False
		for monster in location.monsters:
			if monster.aggro == True:
				monster_ID = monster.ID
				#start_battle = True	
				if location.conditions["dark"] == True:
					if has_torchlight == False:
						#check for nightvision here:
						if monster.night_vision == True:
							print("\n*** You sense something in the darkness moving closer to attack you! ***")
							#Combat.monster_start_combat()
							start_battle = True
					else:
						print("\n*** The {} is pissed! It is moving to attack you! ***".format(monster.name))
						start_battle = True
						#Combat.monster_start_combat()						
				else:		
					print("\n*** The {} is pissed! It is moving to attack you! ***".format(monster.name))
					start_battle = True 
					#Combat.monster_start_combat()
		if start_battle == True:
			pass
			Combat.monster_start_combat(monster_ID)
			start_battle = False
			
			
	def check_weight(): 		 
		total_weight = 0	
		for object in World.player_1.INV:
			total_weight += object.weight		
		if total_weight > World.player_1.STR:
			print('\n\t!!! You are carrying too much weight !!!')
			if "over encumbered" not in World.player_1.status:
				World.player_1.status.append("over encumbered")
		else:
			try:
				World.player_1.status.remove("over encumbered")
			except:
				pass 
			
	def status_effects():
		if len(World.player_1.status) > 0:
			print("\n*** Player status effects:",World.player_1.status,"***")		
		
	
	
class Movement():
	
	def move_action():		 
		Game.determine_room_index()		
		temp_room_coord_List = []
		(x,y) = (World.player_coordinates['x'],World.player_coordinates['y'])
		for room in World.master_room_list:
			temp_room_coord_List.append(room.coordinates)
		if (x,y) in temp_room_coord_List:
			print("{}Entering from the {}...".format(Graphics.msg_decorator2,new_room_entrance.lower()))
			Checks.open_door_check()
			Display.display_room(current_room_index)		
		else:
			print("{}Entering from the {}...".format(Graphics.msg_decorator2,new_room_entrance.lower()))
			Game.new_room()
			
	
	def move(direction,entrance,axis,int):
		if "over encumbered" in World.player_1.status:
			print("\n[-] You can't move! You're over encumbered! Drop some weight!")
		else:		
			global new_room_entrance
			Game.determine_room_index()
			location = World.master_room_list[current_room_index]
			if location.exits[direction] in ["2","3"]:
				print("\n[-] You can't go {}, the {} door is closed.\n".format(direction.lower(),location.door_type.lower()))
				Display.display_room(current_room_index)	
			elif location.exits[direction] == True:
				new_room_entrance = entrance			
				print("\n[+] You make your way {}.\n".format(direction.lower()))
				World.player_coordinates[axis] += int
				Movement.move_action()
			elif location.exits[direction] == "1":
				new_room_entrance = entrance + " door"			
				print("\n[+] You make your way {}.\n".format(direction.lower()))
				World.player_coordinates[axis] += int
				Movement.move_action()
			else:
				print("\n[-] You can't go {}.".format(direction.lower()))
				Display.display_room(current_room_index)		
			
	
	def flee(direction,entrance,axis,int):
		global new_room_entrance
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		if location.exits[direction] in ["2","3"]:
			print("\n[-] You can't flee {}, the {} door is closed!!!".format(direction.lower(),location.door_type.lower()))
			Combat.monster_start_combat()
			#Display.display_room(current_room_index)	
		elif location.exits[direction] == True:
			new_room_entrance = entrance			
			print("\n[+] You flee {}!!!\n".format(direction.lower()))
			World.player_coordinates[axis] += int
			Movement.move_action()
		elif location.exits[direction] == "1":
			new_room_entrance = entrance + " door"			
			print("\n[+] You flee {}!!!\n".format(direction.lower()))
			World.player_coordinates[axis] += int
			Movement.move_action()
		else:
			print("\n[-] You can't flee {}.".format(direction.lower()))
			#Display.display_room(current_room_index)
			Combat.monster_start_combat()					
			
				
class Combat():
	
	def combat_input_parser(input):
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]				
		input_split = input.split()
		try:
			action = input_split[0]
		except:
			action = ""
		try:
			arg_1 = input_split[1]
		except:
			pass
		try:
			arg_2 = input_split[2]
		except:
			pass
		try:
			arg_3 = input_split[3]
		except:
			pass	
			
		#flee
		if action in ["flee","f","fl"]:
			#print("\n***You FLEE!***")
			try:
				if arg_1 in ("north","n"):						
					Movement.flee("North","South","x",1)
				elif arg_1 in ("east","e"):
					Movement.flee("East","West","y",1)
				elif arg_1 in ("south","s"):
					Movement.flee("South","North","x",-1)
				elif arg_1 in ("west","w"):
					Movement.flee("West","East","y",-1)
			except:
				#print("\n[-] Flee what direction!?")
				#Combat.monster_start_combat(attacking_monster_ID)
				pass
				
		#view inventory
		if action in ("i","inventory","inv"):
			Commands.view_inventory()
			
		#attack
		if action in ("a","at","attack"):
			#try:
			try:
				input = arg_1 + " " + arg_2
			except:
				input = arg_1			
			Combat.engage_combat(input)
			#except:
				#print("\n[-] Attack what?")
				
		#look
		if action in ("l","look"):
			Commands.look()
			
		#engage
		if action in ("e","en","engage"):
			for monster in location.monsters:
				if attacking_monster_ID == monster.ID:
					target = monster.name
			Combat.engage_combat(target)
			
			
		#update		
		Game.update()	
		
	
	def monster_start_combat(monster_ID):
		
		global attacking_monster_ID 
		attacking_monster_ID = monster_ID
		combat_input = input('\n{} What would you like to do, engage or flee? ("?" for help) '.format(Graphics.msg_decorator1)).lower()
		Combat.combat_input_parser(combat_input)	
	
	
	def engage_combat(target): #target = self if monster attack first
		#cant start combat in the dark!
		Game.determine_room_index()		
		location = World.master_room_list[current_room_index]
		can_engage = False
		if location.conditions["dark"] == True:
				if has_torchlight == False:
					pass
				else:					
					can_engage = True
		else:			
			can_engage = True 
		if can_engage == False:
			print("\n[-] You can't fight in the dark!")
		else:
			Game.determine_room_index()		
			location = World.master_room_list[current_room_index]
			player_weapon = World.player_1.EQP["main hand"].name.upper()
			if World.player_1.EQP["main hand"].name.lower() == "nothing":
				player_weapon = "FISTS"
			#choose target:
			global initiative_list 
			initiative_list = []
			for monster in location.monsters:			
				if target.lower() in monster.name.lower():
					monster.aggro = True
					global target_monster 				
					target_monster = monster
					#monster_weight = target_monster.HP * 2	
					break	
			for monster in location.monsters: 		
				if monster.aggro == True:
					initiative_list.append((r.randint(1,20)+monster.DEX,monster.name,monster.ID))
			#determine initiative:					
			initiative_list.append((r.randint(1,20)+World.player_1.DEX,World.player_1.NME,""))
			initiative_list.sort(reverse=True)
			print("\n\t\t  ------ENGAGING COMBAT------      \n")
			#print("test",initiative_list,"\n")
			print("\t     rolling initiative order...\n")
			y = 1
			for x in initiative_list:
				print("\t\t  {}".format(str(y)+"."),x[1])
				y += 1 
			#for x in initiative_list:
			Combat.battle_rounds()
			
		
	def battle_rounds():
		Game.determine_room_index()		
		location = World.master_room_list[current_room_index]		
		combat_round = 0
		global combat_over 
		combat_over = 0 
		for monster in location.monsters:
				combat_over += monster.aggro				
		while combat_over > 0:
			combat_round += 1
			print("\n            ----BATTLE ROUND {}---       ".format(combat_round))
			Combat.combat_tactics()
			for x in initiative_list:
				if x[1] == World.player_1.NME:
					Combat.player_attack()
				else:
					Combat.monster_attack(x[2])
					#PROBLEM HERE! if two monsters w same name, atk twice!
					#break	#< 		
			if combat_over == 0:					
				Combat.combat_end()
			else:			
				print('\n\t----Target monster:',target_monster.name," HP:",target_monster.HP,'----')	
				Game.dashboard()	
				player_input = input('\n<<<< Bottom of the combat round! What would you like to do, flee or continue the fight? ("?" for help)')
				#add options here:
				#Combat.bottom_of_round_parser(attack)
				input_split = player_input.split()
				try:
					action = input_split[0]
				except:
					action = ""
				try:
					arg_1 = input_split[1]
				except:
					pass
				#flee
				if action in ["flee","f","fl"]:
					#print("\n***You FLEE!***")
					try:
						if arg_1 in ("north","n"):		
							#break				
							Movement.flee("North","South","x",1)
							break
						elif arg_1 in ("east","e"):
							#break
							Movement.flee("East","West","y",1)
							break
						elif arg_1 in ("south","s"):
							#break
							Movement.flee("South","North","x",-1)
							break
						elif arg_1 in ("west","w"):
							#break
							Movement.flee("West","East","y",-1)
							break
					except:
						pass
						#print("\n[-] Flee what direction!?")
						#Combat.monster_start_combat()
				
				
				
	def bottom_of_round_parser(): #not sure about this 
		pass	
			
			
	def monster_dies():	
		global combat_over
		combat_over -= 1 
		Game.determine_room_index()		
		location = World.master_room_list[current_room_index]	
		monster_weight = target_monster.XP * 2	
		print("test monster weight:",monster_weight)
		print("\n\t***The {} is fucking dead! You gain {} XP!***\n".format(target_monster.name,target_monster.XP))
		World.player_1.XP += target_monster.XP
		if target_monster.weapon.type != "monster":
			print("\t***The {} dropped it's {} to the ground!***".format(target_monster.name,target_monster.weapon.name.upper()))
			location.items.append(target_monster.weapon)				
		location.monsters.remove(target_monster)
		#initiative_list.remove(target_monster.name)	
		# NEED TO REMOVE MONSTER FROM INITIATIVE LIST?
		for x in initiative_list:
			if x[2] == target_monster.ID:
				initiative_list.remove(x)
		location.items.append(Items.corpse_generator(target_monster.name,monster_weight,target_monster.loot,World.current_world_level))				
		
		
	def player_attack():			
		print("\n\t\t\t     ->YOUR TURN!<-")			
		attack = input("\n<<<< Choose your move! {}".format(player_round_tactics))
		Combat.basic_attack()
		# need to add tactics from weapon and stance here... 
		
	def basic_attack():
		#NORMAL attack math starts here...
		player_weapon = World.player_1.EQP["main hand"].name.upper()
		if World.player_1.EQP["main hand"].name.lower() == "nothing":			
			player_weapon = "FISTS" # unarmed
		d20 = r.randint(1,20)
		if d20 == 20:
			print("\n\t !!! CRITICAL HIT !!!")
		attacknum = d20 + World.player_1.ATK
		print('\n\tyour d20 roll + your HIT={} vs monsters DEF={}'.format(attacknum,target_monster.DEF))
		if attacknum >= target_monster.DEF:
			maxd = World.player_1.DMG
			if d20 == 20:
				damage = maxd + 1 
			else:
				damage = r.randint(1,maxd)
			print("\n\t***You attack and hit with your {} doing <{} DAMAGE!>***".format(player_weapon,damage))
			target_monster.HP -= damage 
			if target_monster.HP <= 0:
				Combat.monster_dies()				
				Combat.switch_target()			
		else:
			print("\n\t***You attack with your {} but MISS!***".format(player_weapon))
			
			
	def combat_tactics():
		global player_round_tactics
		player_round_tactics = ["basic"]
		target_monster_tactics = target_monster.tactics
		print("test target monster's plan! {}".format(target_monster_tactics))
		
		attack = input("\n<<<< SET ATTACK STANCE! (Defensive/Aggressive/Evasive?)") 
		
		#VVV. can consolidate this shit below!! VVVV
		
		# defensive
		if attack.lower() in ["d","def","defensive"]:
			print("\n[+] Set Defensive!")
			if target_monster_tactics == "aggressive":
				print("\n[+] You have advantage!")
			if target_monster_tactics == "evasive":
				print("\n[-] You have disadvantage!")
			# ADD MORE COMMANDS HERE! "skills" based on what weapon equipped?!
			
			for slot in World.player_1.EQP:
				equip = World.player_1.EQP[slot]
				if equip.type == 'weapon' and equip.tactics["defensive"] != None: 
					print("\n\t(You may use the defensive action {} with your {})".format(equip.tactics["defensive"].upper(),equip.name.upper()))
					player_round_tactics.append(equip.tactics["defensive"])
					break
					#print("\n \t test You have a special defnesive tactic with your {}!".format(player_weapon))
					
		#aggresive	
		if attack.lower() in ["a","agg","aggressive"]:
			print("\n[+] Set Aggressive!")
			for slot in World.player_1.EQP:
				equip = World.player_1.EQP[slot]
				if equip.type == 'weapon' and equip.tactics["aggressive"] != None: 
					print("\n\tYou {} with your {}!".format(equip.tactics["aggressive"].upper(),equip.name.upper()))
					break
			# ADD MORE COMMANDS HERE! 
			
		#evasive
		if attack.lower() in ["e","eva","evasive"]:
			print("\n[+] Set evasive!")
			for slot in World.player_1.EQP:
				equip = World.player_1.EQP[slot]
				if equip.type == 'weapon' and equip.tactics["evasive"] != None: 
					print("\n\tYou {} with your {}!".format(equip.tactics["evasive"].upper(),equip.name.upper()))
					break
		
			
	
	def monster_attack(monster_ID):
		Game.determine_room_index()		
		location = World.master_room_list[current_room_index]
		player_def = World.player_1.base_DEF + World.player_1.DEF
		for monster in location.monsters:
			if monster_ID == monster.ID:
				if monster.HP > 0:
					print("\n\t\t\t->{}'s TURN!<-".format(monster.name.upper()))
					print("\n\t{} is coming in to attack!".format(monster.name))
					#MAYBE DIFFERENT MONSTER ATTACKS HERE?
					d20 = r.randint(1,20)
					attack_total = d20 + monster.ATK
					print('\n\tmonster total ATK:{} vs player total DEF:{}'.format(attack_total,player_def))
					if attack_total >= player_def:	
						if location.conditions["dark"] == True:
							if has_torchlight == False:
								monster_name = 'Something'
							else:
								monster_name = monster.name
						else:
							monster_name = monster.name			
						max_dam = monster.DMG
						monster_damage = r.randint(1,max_dam)
						World.player_1.HP -= monster_damage 
						print("\n\t***{} attacks you with it's {}! <YOU TAKE {} {} DAMAGE!>***".format(monster_name,monster.weapon.name.upper(),monster_damage,monster.DMG_type.upper()))
						if World.player_1.HP <= 0:
							pass
							print("\nGAME OVER")
					else:
						if location.conditions["dark"] == True:
							if has_torchlight == False:
								monster_name = "Something"
							else:
								monster_name = monster.name
						else:
							monster_name = monster.name
						print("\n\t***{} attacks and <MISSES!>***".format(monster_name))
						
						
	def switch_target(): 
		Game.determine_room_index()		
		location = World.master_room_list[current_room_index]
		for x in initiative_list:
				if x[1] == World.player_1.NME:
					pass
				else:
					for monster in location.monsters:
						if x[1] in monster.name:
							print("test new target! {}".format(monster.name))
							global target_monster
							target_monster = monster
							print("2test new target! {}".format(target_monster.name)) 	
						
						
	def combat_end():
		print("\n\t ***The dust settles and the combat is over!***\n")
		Display.display_room(current_room_index)
		Game.dashboard()
		Game.action()			
						

class Commands():
	
	def open_door(input):
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		if input in ["n", "north"]:
			direction = "North"
		if input in ["e", "east"]:
			direction = "East"
		if input in ["s", "south"]:
			direction = "South"
		if input in ["w", "west"]:
			direction = "West"		
		if location.exits[direction] == "2":
			location.exits[direction] = "1"		
			print("\n[+] As you motion your hand forward, the {} door to the {} slides open.".format(location.door_type,direction.lower()))
		elif location.exits[direction] == "3":
			location.exits[direction] = "1"			
			Game.trigger_door_trap()			
		else:
			print("\n[-] You can't open anything in that direction.")		
		
	
	def close_door(input):
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		if input in ["n", "north"]:
			direction = "North"
		if input in ["e", "east"]:
			direction = "East"
		if input in ["s", "south"]:
			direction = "South"
		if input in ["w", "west"]:
			direction = "West"		
		if location.exits[direction] == "1":
			location.exits[direction] = "2"		
			print("\n[+] As you motion your hand forward, the {} door to the {} slides closed.\n".format(location.door_type,direction.lower()))				
		else:
			print("\n[-] You can't close anything in that direction.\n")
		Display.display_room(current_room_index)
		
		
	def unlock_door(input):
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		has_keys = False
		correct_key = False
		if input in ["n", "north"]:
			direction = "North"
		if input in ["e", "east"]:
			direction = "East"
		if input in ["s", "south"]:
			direction = "South"
		if input in ["w", "west"]:
			direction = "West"		
		if location.exits[direction] == "0":
			print("TEST ROOM LOCK #",location.lock_number)
			for item in World.player_1.INV:
				if item.type == "item":
					if item.function == "unlock":
						has_keys = True
						print("TEST KEY #",item.contents[0])
						if item.contents[0] == location.lock_number:
							correct_key = True							
							print("\n[+] Success! You unlock the {} door with your {}".format(direction,item.name))
							location.exits[direction] = "2"
							World.player_1.INV.remove(item)
							World.potential_exits += 1 							
							if r.randint(1,2) == 2:
								print("\n yay special room!")
								Room.unlock_special_room_generator(direction)							
							break				
			if has_keys == False:		
				print("\n[-] You don't have any keys!")
			else:				
				if correct_key == False:
					print("\n[-] You don't have the matching key for that door.")	
				else:
					pass			
		else:
			print("\n[-] You can't unlock anything in that direction.")		
		
		
	def search_room(input):		
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		can_search = False
		if location.conditions["dark"] == True:
				if has_torchlight == False:
					pass
				else:					
					can_search = True
		else:			
			can_search = True 
		if can_search == False:
			print("\n[-] You can't search in the dark!")
		else:		
			if location.conditions["searched"] == False:
				#TRAPS
				if input in ["t","tra","trap","traps"]:
					Search.search_traps()
					location.conditions["searched"]	= True	
				#OTHER SEARCHABLES HERE...		
			else:
				print("\n[-] You have already searched this room.")
			
			
	def view_inventory():		
		total_weight = 0 
		inv = []
		print('\nYour Inventory:')		
		print('\nCarried items:\n')
		for item in (World.player_1.INV):
			inv.append(item.name)			
			total_weight += item.weight		
		for item_name in sorted(inv):
			print('\t',item_name)
		print('\nEquipment worn/wielded:\n')
		for slot in World.player_1.EQP:				
			print('\t',slot.title(),'-',World.player_1.EQP[slot].name)		
		print('\nCarried weight:',total_weight,'out of',World.player_1.STR)
		
		
	def use(input):
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		object_usable = False	
		for object in World.player_1.INV:
			if input in object.name.lower():
				if object.type == "item":
					#HEAL! use potion
					if object.function == "heal":
						object_usable = True
						heal_amount = object.contents[0]
						print("\n[+] You use your {} and heal {}HP!".format(object.name.lower(),heal_amount))
						World.player_1.HP += heal_amount
						World.player_1.INV.remove(object)	
						break # is this working???	
					#OTHER USEABLES HERE...
					
				#use as equip...			
				if object.type in ["weapon","armor","torch"]:
					object_usable = True
					InputParser.action_input_parser("equip "+input)						
				if object_usable == False:				
					print("\n[-] You can't find any use for the {}".format(object.name))		
		
		
	def get(input):
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		if input in ["al","all"]:
			for object in location.items:
				World.player_1.INV.append(object)												
				print('\n[+] You picked up the {}.'.format(object.name))
			location.items =[]	
		else:
			for object in location.items:
				if object != False:
					if input in object.name.lower():				
						location.items.remove(object)
						World.player_1.INV.append(object)					
						print('\n[+] You picked up the {}.'.format(object.name))
						break				
					
					
	def drop(input):
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]	
		if input in ["al","all"]:
			for object in World.player_1.INV:
				location.items.append(object)
				print('\n[+] You dropped the {}.'.format(object.name))
			World.player_1.INV = []
		else:			
			for object in World.player_1.INV:			
				if input in object.name.lower():			
					World.player_1.INV.remove(object)
					location.items.append(object)
					print('\n[+] You dropped the {}.'.format(object.name))
					break
				
				
	def equip(what):
		for object in World.player_1.INV:				
			if what in object.name.lower():				
				if object.type != "item":
					# One and two handed weapons here!
					if object.type in ["weapon"]:
						#print("\ntest equip weapon to appropriate hand")
						if object.slot == "one hand":
							if World.player_1.EQP["main hand"] == nothing_equip:	
								World.player_1.EQP["main hand"] = object
								World.player_1.INV.remove(object)	
								print("\n[+] You wield the {} with {}!".format(object.name.title(),object.slot))						
								break
							else:
								#print("\n[-] You already have something equipped there.")
								#break
								if World.player_1.EQP["off hand"] == nothing_equip:
									World.player_1.EQP["off hand"] = object
									World.player_1.INV.remove(object)	
									print("\n[+] You wield the {} with {}!".format(object.name.title(),object.slot))						
									break
								else:
									print("\n[-] You already have something equipped there.")
									break
						if object.slot == "both hands":
							if World.player_1.EQP["main hand"] == nothing_equip and World.player_1.EQP["off hand"] == nothing_equip:								
								World.player_1.EQP["main hand"] = object
								World.player_1.EQP["off hand"] = object
								World.player_1.INV.remove(object)	
								print("\n[+] You wield the {} with {}!".format(object.name.title(),object.slot))	
							else:
								print("\n[-] You already have something equipped there.")						
					# armor here!	
					else:		
						slot = object.slot
						if World.player_1.EQP[slot] == nothing_equip:
							World.player_1.EQP[slot] = object
							World.player_1.INV.remove(object)
							print("\n[+] {} equipped to {}.".format(object.name.title(),object.slot))
							break
						else:
							print("\n[-] You already have something equipped there.")
				else:
					print("\n[-] You can't equip that.")
		Checks.player_atack_defense()
		
					
	def unequip(what):
		for slot in World.player_1.EQP:			
			if what in World.player_1.EQP[slot].name.lower():	
				if World.player_1.EQP[slot].slot == "both hands":
					print("\n[+] {} unequipped.".format(World.player_1.EQP[slot].name))
					World.player_1.INV.append(World.player_1.EQP[slot])
					World.player_1.EQP["main hand"] = nothing_equip
					World.player_1.EQP["off hand"] = nothing_equip					
					break
				else:									
					print("\n[+] {} unequipped.".format(World.player_1.EQP[slot].name))
					World.player_1.INV.append(World.player_1.EQP[slot])	
					World.player_1.EQP[slot] = nothing_equip				
					break
		Checks.player_atack_defense()					
				
				
	def look():
		Game.determine_room_index()
		print("\n[+] You survey the surroundings...\n")
		#print("\n ")
		Display.display_room(current_room_index)
		
		
	def loot(input):
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]	
		for object in location.items:
			if input in object.name.lower():
				if object.type in ["corpse"]:
					loot_list = object.contents
					if len(object.contents) > 0: 
						for loot in loot_list:
							World.player_1.INV.append(loot)												
							print("\n[+] You loot <<{}>> from {}!".format(loot.name,object.name))				
						object.contents = []
						object.name += " (looted)"					
					else:
						print("\n[-] You find nothing from the {}".format(object.name))
						if "(looted)" in object.name:
							pass
						else:
							object.name += " (looted)"							
				else:
					Commands.get(input)
					#print("test you cant loot that!")
					
				
						
						
	def disarm_trap(input):		
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		has_kit = False
		current_kit = None 
		for item in World.player_1.INV:
			if item.name == "Trap Disarm Kit":
				has_kit = True
				current_kit = item
				#print("test kit uses left: {}".format(current_kit.contents[0]))
				break # <hope this helps using multiple kits at once
		if has_kit == True:
			#print("test you have a kit!")
			if input in ["n", "north"]:
				direction = "North"
			if input in ["e", "east"]:
				direction = "East"
			if input in ["s", "south"]:
				direction = "South"
			if input in ["w", "west"]:
				direction = "West"
			if location.exits[direction] == "3":
				print("\n[+] You successfully dissarm the trap on the {} door!".format(direction))
				location.exits[direction] = "2"
				current_kit.contents[0] -= 1 
				print("\nDissarm kit uses left: {}".format(current_kit.contents[0]))
				if current_kit.contents[0] <= 0:
					World.player_1.INV.remove(current_kit)
			else:
				print("\n[-] There is no trap that direction to disarm!")			
		else:
			print("\n[-] You don't have any trap disarming kits!")
		pass
		
		
	def name_equip(equip,name):
		#print("test1",equip,name)
		for object in World.player_1.INV:
			if object.type == "weapon":
				#print("test2.5")
				if equip in object.name.lower():
					#print("test3",equip,name)				
					object.name += " of " + name.title()
					print('\n[+] Changed name to "{}"'.format(object.name))
					break
		
			
		
class Search():
	
	def search_traps():
		Game.determine_room_index()
		location = World.master_room_list[current_room_index]
		print("\n[+] Searching for traps... ")
		room_trapped = False
		for exit in location.exits:			
			if location.exits[exit] == "3":
				print("\n[+] You found some kind of trap on the {} door!".format(exit.lower()))
				room_trapped = True 
		if room_trapped == False:
			print("\n[+] You find no traps in this room.")			
	

def main():	
	Player.create_player()
	player_name = input("ENTER YOUR NAME: ")
	print("\n\t YOUR ADVENTURE BEGINS\n")
	World.player_1.NME = player_name
	Equipment.start_equip()
	Room.starting_room()
	Display.display_room(0)	
	while True:
		Game.update()
		Game.action()
		
		
main()
