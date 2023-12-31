import pygame
import scripts.Engine as E
import os
import json
import random

sfx_path = "data/audio/sfx"
music_path = "data/images/music"

class Assets:
    def __init__(self, cwd):
        # Variables that are dictionaries to store different types of assets
        self.tileset = {}
        self.images = {}
        self.sound_effects = {}
        self.music = {}
        self.animations = {"fire":{}, "water":{}, "lightning":{}}
        self.spells = {"fire":{"attack":[[3], []], "fireball":[[5], []], "flame_slash":[[1], []], "flame_thrower":[[5], []]}, 
                       "water":{"attack":[[3], []], "drown":[[4], []], "ice_spike": [[1], []], "ice_wall": [[4], []], "splash": [[2], []], "water_arrow": [[5], []]}, 
                       "lightning":{"attack":[[3], []]}
                       }
        
        
        self.rooms = {}
        self.corridors = {}
        
        self.replacements = {}
        self.replacement_data = {}
        
        self.r_corridors = {}
        self.rc_data = {}
        
        self.cwd = cwd +'/'
        
        self.load_rooms()
        self.load_tileset()
        self.load_animations()
        self.load_spells()
        
    def load_rooms(self):
        path = "data/rooms"
        file_list = os.listdir(path)
        replacement_list = os.listdir("data/replacements")
        
        for item in file_list:
            file = open(path + "/" + item, "r")
            data = json.load(file)
            del data["tilesets"]
            file.close()
            
            if "room" in item:
                objects = {}
                
                self.replacements[item.split(".")[0]] = []
                
                for obj_id in data["objects"]:
                    obj = data["objects"][obj_id]
                    
                    objects[obj_id] = [pygame.Rect(obj[0], obj[1], obj[2], obj[3]), obj[4]]

                data["objects"] = objects
                rect = data["objects"]["Room"][0]
                data["range"] = [int(rect.left/16), int(rect.right/16), int(rect.top/16), int(rect.bottom/16)]
                
                data["relativity"] = {}
                data["entry_count"] = 0
                data["main_entry"] = None
                
                entry = None
                for obj_id in data["objects"]:
                    if obj_id in ["Left", "Right", "Top", "Bottom"]:
                        data["entry_count"] += 1
                        if entry == None:
                            entry = data["objects"][obj_id][0]
                            data["main_entry"] = entry
                    
                for obj_id in data["objects"]:
                    data["relativity"][obj_id] = [data["main_entry"].x - data["objects"][obj_id][0].x, data["main_entry"].y - data["objects"][obj_id][0].y]   
                    
                self.rooms[item] = data
                
            if "corridor" in item:
                objects = {}
                
                self.r_corridors[item.split('.')[0]] = []
                
                for obj_id in data["objects"]:
                    obj = data["objects"][obj_id]
                    
                    objects[obj_id] = [pygame.Rect(obj[0], obj[1], obj[2], obj[3]), obj[4]]

                data["objects"] = objects
                rect = data["objects"]["Corridor"][0]
                data["range"] = [int(rect.left/16), int(rect.right/16), int(rect.top/16), int(rect.bottom/16)]
                
                data["relativity"] = {}
                data["entry_count"] = 0
                data["main_entry"] = None
                
                entry = None
                for obj_id in data["objects"]:
                    if obj_id in ["Left", "Right", "Top", "Bottom"]:
                        data["entry_count"] += 1
                        if entry == None:
                            entry = data["objects"][obj_id][0]
                            data["main_entry"] = entry
                    
                for obj_id in data["objects"]:
                    data["relativity"][obj_id] = [entry.x - data["objects"][obj_id][0].x, entry.y - data["objects"][obj_id][0].y]

                self.corridors[item] = data
        
        for item in replacement_list:
            file = open("data/replacements/" + item, "r")
            data = json.load(file)
            del data["tilesets"]
            file.close()
            
            if "room" in item:
                objects = {}
                
                for obj_id in data["objects"]:
                    obj = data["objects"][obj_id]
                    
                    objects[obj_id] = [pygame.Rect(obj[0], obj[1], obj[2], obj[3]), obj[4]]

                data["objects"] = objects
                rect = data["objects"]["Room"][0]
                data["range"] = [int(rect.left/16), int(rect.right/16), int(rect.top/16), int(rect.bottom/16)]
                
                data["relativity"] = {}
                data["entry_count"] = 0
                data["main_entry"] = None
                
                entry = None
                for obj_id in data["objects"]:
                    if obj_id in ["Left", "Right", "Top", "Bottom"]:
                        data["entry_count"] += 1
                        if entry == None:
                            entry = data["objects"][obj_id][0]
                            data["main_entry"] = entry
                    
                for obj_id in data["objects"]:
                    data["relativity"][obj_id] = [entry.x - data["objects"][obj_id][0].x, entry.y - data["objects"][obj_id][0].y]   
                    
                self.replacement_data[item] = data
                
            if "corridor" in item:
                objects = {}
                
                for obj_id in data["objects"]:
                    obj = data["objects"][obj_id]
                    
                    objects[obj_id] = [pygame.Rect(obj[0], obj[1], obj[2], obj[3]), obj[4]]

                data["objects"] = objects
                rect = data["objects"]["Corridor"][0]
                data["range"] = [int(rect.left/16), int(rect.right/16), int(rect.top/16), int(rect.bottom/16)]
                
                data["relativity"] = {}
                data["entry_count"] = 0
                data["main_entry"] = None
                
                entry = None
                for obj_id in data["objects"]:
                    if obj_id in ["Left", "Right", "Top", "Bottom"]:
                        data["entry_count"] += 1
                        if entry == None:
                            entry = data["objects"][obj_id][0]
                            data["main_entry"] = entry
                    
                for obj_id in data["objects"]:
                    data["relativity"][obj_id] = [entry.x - data["objects"][obj_id][0].x, entry.y - data["objects"][obj_id][0].y]

                self.rc_data[item] = data
        
        remove_list = []
        for replacement_id in self.replacements:
            for file in replacement_list:
                if replacement_id in file:
                    self.replacements[replacement_id].append(file)

            if len(self.replacements[replacement_id]) == 0:
                remove_list.append(replacement_id)
        
        for r in remove_list:
            del self.replacements[r]
            
        remove_list = []
        for replacement_id in self.r_corridors:
            for file in replacement_list:
                if replacement_id in file:
                    self.r_corridors[replacement_id].append(file)

            if len(self.r_corridors[replacement_id]) == 0:
                remove_list.append(replacement_id)
        
        for r in remove_list:
            del self.r_corridors[r]
        
    def load_animations(self):
        anim_list = os.listdir("data/images/animations/player")
        p_anims = ["idle", "run", "jump", "wall_slide", "dash", "attack"]
        
        for a in anim_list:
            for anim in p_anims:
                path = "data/images/animations/player" + "/" + a + "/" + anim
                self.animations[a][anim] = []
                
                for i in range(len(os.listdir(path))):
                    img_path = f"{path}/{anim}{i+1}.png"
                    self.animations[a][anim].append(E.ImageManager.load(img_path, (0, 0, 0)))
        
        self.animations["fountain"] = []
        self.animations["torch"] = []
        for i in range(8):
            path = "data/images/animated_tiles/fountain/fountain" + str(i+1) + ".png"
            self.animations["fountain"].append(E.ImageManager.load(path, (0, 0, 0))) 
        for i in range(8):
            path = "data/images/animated_tiles/torch/torch" + str(i+1) + ".png"
            self.animations["torch"].append(E.ImageManager.load(path, (0, 0, 0))) 
        
        images, ids = E.ImageManager.load_folder("data/images", return_ids=True)
        
        for i in range(len(ids)):
            self.images[ids[i].split(".")[0]] = images[i]
            
    def load_tileset(self):
        tileset = E.ImageManager.load("data/images/tileset.png", (0, 0, 0))
        w = tileset.get_width()
        h = tileset.get_height()
        tilesize = 16
        tile_index = 1
        
        for i in range(int(h/tilesize)):
            for j in range(int(w/tilesize)):
                section = [j*tilesize, i*tilesize, tilesize, tilesize]
                img = E.ImageManager.get_image(tileset, section[0], section[1], section[2], section[3], 1)
                self.tileset[tile_index] = img
                
                tile_index += 1
        
        with open("data/images/decor_tileset.tset") as file:
            load_data = json.load(file)
            path = load_data["path"]
            file.close()
        
        
        tileset = E.ImageManager.load(path, load_data["colorkey"])
        w = tileset.get_width()
        h = tileset.get_height()
        
        for tile_id in load_data["tiles"]:
            tile = load_data["tiles"][tile_id]
            img = E.ImageManager.get_image(tileset, tile[0], tile[1], tile[2], tile[3], 1)
            self.tileset[tile_id] = img 
    
    def load_spells(self):
        # Fire spells
        img_list = {"fire": os.listdir("data/images/spells/fire"), "water": os.listdir("data/images/spells/water"), "lightning": os.listdir("data/images/spells/lightning")}
        
        for spell_type in self.spells:
            for spell in self.spells[spell_type]:
                num = 6
                if spell == "attack":
                    num = 6
                if spell == "fireball":
                    num = 3
                if spell == "flame_slash":
                    num = 5
                if spell == "flame_thrower":
                    num = 14
                if spell == "drown":
                    num = 10
                if spell == "ice_spike":
                    num = 1
                if spell == "ice_wall":
                    num = 12
                if spell == "splash":
                    num = 9
                if spell == "water_arrow":
                    num = 11
                    
                
                for i in range(num):
                    img = f"{spell}{i+1}.png"
                        
                    image = E.ImageManager.load(f"data/images/spells/{spell_type}/{img}", (0, 0, 0))
                    if spell == "fireball":
                        image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
                    if spell == "drown":
                        image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
                        image.set_alpha(180)
                    self.spells[spell_type][spell][1].append(image)
            
                self.spells[spell_type][spell][0] = self.spells[spell_type][spell][0] * len(self.spells[spell_type][spell][1])

    def modify_image(self, img_id, scale=0, colorkey=(0, 0, 0)):
        if scale != 0:
            self.images[img_id] = pygame.transform.scale(self.images[img_id], (scale, scale))
        
        if colorkey != (0, 0, 0):
            self.images[img_id].set_colorkey(colorkey)



