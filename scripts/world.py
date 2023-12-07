
import pygame
import random
from copy import deepcopy
from scripts.spike import Spike


class Room:
    def __init__(self, id, room):
        self.id = id
        self.Room = room["objects"]["Room"][0]
        self.entry_count = room["entry_count"]
        self.relativity = room["relativity"]
        self.main_entry = room["main_entry"]
        self.range = room["range"]
        self.data = room["data"]
        self.spawn = list(room["objects"]["Spawn"][0].topleft)
        self.trigger = None
        self.entries = {}
        self.valid = True
        self.spikes = {}
        
        for obj_id in room["objects"]:
            
            if "Spike" in obj_id:
                self.spikes[obj_id] = room["objects"][obj_id][0]
            
            if obj_id in ["Left", "Right", "Top", "Bottom"]:
                if room["objects"][obj_id][0] == self.main_entry:
                    self.main_entry = [room["objects"][obj_id][0], obj_id]
                self.entries[obj_id] = [room["objects"][obj_id][0], False]
    
    def update(self):
        for e in self.entries:
            if e == self.main_entry[1]:
                continue
            self.entries[e][0].topleft = [self.main_entry[0].x - self.relativity[e][0], self.main_entry[0].y - self.relativity[e][1]]
        
        self.Room.x = self.main_entry[0].x - self.relativity["Room"][0]
        self.Room.y = self.main_entry[0].y - self.relativity["Room"][1]
        
        self.spawn = [self.main_entry[0].x - self.relativity["Spawn"][0], self.main_entry[0].y - self.relativity["Spawn"][1]]
        
        for s in self.spikes:
            self.spikes[s].topleft = [self.main_entry[0].x - self.relativity[s][0], self.main_entry[0].y - self.relativity[s][1]]
    
    def closed_off(self):
        e_count = 0
        for e in self.entries:
            if self.entries[e][1]:
                e_count += 1
        return (e_count == len(self.entries))
       
       
    def connect_to_corridor(self, entry, corridor):
        if entry == "Left" and ("Right" in self.entries):
            self.entries["Right"][0].right = corridor.entries["Left"][0].left
            self.entries["Right"][0].y = corridor.entries["Left"][0].y
            self.entries["Right"][1] = True
            corridor.entries["Left"][1] = True
            
            if "Right" != self.main_entry[1]:
                self.main_entry[0].x = self.entries["Right"][0].x + self.relativity["Right"][0]
                self.main_entry[0].y = self.entries["Right"][0].y + self.relativity["Right"][1]
            
            self.update()
            return True
        elif entry == "Right" and ("Left" in self.entries):
            self.entries["Left"][0].left = corridor.entries["Right"][0].right
            self.entries["Left"][0].y = corridor.entries["Right"][0].y
            self.entries["Left"][1] = True
            corridor.entries["Right"][1] = True
            
            if "Left" != self.main_entry[1]:
                self.main_entry[0].x = self.entries["Left"][0].x + self.relativity["Left"][0]
                self.main_entry[0].y = self.entries["Left"][0].y + self.relativity["Left"][1]
        
            self.update()
            return True
        elif entry == "Top" and ("Bottom" in self.entries):
            self.entries["Bottom"][0].bottom = corridor.entries["Top"][0].top
            self.entries["Bottom"][0].x = corridor.entries["Top"][0].x
            self.entries["Bottom"][1] = True
            corridor.entries["Top"][1] = True
            
            if "Bottom" != self.main_entry[1]:
                self.main_entry[0].x = self.entries["Bottom"][0].x + self.relativity["Bottom"][0]
                self.main_entry[0].y = self.entries["Bottom"][0].y + self.relativity["Bottom"][1]
            
            self.update()
            return True
        elif entry == "Bottom" and ("Top" in self.entries):
            self.entries["Top"][0].top = corridor.entries["Bottom"][0].bottom
            self.entries["Top"][0].x = corridor.entries["Bottom"][0].x
            self.entries["Top"][1] = True
            corridor.entries["Bottom"][1] = True
            
            if "Top" != self.main_entry[1]:
                self.main_entry[0].x = self.entries["Top"][0].x + self.relativity["Top"][0]
                self.main_entry[0].y = self.entries["Top"][0].y + self.relativity["Top"][1]
            
            self.update()
            return True

        return False
        
