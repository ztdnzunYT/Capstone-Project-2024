import os
import random



class Player_animations():
    path = os.path.normpath("xzplore\\assets\\player_animations")

    player_assests = {

        #"idle" :  sorted(list(os.listdir(os.path.join(path,"desert_sandtiles")))),
        "up_walk_path" : os.path.normpath(os.path.join(path,"player_up")),
        "up_idle" : os.path.normpath(os.path.join(path,"player_up_idle"))+".png",
        "up_walk" : sorted(list(os.listdir(os.path.join(path,"player_up")))),

        "down_walk_path" : os.path.normpath(os.path.join(path,"player_down")),
        "down_idle" : os.path.normpath(os.path.join(path,"player_down_idle"))+".png",
        "down_walk" :  sorted(list(os.listdir(os.path.join(path,"player_down")))),

        "left_walk_path" : os.path.normpath(os.path.join(path,"player_left")),
        "left_idle" : os.path.normpath(os.path.join(path,"player_left_idle"))+".png",
        "left_walk" :  sorted(list(os.listdir(os.path.join(path,"player_left")))),

        "right_walk_path" : os.path.normpath(os.path.join(path,"player_right")),
        "right_idle" : os.path.normpath(os.path.join(path,"player_right_idle"))+".png",
        "right_walk" :  sorted(list(os.listdir(os.path.join(path,"player_right")))),

    }

class Clouds():

    path = str(os.path.normpath("xzplore/assets"))

    clouds_assets = { 
        "path" : str(os.path.join(path,"cloud_shadows")),
        "clouds" : sorted(list(os.listdir(os.path.join(path,"cloud_shadows")))), 
    }


class Desert_planet():

    path = str(os.path.normpath("xzplore/assets/desert_planet_assets"))

    map_tiles = { 
        "path" : str(os.path.join(path,"desert_sandtiles")),
        "normal_tiles" : sorted(list(os.listdir(os.path.join(path,"desert_sandtiles"))))[0], 
        "dig_tiles" : sorted(list(os.listdir(os.path.join(path,"desert_sandtiles"))))[1:],
        
    }

    rock_assets = {
        "path" : os.path.join(path,"desert_rocks"),
        "rocks" : sorted(list(os.listdir(os.path.join(path,"desert_rocks")))),
        "item" : "Sand Rock",
        "description" : ("Naturally occurring solid made up of a mineral like substance"),
    }

    grass_assets = {
        "path" : os.path.join(path,"desert_grass"),
        "grass" : sorted(list(os.listdir(os.path.join(path,"desert_grass")))),
        "item" : "Dried Grass",
        "description" : "Plant with dried slender blades",
    }

    bush_assets = {
        "path" : os.path.join(path,"desert_bushes"),
        "bushes" : sorted(list(os.listdir(os.path.join(path,"desert_bushes"))))[2:],
        "item" : "Dried Bush",
        "description": "Wooded dried plant with short branches"
    }

    desert_worms = {
        "enemy" : "Desert Worm",
        "description" :  "Toxic parasite found in desert regions",
        "path" : "xzplore/assets/desert_worm",
        "animations" : sorted(os.listdir("xzplore/assets/desert_worm")) 

    }

class Colletibles():

    collectible_items = {
        "fossil_path" : os.path.normpath("xzplore/assets/fossils"),
        "fossils" : os.listdir(os.path.normpath("xzplore/assets/fossils")),
        "random_fossil" : random.choice(os.listdir(os.path.normpath("xzplore/assets/fossils")))
    }

    malachite = { 
        "item" : "Malachite",
        "description" : "Vivid green gemstone with swirling banded patterns and smooth, glossy finish", 
        "image" : "xzplore/assets/gems/malachite.png"
    }

    quartz = { 
        "item" : "Quartz",
        "description" : "Clear to milky white gemstone with hexagonal shapes and a glassy luster", 
        "image" : "xzplore/assets/gems/quartz.png"
    }

    agate = { 
        "item" : "Agate",
        "description" : "Banded gemstone with smooth layers of color, typically in earthy tones",
        "image" : "xzplore/assets/gems/agate.png"
    }
    opal = { 
        "item" : "Opal",
        "description" : "Colorful gemstone with shifting hues and a translucent to opaque look",
        "image" : "xzplore/assets/gems/opal.png"
    }
    topaz = { 
        "item" : "Topaz",
        "description" : "Transparent gemstone often showcasing a brilliant luster and clarity",
        "image" : "xzplore/assets/gems/topaz.png"
    }
    peridot = { 
        "item" : "Peridot",
        "description" : "Vibrant green gemstone known for its distinctive olive hue and clarity",
        "image" : "xzplore/assets/gems/peridot.png"
    }
    arizona = { 
        "item" : "Arizona",
        "description" : "Unique stone like turquoise, known for its striking blue color",
        "image" : "xzplore/assets/gems/arizona.png"
    }
    obsidian = { 
        "item" : "Obsidian",
        "description" : "Volcanic black glass with shiny surface and sharp edges",
        "image" : "xzplore/assets/gems/obsidian.png"
    }

    chrysocolla ={ 
        "item" : "Chrysocolla",
        "description" : "Vibrant blue-green mineral with smooth, waxy luster mottled patterns",
        "image" : "xzplore/assets/gems/chrysocolla.png"
    }

    petrified_wood = { 
        "item" : "Petrified Wood",
        "description" : "Fossilized tree remains that display wood-like patterns",
        "image" : "xzplore/assets/gems/petrified_wood.png"
    }

    turquoise = { 
        "item" : "Turquoise",
        "description" : "Blue-green mineral with unique matrix patterns and polished surface",
        "image" : "xzplore/assets/gems/turquoise.png"
    }

    garnet = { 
        "item" : "Garnet",
        "description" : "Red gemstone known for its brilliance and vitreous luster",
        "image" : "xzplore/assets/gems/garnet.png"
    }



    desert_collectibles = [turquoise,quartz,opal,peridot,agate,garnet]





print(os.path.normpath(Colletibles.malachite["image"]))


















print(Colletibles.collectible_items["fossil_path"])
