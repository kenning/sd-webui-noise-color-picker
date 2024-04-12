import random

import gradio as gr
import numpy as np
import modules.scripts as scripts
from modules import devices, processing

from PIL import Image


class Script(scripts.Script):

    def __init__(self):
        self.scalingW = 0
        self.scalingH = 0
        self.hr_denoise = 0
        self.hr_steps = 0
        self.scaler = ""

    def title(self):
        return "Fast Alternate Init Noise"

    def show(self, is_img2img):
        if not is_img2img:
            return scripts.AlwaysVisible
        return False

    def ui(self, is_img2img):

        with gr.Accordion("Noise Color Picker", open=False):
            enabled = gr.Checkbox(label="Enabled", default=False)

            denoising = gr.Slider(
                minimum=0.0,
                maximum=1.0,
                step=0.01,
                label="Denoising strength",
                value=0.9,
                elem_id=self.elem_id("denoising"),
            )

            with gr.Accordion("Color Adjustments", open=False):
                with gr.Row():
                    val_min = gr.Slider(
                        minimum=-1,
                        maximum=255,
                        step=1,
                        value=-1,
                        label="Brightness Min",
                        elem_id=self.elem_id("plasma_val_min"),
                    )
                    val_max = gr.Slider(
                        minimum=-1,
                        maximum=255,
                        step=1,
                        value=-1,
                        label="Brightness Max",
                        elem_id=self.elem_id("plasma_val_max"),
                    )
                with gr.Row():
                    red_min = gr.Slider(
                        minimum=-1,
                        maximum=255,
                        step=1,
                        value=-1,
                        label="Red Min",
                        elem_id=self.elem_id("plasma_red_min"),
                    )
                    red_max = gr.Slider(
                        minimum=-1,
                        maximum=255,
                        step=1,
                        value=-1,
                        label="Red Max",
                        elem_id=self.elem_id("plasma_red_max"),
                    )
                with gr.Row():
                    grn_min = gr.Slider(
                        minimum=-1,
                        maximum=255,
                        step=1,
                        value=-1,
                        label="Green Min",
                        elem_id=self.elem_id("plasma_grn_min"),
                    )
                    grn_max = gr.Slider(
                        minimum=-1,
                        maximum=255,
                        step=1,
                        value=-1,
                        label="Green Max",
                        elem_id=self.elem_id("plasma_grn_max"),
                    )
                with gr.Row():
                    blu_min = gr.Slider(
                        minimum=-1,
                        maximum=255,
                        step=1,
                        value=-1,
                        label="Blue Min",
                        elem_id=self.elem_id("plasma_blu_min"),
                    )
                    blu_max = gr.Slider(
                        minimum=-1,
                        maximum=255,
                        step=1,
                        value=-1,
                        label="Blue Max",
                        elem_id=self.elem_id("plasma_blu_max"),
                    )

            with gr.Row():
                seed_choice = gr.Textbox(
                    label="Seed override",
                    value=-1,
                    interactive=True,
                    elem_id=self.elem_id("seed_choice"),
                    visible=False,
                )

        return [
            enabled,
            denoising,
            val_min,
            val_max,
            red_min,
            red_max,
            grn_min,
            grn_max,
            blu_min,
            blu_max,
            seed_choice,
        ]

    def create_fast_noise(
        self,
        p,
        enabled,
        denoising,
        val_min,
        val_max,
        red_min,
        red_max,
        grn_min,
        grn_max,
        blu_min,
        blu_max,
        seed_choice,
    ):

        np.random.seed(seed_choice)
        random.seed(seed_choice)
        orig_width = p.width
        orig_height = p.height

        width = (p.width // 4) + 4
        height = (p.height // 4) + 4

        if red_min == -1:
            red_min = 0
        if red_max == -1:
            red_max = 255
        if grn_min == -1:
            grn_min = 0
        if grn_max == -1:
            grn_max = 255
        if blu_min == -1:
            blu_min = 0
        if blu_max == -1:
            blu_max = 255
        if val_min == -1:
            val_min = 0
        if val_max == -1:
            val_max = 255
        if red_min < val_min:
            red_min = val_min
        if grn_min < val_min:
            grn_min = val_min
        if blu_min < val_min:
            blu_min = val_min
        if red_max > val_max:
            red_max = val_max
        if grn_max > val_max:
            grn_max = val_max
        if blu_max > val_max:
            blu_max = val_max

        # Generate a random array of shape (width, height, 3)
        rgb_array = np.random.random(size=(width, height, 3))
        intarray = np.zeros_like(rgb_array, dtype=np.uint8)
        intarray[:, :, 0] = red_min + (rgb_array[:, :, 0] * (red_max - red_min))
        intarray[:, :, 1] = grn_min + (rgb_array[:, :, 1] * (grn_max - grn_min))
        intarray[:, :, 2] = blu_min + (rgb_array[:, :, 2] * (blu_max - blu_min))

        img = Image.fromarray(intarray, mode="RGB")
        img = img.resize((img.width * 4, img.height * 4))  # use default resizing algo
        img = img.crop((0, 0, orig_width, orig_height))

        return img

    def process(
        self,
        p,
        enabled,
        denoising,
        val_min,
        val_max,
        red_min,
        red_max,
        grn_min,
        grn_max,
        blu_min,
        blu_max,
        seed_choice,
    ):
        if not enabled or "alt_hires" in p.extra_generation_params:
            return None

        if p.enable_hr:
            self.hr_denoise = p.denoising_strength
            self.hr_steps = p.hr_second_pass_steps
            if self.hr_steps == 0:
                self.hr_steps = p.steps
            if p.hr_resize_x == 0 and p.hr_resize_y == 0:
                self.scalingW = p.hr_scale
                self.scalingH = p.hr_scale
            else:
                self.scalingW = p.hr_resize_x
                self.scalingH = p.hr_resize_y
            self.scaler = p.hr_upscaler
        else:
            self.scalingW = 0

        # image size
        p.__class__ = processing.StableDiffusionProcessingImg2Img
        dummy = processing.StableDiffusionProcessingImg2Img()
        for k, v in dummy.__dict__.items():
            if hasattr(p, k):
                continue
            setattr(p, k, v)

        p.extra_generation_params["Alt denoising strength"] = denoising
        p.extra_generation_params["Value Min"] = val_min
        p.extra_generation_params["Value Max"] = val_max
        p.extra_generation_params["Red Min"] = red_min
        p.extra_generation_params["Red Max"] = red_max
        p.extra_generation_params["Green Min"] = grn_min
        p.extra_generation_params["Green Max"] = grn_max
        p.extra_generation_params["Blue Min"] = blu_min
        p.extra_generation_params["Blue Max"] = blu_max
        p.initial_noise_multiplier = (
            1.0  # Note this was adjustable in seshelle's ext. Not sure what it does
        )
        p.denoising_strength = float(denoising)

        img_num = p.batch_size

        p.init_images = []

        init_seed = int(seed_choice)

        # "Seed must be between 0 and 2**32 - 1"
        init_seed = min(max(init_seed, 0), 2**32 - 1)

        for img in range(img_num):
            real_seed = init_seed + img
            p.extra_generation_params["Alt noise type"] = "Fast"
            image = self.create_fast_noise(
                p,
                True,
                denoising,
                val_min,
                val_max,
                red_min,
                red_max,
                grn_min,
                grn_max,
                blu_min,
                blu_max,
                init_seed,
            )

            p.init_images.append(image)

    def postprocess(
        self,
        p,
        processed,
        enabled,
        denoising,
        val_min,
        val_max,
        red_min,
        red_max,
        grn_min,
        grn_max,
        blu_min,
        blu_max,
        seed_choice,
    ):
        if (
            not enabled
            or self.scalingW == 0
            or "alt_hires" in p.extra_generation_params
            or not p.enable_hr
        ):
            return None
        devices.torch_gc()

        new_p = p
        new_p.init_images = []
        for i in range(len(processed.images)):
            new_p.init_images.append(processed.images[i])

        new_p.extra_generation_params["alt_hires"] = self.scalingW
        new_p.width = int(new_p.width * self.scalingW)
        new_p.height = int(new_p.height * self.scalingH)
        new_p.denoising_strength = self.hr_denoise

        if new_p.denoising_strength > 0:
            new_p.steps = max(1, int(self.hr_steps / self.hr_denoise - 0.5))
        else:
            new_p.steps = 0

        p.resize_mode = 3 if "Latent" in self.scaler else 0
        new_p.scripts = None
        new_p = processing.process_images(new_p)
        processed.images = new_p.images
