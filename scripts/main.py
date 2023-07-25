import modules.scripts as scripts
import gradio as gr

from modules import script_callbacks
from modules.ui_components import FormRow, ToolButton

class RatioLock(scripts.Script):
    detect_ratio_symbol = '\U0001F50D' # 
    image_ratios = {
        "None": None,
        "1:1 - Square": 1.0,
        "4:3 - Standard": 4/3,
        "16:9 - Widescreen": 16/9,
        "3:2 - Classic": 3/2,
        "5:4 - Medium Format": 5/4,
        "3:1 - Panorama": 3/1,
        "8:10 - Portrait": 8/10,
        "2:1 - Cinemascope": 2.0,
        "9:16 - Vertical Video": 9/16,
        "21:9 - Ultrawide": 21/9
    }

    # Slider controls from A1111 WebUI.
    txt2img_w_slider = None
    txt2img_h_slider = None
    img2img_w_slider = None
    img2img_h_slider = None

    # Our controls
    txt2img_dims_ratio = gr.Dropdown(list(image_ratios.keys()), value="None", label="Image Ratio", elem_id="txt2img_dims_ratio")
    txt2img_dims_detect = ToolButton(value=detect_ratio_symbol, elem_id="txt2img_dims_detect", label="Detect dims")
    img2img_dims_ratio = gr.Dropdown(list(image_ratios.keys()), value="None", label="Image Ratio", elem_id="img2img_dims_ratio")
    img2img_dims_detect = ToolButton(value=detect_ratio_symbol, elem_id="img2img_dims_detect", label="Detect dims")
    
    def __init__(self):
        self.width = None
        self.height = None
        
    # The title of the script. This is what will be displayed in the dropdown menu.
    def title(self):
        return "Ratio Lock"
    
    # Determines when the script should be shown in the dropdown menu via the 
    # returned value. As an example:
    # is_img2img is True if the current tab is img2img, and False if it is txt2img.
    # Thus, return is_img2img to only show the script on the img2img tab.
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    # How the script's is displayed in the UI. See https://gradio.app/docs/#components
    # for the different UI components you can use and how to create them.
    # Most UI components can return a value, such as a boolean for a checkbox.
    # The returned values are passed to the run method as parameters.
    def ui(self, is_img2img):
        # not sure where else to put this, assumes these items are built first 
        # based on where scripts display in page    
        if not is_img2img:
            dims_ratio = self.txt2img_dims_ratio
            dims_detect = self.txt2img_dims_detect
            self.width = self.txt2img_w_slider
            self.height = self.txt2img_h_slider
        else:
            dims_ratio = self.img2img_dims_ratio
            dims_detect = self.img2img_dims_detect
            self.width = self.img2img_w_slider
            self.height = self.img2img_h_slider
        
        width_change_event = self.width.change(fn=self.width_change, inputs=[dims_ratio, self.width, self.height], outputs=[self.height], show_progress=False)
        
        # height_change_event = self.txt2img_h_slider.change(fn=height_change, inputs=[dims_ratio, width, height], outputs=[width], show_progress=False, cancels=[width_change_event])
        dims_ratio.change(fn=self.on_dims_ratio, inputs=[dims_ratio, self.width, self.height], outputs=[self.height])
        dims_detect.click(fn=self.on_dims_detect, inputs=[self.width, self.height], outputs=[dims_ratio])

        return []
    
    def width_change(self, ratio, width, height):
        ratio = self.image_ratios[ratio]
        return round(width/ratio) if ratio else height

    def height_change(ratio, width, height):
        ratio = RatioLock.image_ratios[ratio]
        return round(height * ratio) if ratio else width

    def on_dims_ratio(self, ratio, width, height):
        ratio = self.image_ratios[ratio]
        if ratio:
            height = round(width / ratio)
        return height
    
    def on_dims_detect(self, width, height):
        for key, ratio in self.image_ratios.items():
            if ratio is not None and abs(ratio - (width / height)) < 0.001:
                return key
        return "None"

    @staticmethod
    def on_before_component(component, **_kwargs):
        elem_id = _kwargs.get('elem_id')

        if elem_id == "txt2img_cfg_scale":
            with gr.Row():
                RatioLock.txt2img_dims_ratio.render()
                RatioLock.txt2img_dims_detect.render()

        if elem_id == "img2img_cfg_scale":
            with gr.Row():
                RatioLock.img2img_dims_ratio.render()
                RatioLock.img2img_dims_detect.render()
                                         
    @staticmethod
    def on_after_component(component, **_kwargs):
        elem_id = getattr(component, "elem_id", None)
        
        if elem_id == "txt2img_width":
            RatioLock.txt2img_w_slider = component
            return

        if elem_id == "txt2img_height":
            RatioLock.txt2img_h_slider = component
            return

        if elem_id == "img2img_width":
            RatioLock.img2img_w_slider = component
            return

        if elem_id == "img2img_height":
            RatioLock.img2img_h_slider = component
            return
        
script_callbacks.on_before_component(RatioLock.on_before_component)
script_callbacks.on_after_component(RatioLock.on_after_component)