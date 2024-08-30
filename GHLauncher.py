import dearpygui.dearpygui as dpg
import platform 

class globals:
    if platform.system() == "Darwin":
        VIEWPORT_WIDTH = 1000
        VIEWPORT_HEIGHT = 600
    elif platform.system() == "Windows":
        VIEWPORT_WIDTH = 1250
        VIEWPORT_HEIGHT = 850

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=1000, height=600)

with dpg.window(label="Example Window"):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)





dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()