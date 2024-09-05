import dearpygui.dearpygui as dpg
import platform 

class globals:
    if platform.system() == "Darwin":
        VIEWPORT_WIDTH = 1000
        VIEWPORT_HEIGHT = 600
    if platform.system() == "Windows":
        VIEWPORT_WIDTH = 1400
        VIEWPORT_HEIGHT = 1000
    
dpg.create_context()
dpg.create_viewport(title='GHLauncher', width=globals.VIEWPORT_WIDTH, height=globals.VIEWPORT_HEIGHT)

class Thumbnail_props:
    def __init__(self,path,tag):
        self.path = path 
        self.tag = tag
        self.load_image = dpg.load_image(self.path)
        self.width = self.load_image[0]
        self.height = self.load_image[1]
        self.channels = self.load_image[2]
        self.data = self.load_image[3]

thumbnails = []
kart_shifters_thumbnail = Thumbnail_props("Kart Shifters Poster-1.png.png","pic1")
basketball_thumbnail = Thumbnail_props("Screen Shot 2024-03-05 at 10.50.37 AM.png","pic2")
new_thumbnail = Thumbnail_props("Screen Shot 2024-03-05 at 10.51.43 AM.png","pic")
thumbnails.extend([kart_shifters_thumbnail,basketball_thumbnail,new_thumbnail])


dpg.set_global_font_scale(1.2)
with dpg.window(pos=(0,0),width=globals.VIEWPORT_WIDTH,height=globals.VIEWPORT_HEIGHT,no_move=True,no_title_bar=True,no_resize=True,no_bring_to_front_on_focus=True) as background_window:
    dpg.create_context()
    with dpg.window(pos=(0,0),width=220,height=globals.VIEWPORT_HEIGHT,no_move=True,no_title_bar=True,no_resize=True)as side_menu:
        dpg.add_text("GHLauncher")
        dpg.add_separator()
        dpg.add_spacer(height=30)
        dpg.add_button(label="WHAT'S NEW")
        dpg.add_button(label="CATELOG")
        dpg.add_button(label="VISIT OUR WEBSITE")
        dpg.add_button(label="SETTINGS")

    with dpg.texture_registry(show=False):
        for thumbnail in thumbnails:
            dpg.add_static_texture(width=thumbnail.width,height=thumbnail.height,default_value=thumbnail.data,tag=thumbnail.tag)

    with dpg.child_window(label="Tutorial",tag="mm",pos=(220,0)) as whats_new_window :
        for thumbnail in thumbnails:
            dpg.add_image(thumbnail.tag,width=150,height=200)
            dpg.add_separator()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

"""

import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=800, height=600)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()"""