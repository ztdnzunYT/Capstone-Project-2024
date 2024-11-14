import dearpygui.dearpygui as dpg
import platform 
import os
import pathlib
import subprocess

class globals:
    if platform.system() == "Darwin":
        VIEWPORT_WIDTH = 1000
        VIEWPORT_HEIGHT = 600
    if platform.system() == "Windows":
        VIEWPORT_WIDTH = 1400
        VIEWPORT_HEIGHT = 800
    
dpg.create_context()
dpg.create_viewport(title='GHLauncher', width=globals.VIEWPORT_WIDTH, height=globals.VIEWPORT_HEIGHT,resizable=False)

class Thumbnail_props:
    def __init__(self,path,tag,game_name,game_path):
        self.path = path 
        self.tag = tag
        self.game_name = game_name
        self.game_path = game_path
        self.load_image = dpg.load_image(self.path)
        self.width = self.load_image[0]
        self.height = self.load_image[1]
        self.channels = self.load_image[2]
        self.data = self.load_image[3]

        
thumbnails = []
xzplore_thumbnail = Thumbnail_props("Assets/Thumbnails/xzplore.png","pic1","Xzplore",None)
dungeon_survival_thumbnail = Thumbnail_props("Assets/Thumbnails/Dungeon_surviver.png","pic2","Dungeoun Survival","Necromancer.exe")
bbal_thumbnail = Thumbnail_props("Assets/Thumbnails/bball-thumbnail.png","pic3","B-Ball","B-Ball.exe")
pickle_jump_thumbnail = Thumbnail_props("Assets/Thumbnails/Pickle-jump.png","pic4","Pickle Jump",None)
fighterz_thumbnail = Thumbnail_props("Assets/Thumbnails/FIGHTERZ.png","pic5","FighterZ",None)
kart_shifters_thumbnail = Thumbnail_props("Assets/Thumbnails/Kart-Shifters-Poster-1.png","pic6","Kart Shifters","Kart_shifters.exe")

thumbnails.extend([xzplore_thumbnail,dungeon_survival_thumbnail,bbal_thumbnail,pickle_jump_thumbnail,fighterz_thumbnail,kart_shifters_thumbnail])

dpg.set_global_font_scale(1.2)
with dpg.window(pos=(0,0),width=globals.VIEWPORT_WIDTH,height=globals.VIEWPORT_HEIGHT,no_move=True,no_title_bar=True,no_resize=True,no_bring_to_front_on_focus=True) as background_window:
    dpg.create_context()
    with dpg.window(pos=(0,0),width=220,height=globals.VIEWPORT_HEIGHT,no_move=True,no_title_bar=True,no_resize=True)as side_menu:
        dpg.add_text("GHLauncher")
        dpg.add_separator()
        dpg.add_spacer(height=30)
        dpg.add_button(label="WHAT'S NEW")
        dpg.add_button(label="CATALOG")
        dpg.add_button(label="ACHIVEMENTS")
        dpg.add_button(label="SETTINGS")
        dpg.add_button(label="VISIT OUR WEBSITE")

    with dpg.texture_registry(show=False):
        for thumbnail in thumbnails:
            dpg.add_static_texture(width=thumbnail.width,height=thumbnail.height,default_value=thumbnail.data,tag=thumbnail.tag)

    def openApp(sender, app_data, user_data):
        #subprocess.call(["C:/Users/348580/Download/Kart_shifters/Kart_shifters.exe"])
        os.startfile(os.path.abspath(user_data))

    with dpg.child_window(label="WHAT'S NEW",pos=(220,0),tag="whats_new_window") as whats_new_window:
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            for thumbnail in thumbnails[:5]:
                dpg.add_spacer(width=60)
                with dpg.group():
                    dpg.add_image(thumbnail.tag,width=150,height=200)
                    dpg.add_spacer(height=10)                    
                    dpg.add_button(label=thumbnail.game_name,callback=openApp,user_data=thumbnail.game_path)
        dpg.add_spacer(height=20)

        with dpg.group(horizontal=True):
            for thumbnail in thumbnails[5:]:
                dpg.add_spacer(width=60)
                with dpg.group():
                    dpg.add_image(thumbnail.tag,width=150,height=200)
                    dpg.add_spacer(height=10)                    
                    dpg.add_button(label=thumbnail.game_name,callback=openApp,user_data=thumbnail.game_path)
        dpg.add_spacer(height=20)
        dpg.add_separator()
    
        
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