class Corridor:
    def __init__(self, id, corridor):
        self.id = id
        self.Corridor = corridor["objects"]["Corridor"][0]
        self.relativity = corridor["relativity"]
        self.range = corridor["range"]
        self.entry_count = corridor["entry_count"]
        self.main_entry = corridor["main_entry"]
        self.data = corridor["data"]
        self.entries = {}
        self.spikes = {}
        self.valid = True
        
        for obj_id in corridor["objects"]:
            if "Spike" in obj_id:
                self.spikes[obj_id] = corridor["objects"][obj_id][0]
            
            if obj_id in ["Left", "Right", "Top", "Bottom"]:
                if corridor["objects"][obj_id][0] == self.main_entry:
                    self.main_entry = [corridor["objects"][obj_id][0], obj_id]
                self.entries[obj_id] = [corridor["objects"][obj_id][0], False]
    
    def update(self):
        for e in self.entries:
            if e == self.main_entry[1]:
                continue
            self.entries[e][0].topleft = [self.main_entry[0].x - self.relativity[e][0], self.main_entry[0].y - self.relativity[e][1]]
        
        self.Corridor.x = self.main_entry[0].x - self.relativity["Corridor"][0]
        self.Corridor.y = self.main_entry[0].y - self.relativity["Corridor"][1]
        
        for s in self.spikes:
            self.spikes[s].topleft = [self.main_entry[0].x - self.relativity[s][0], self.main_entry[0].y - self.relativity[s][1]]
    
    def closed_off(self):
        e_count = 0
        for e in self.entries:
            if self.entries[e][1]:
                e_count += 1
        return (e_count == len(self.entries))
       
    def connect_to_room(self, entry, room):
        if entry == "Left" and ("Right" in self.entries):
            self.entries["Right"][0].right = room.entries["Left"][0].left
            self.entries["Right"][0].y = room.entries["Left"][0].y
            self.entries["Right"][1] = True
            room.entries["Left"][1] = True
            
            if "Right" != self.main_entry[1]:
                self.main_entry[0].x = self.entries["Right"][0].x + self.relativity["Right"][0]
                self.main_entry[0].y = self.entries["Right"][0].y + self.relativity["Right"][1]
            
            self.update()
            return True
        elif entry == "Right" and ("Left" in self.entries):
            self.entries["Left"][0].left = room.entries["Right"][0].right
            self.entries["Left"][0].y = room.entries["Right"][0].y
            self.entries["Left"][1] = True
            room.entries["Right"][1] = True
            
            if "Left" != self.main_entry[1]:
                self.main_entry[0].x = self.entries["Left"][0].x + self.relativity["Left"][0]
                self.main_entry[0].y = self.entries["Left"][0].y + self.relativity["Left"][1]
            
            self.update()
            return True
        elif entry == "Top" and ("Bottom" in self.entries):
            self.entries["Bottom"][0].bottom = room.entries["Top"][0].top
            self.entries["Bottom"][0].x = room.entries["Top"][0].x
            self.entries["Bottom"][1] = True
            room.entries["Top"][1] = True
            
            if "Bottom" != self.main_entry[1]:
                self.main_entry[0].x = self.entries["Bottom"][0].x + self.relativity["Bottom"][0]
                self.main_entry[0].y = self.entries["Bottom"][0].y + self.relativity["Bottom"][1]
            
            self.update()
            return True
        elif entry == "Bottom" and ("Top" in self.entries):
            self.entries["Top"][0].top = room.entries["Bottom"][0].bottom
            self.entries["Top"][0].x = room.entries["Bottom"][0].x
            self.entries["Top"][1] = True
            room.entries["Bottom"][1] = True
            
            if "Top" != self.main_entry[1]:
                self.main_entry[0].x = self.entries["Top"][0].x + self.relativity["Top"][0]
                self.main_entry[0].y = self.entries["Top"][0].y + self.relativity["Top"][1]
            
            self.update()
            return True

        return False
        
        
        

