# sd-webui-noise-color-picker

This is practically a fork of [diffusion-noise-alternatives](https://github.com/Seshelle/diffusion-noise-alternatives-webui) and actually has far fewer features. 

In comparison this extension is much faster.

## Tips on usage

* Color control over outputs is most noticeable when all three colors are changed. Try a high min with one color and a low max with the other two to see a clear impact.

* -1 means no value. If a min is -1 it is 0; if a max is -1 it is 255

* This extension changes the **initial** noise from SD's basic gaussian noise in txt2img to allow for color control. 

* Because it only changes the initial state, it is easily overridden by loras or even the subject. If you turn 

## Examples

Output with no parameters set:

![Workflow with no parameters set](https://github.com/kenning/sd-webui-noise-color-picker/blob/main/images/base.png)

Same seed, parameters, etc. but brightness maxed at 50/255:

![Darker output](https://github.com/kenning/sd-webui-noise-color-picker/blob/main/images/dark.png)

Same but high minimum red (and low maximum green and blue, to further emphasize red)

![Redder output](https://github.com/kenning/sd-webui-noise-color-picker/blob/main/images/redder.png)

Same with high minimum green, slight minimum red and a low maximum blue

![Green and red output](https://github.com/kenning/sd-webui-noise-color-picker/blob/main/images/green_and_red.png)

## Known issues

Under the hood, this extension actually uses the img2img pipeline. As a result, some extensions or some combination of extensions do not work properly.

## TODO

- Would be nice to improve on the UI
- As brightness goes up, maybe the other colors could go up too
- I guess it should handle strange inputs like a min being higher than a max
