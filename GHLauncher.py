import dearpygui.dearpygui as dpg
import platform 
import os

class globals:
    if platform.system() == "Darwin":
        VIEWPORT_WIDTH = 1000
        VIEWPORT_HEIGHT = 600
    if platform.system() == "Windows":
        VIEWPORT_WIDTH = 1400
        VIEWPORT_HEIGHT = 800
    
dpg.create_context()
dpg.create_viewport(title='GHLauncher', width=globals.VIEWPORT_WIDTH, height=globals.VIEWPORT_HEIGHT)

class Thumbnail_props:
    def __init__(self,path,tag,game_name):
        self.path = path 
        self.tag = tag
        self.game_name = game_name
        self.load_image = dpg.load_image(self.path)
        self.width = self.load_image[0]
        self.height = self.load_image[1]
        self.channels = self.load_image[2]
        self.data = self.load_image[3]
        
thumbnails = []
kart_shifters_thumbnail = Thumbnail_props("Kart-Shifters-Poster-1.png","pic1","Kart Shifters")
basketball_thumbnail = Thumbnail_props("Screen-Shot-2024-03-05-at-10.50.37-AM.png","pic2","Stick Basketball")
bbal_thumbnail = Thumbnail_props("bball-thumbnail-1.png","pic","B-Ball")
thumbnails.extend([kart_shifters_thumbnail,basketball_thumbnail,bbal_thumbnail])

dpg.set_global_font_scale(1.2)
with dpg.window(pos=(0,0),width=globals.VIEWPORT_WIDTH,height=globals.VIEWPORT_HEIGHT,no_move=True,no_title_bar=True,no_resize=True,no_bring_to_front_on_focus=True) as background_window:
    dpg.create_context()
    with dpg.window(pos=(0,0),width=220,height=globals.VIEWPORT_HEIGHT,no_move=True,no_title_bar=True,no_resize=True)as side_menu:
        dpg.add_text("GHLauncher")
        dpg.add_separator()
        dpg.add_spacer(height=30)
        dpg.add_button(label="WHAT'S NEW")
        dpg.add_button(label="CATELOG")
        dpg.add_button(label="ACHIVEMENTS")
        dpg.add_button(label="SETTINGS")
        dpg.add_button(label="VISIT OUR WEBSITE")

    with dpg.texture_registry(show=False):
        for thumbnail in thumbnails:
            dpg.add_static_texture(width=thumbnail.width,height=thumbnail.height,default_value=thumbnail.data,tag=thumbnail.tag)

    def openApp(sender, app_data, user_data):
        os.system(f"open {user_data}")

    with dpg.child_window(label="WHAT'S NEW",pos=(220,0),tag="whats_new_window") as whats_new_window:
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            for thumbnail in thumbnails:
                dpg.add_spacer(width=60)
                with dpg.group():
                    dpg.add_image(thumbnail.tag,width=150,height=200)
                    dpg.add_spacer(height=10)                    
                    dpg.add_button(label=thumbnail.game_name,callback=openApp,user_data=thumbnail.path)
                   
        dpg.add_spacer(height=20)
        dpg.add_separator()
    
        
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

