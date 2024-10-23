import os

class Desert_planet():

    path = str(os.path.normpath("assets\desert_planet_assets"))

    map_tiles = { 
        "path" : str(os.path.join(path,"desert_sandtiles")),
        "normal_tiles" : list(os.listdir(os.path.join(path,"desert_sandtiles")))[0], 
        "dig_tiles" : list(os.listdir(os.path.join(path,"desert_sandtiles")))[1:],
        
    }

    rock_assets = {
        "path" : os.path.join(path,"desert_rocks"),
        "rocks" : list(os.listdir(os.path.join(path,"desert_rocks"))),
        "item" : "Sand Rock",
        "description" : ("Naturally occurring solid made up of a mineral like substance"),
    }

    grass_assets = {
        "path" : os.path.join(path,"desert_grass"),
        "grass" : list(os.listdir(os.path.join(path,"desert_grass"))),
        "item" : "Dried Grass",
        "description" : "Plant with slender blades",
    }

    bush_assets = {
        "path" : os.path.join(path,"desert_bushes"),
        "bushes" : list(os.listdir(os.path.join(path,"desert_bushes"))),
        "item" : "Dried Bush",
        "description": "Wooded dried plant with short branches"
    }


