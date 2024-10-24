import os




class Player_animations():
    path = os.path.normpath("xzplore/assets/player_animations")

    player_assests = {

        #"idle" :  sorted(list(os.listdir(os.path.join(path,"desert_sandtiles")))),
        "up_walk_path" : os.path.normpath(os.path.join(path,"player_up")),
        "up_walk" : sorted(list(os.listdir(os.path.join(path,"player_up")))),
        "down_walk_path" : os.path.normpath(os.path.join(path,"player")),
        "down_walk" :  sorted(list(os.listdir(os.path.join(path,"player_down")))),
        "left_walk" :  sorted(list(os.listdir(os.path.join(path,"player_left")))),
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


