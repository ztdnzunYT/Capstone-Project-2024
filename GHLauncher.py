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


dpg.show_style_editor()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
