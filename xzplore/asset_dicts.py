import os


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