class World:
    def __init__(self, gm):
        self.gm = gm
        
        #generation variables
        self.level = {"tiles":[],  "decor":[], "walls":[]}
        self.game_world = {"rooms": [], "corridors":[]}
        self.current_rooms = []
        self.current_cs = []
        self.handling_corridors = True
        self.room_count = 0
        self.retry = False
        self.max_retries = 20
        self.retries = 0
        
        self.spawn_points = []
    
    def check_corridor_entry(self, corridor):
        direction = {"Left": [-10, 0], "Right": [10, 0], "Top": [0, -10], "Bottom": [0, 10]}
        for e in corridor.entries:
            rect = deepcopy(corridor.entries[e][0])
            rect.x += direction[e][0]
            rect.y += direction[e][1]
            
            valid_entries = []
            
            for r in self.game_world["rooms"]:
                if rect.colliderect(r.Room):
                    valid_entries.append(corridor.entries[e][0])
            
            
            if corridor.entries[e][0] not in valid_entries:
                corridor.entries[e][1] = False
    
    def replace_corridor(self, corridor):
        valid_entries = []
        for e in corridor.entries:
            if corridor.entries[e][1]:
                valid_entries.append(e)
        
        replaced = False
        while not replaced:
            c_id = random.choice(self.gm.assets.r_corridors[corridor.id.split(".")[0]])
            if c_id in self.gm.assets.rc_data:
                c = Corridor(c_id, deepcopy(self.gm.assets.rc_data[c_id]))
                if list(c.entries) == valid_entries:
                    c.Corridor = corridor.Corridor
                    for e in valid_entries:
                        c.entries[e] = corridor.entries[e]
                    return c
            else:
                print("break")
                break
            
    def check_room_entries(self, room):
        direction = {"Left": [-10, 0], "Right": [10, 0], "Top": [0, -10], "Bottom": [0, 10]}
        
        for e in room.entries:
            rect = deepcopy(room.entries[e][0])
            rect.x += direction[e][0]
            rect.y += direction[e][1]
            
            valid_entries = []
            valid_entry_ids = []
            
            for c in self.game_world["corridors"]:
                if rect.colliderect(c.Corridor):
                    valid_entries.append(room.entries[e][0])
            
            if room.entries[e][0] not in valid_entries:
                room.entries[e][1] = False
                #self.gm.test_entries2.append(room.entries[e][0])
            else:
                #self.gm.test_entries1.append(room.entries[e][0])
                pass
            
        
        for e in room.entries:
            if room.entries[e][1] == True:
                valid_entry_ids.append(e)
            
            #print(room.closed_off(), valid_entry_ids, room.entries)
                
        return [room.closed_off(), valid_entry_ids]
        
    
    def generate(self, count=2):
        room_ids = list(self.gm.assets.rooms.keys())
        c_ids = list(self.gm.assets.corridors.keys())
        
        if self.current_rooms == [] and self.current_cs == []:
            self.room_count = 1
            r_id = deepcopy(random.choice(room_ids))
            r = Room(r_id,self.gm.assets.rooms[r_id]) # Intitial room
            self.current_rooms = [r]
            self.current_cs = []
            
            self.handling_corridors = True
        
        self.retry = False
        
        while True:
            if self.handling_corridors:
                
                #print("Handling", self.current_rooms, self.current_cs)
                
                if self.room_count >= count:
                    print("Done")
                    print(self.room_count, count)
                    break
                
                if len(self.current_rooms) == 0 and len(self.current_cs) == 0:
                    print("Hmmm...")
                    self.retry = True
                    break
                
                if len(self.current_rooms) == 0:
                    self.handling_corridors = False
                    #break
                    continue
                
                
                if self.current_rooms[0].closed_off():
                    i = self.current_rooms.pop(0)
                    self.game_world["rooms"].append(i)
                    continue
                
                for e in self.current_rooms[0].entries:
                    if not self.current_rooms[0].entries[e][1]:
                        c_id = random.choice(c_ids)
                        c = Corridor(c_id, deepcopy(self.gm.assets.corridors[c_id]))
                        if c.connect_to_room(e, self.current_rooms[0]):
                            for room in (self.game_world["rooms"] + self.current_rooms):
                                if c.Corridor.colliderect(room.Room):
                                    c.valid = False
                            
                            for corr in (self.game_world["corridors"] + self.current_cs):
                                if c.Corridor.colliderect(corr.Corridor):
                                    c.valid = False
                            
                            if c.valid:
                                self.current_cs.append(c)
                        
            elif not self.handling_corridors:
                
                #print("Handling2", self.current_rooms, self.current_cs)
                
                if len(self.current_cs) == 0:
                    self.handling_corridors = True
                    #break
                    continue
                
                if self.current_cs[0].closed_off():
                    i = self.current_cs.pop(0)
                    self.game_world["corridors"].append(i)
                    self.room_count += 1
                    continue
                
                for e in self.current_cs[0].entries:
                    if not self.current_cs[0].entries[e][1]:
                        r_id = deepcopy(random.choice(room_ids))
                        room = Room(r_id, deepcopy(self.gm.assets.rooms[r_id]))
                        if room.connect_to_corridor(e, self.current_cs[0]):
                            for r in (self.game_world["rooms"] + self.current_rooms):
                                if room.Room.colliderect(r.Room):
                                    room.valid = False
                            
                            for corr in (self.game_world["corridors"] + self.current_cs):
                                if room.Room.colliderect(corr.Corridor):
                                    room.valid = False
                            
                            if room.valid:
                                self.current_rooms.append(room)
        
        if self.retry:
            self.retries += 1
            self.room_count = 0
            self.game_world["rooms"].clear()
            self.game_world["corridors"].clear()
            self.current_rooms = []
            self.current_cs = []
            self.handling_corridors = True
            return
        
        # Correction of the dungeon
        corridors = []
        for i, c in sorted(enumerate(self.game_world["corridors"])):
            self.check_corridor_entry(c)
            
            if len(c.entries) == 2 and c.closed_off() == False:
                continue
                
            if len(c.entries) == 3:
                closed = 0
                for e in c.entries:
                    if c.entries[e][1]:
                        closed += 1
                
                if c.closed_off() == False and closed == 1:
                    continue

            corridors.append(c)
            
        self.game_world["corridors"].clear()
        self.game_world["corridors"] = corridors
        
        for i, c in sorted(enumerate(self.game_world["corridors"])):  
            
            if len(c.entries) >= 3 and c.closed_off() == False:
                c = self.replace_corridor(c)
            
            tile_pos = [int(c.Corridor.x/self.gm.TILESIZE), int(c.Corridor.y/self.gm.TILESIZE)]
            for y in range(c.range[2], c.range[3]):
                for x in range(c.range[0], c.range[1]):
                    tile_id = f"{x}/{y}"
                    
                    i = -(c.range[1] - (x + (c.range[1]-c.range[0])))
                    j = -(c.range[3] - (y + (c.range[3]-c.range[2])))
                    new_pos = [tile_pos[0] + i, tile_pos[1] + j]
                    
                    for layer in c.data:
                        if tile_id in c.data[layer]:
                            tile = [c.data[layer][tile_id][0], new_pos]
                            
                            if tile[0] in [81, 82, 83, 84]:
                                img = self.gm.assets.tileset[tile[0]]
                                s = Spike(img, [new_pos[0]*self.gm.TILESIZE, new_pos[1]*self.gm.TILESIZE], tile[0])
                                self.gm.spikes.append(s)
                                continue

                            self.level[layer].append(tile)
            
            for s in c.spikes:
                spike = c.spikes[s]
                t = 81
                if s == "Spike D": 
                    t = 82  
                if s == "Spike L": 
                    t = 83  
                if s == "Spike R": 
                    t = 84 
                img = self.gm.assets.tileset[t]
                s = Spike(img, [spike.x, spike.y], t, "hidden")
                self.gm.spikes.append(s) 
                      
            self.gm.test_rects.append(c.Corridor)
            for e in c.entries:
                self.gm.test_rects.append(c.entries[e][0])
        
        for room in self.game_world["rooms"]:
            replace_info = self.check_room_entries(room)
            
            #print(replace_info)
            
            if replace_info[0] == False and len(replace_info[1]) > 0:
                replaced = False
                while not replaced:
                    #print("replacing", replace_info)
                    r_id = random.choice(self.gm.assets.replacements[room.id.split(".")[0]])
                    if r_id in self.gm.assets.replacement_data:
                        r = Room(r_id, deepcopy(self.gm.assets.replacement_data[r_id]))
                        if list(r.entries) == replace_info[1]:
                            #print(r.entries)
                            #print("Yeahhhhhhh!!!!")
                            r.Room = room.Room
                            r.spawn = room.spawn
                            r.trigger = room.trigger
                            for e in replace_info[1]:
                                r.entries[e] = room.entries[e]
                            room = r
                            replaced = True
                    else:
                        print("break")
                        break
            
            tile_pos = [int(room.Room.x/self.gm.TILESIZE), int(room.Room.y/self.gm.TILESIZE)]
            for y in range(room.range[2], room.range[3]):
                for x in range(room.range[0], room.range[1]):
                    tile_id = f"{x}/{y}"
                    
                    i = -(room.range[1] - (x + (room.range[1]-room.range[0])))
                    j = -(room.range[3] - (y + (room.range[3]-room.range[2])))
                    new_pos = [tile_pos[0] + i, tile_pos[1] + j]
                    
                    for layer in room.data:
                        if tile_id in room.data[layer]:
                            tile = [room.data[layer][tile_id][0], new_pos]
                            
                            if tile[0] in [81, 82, 83, 84]:
                                img = self.gm.assets.tileset[tile[0]]
                                s = Spike(img, [new_pos[0]*self.gm.TILESIZE, new_pos[1]*self.gm.TILESIZE], tile[0])
                                self.gm.spikes.append(s)
                                continue

                            self.level[layer].append(tile)
            
            
            for s in room.spikes:
                spike = room.spikes[s]
                t = 81
                if s == "Spike D": 
                    t = 82  
                if s == "Spike L": 
                    t = 83  
                if s == "Spike R": 
                    t = 84 
                img = self.gm.assets.tileset[t]
                s = Spike(img, [spike.x, spike.y], t, "hidden")
                self.gm.spikes.append(s) 
            
            self.spawn_points.append(room.spawn)
            self.gm.test_rects.append(pygame.Rect(room.spawn[0], room.spawn[1], 16, 16))
            
            self.gm.test_rects.append(room.Room)
            for e in room.entries:
                self.gm.test_rects.append(room.entries[e][0])
        