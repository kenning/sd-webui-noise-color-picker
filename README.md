# sd-webui-noise-color-picker

This is practically a fork of [diffusion-noise-alternatives](https://github.com/Seshelle/diffusion-noise-alternatives-webui) and actually has far fewer features. 

In comparison this extension is much faster.

## Examples

Output with no parameters set:

![Workflow with no parameters set](https://github.com/kenning/sd-webui-noise-color-picker/blob/main/images/base.png)

Same seed, parameters, etc. but brightness maxed at 50/255:

![Darker output](https://github.com/kenning/sd-webui-noise-color-picker/blob/main/images/dark.png)

Same but high minimum red (and low maximum green and blue, to further emphasize red)

![Redder output](https://github.com/kenning/sd-webui-noise-color-picker/blob/main/images/redder.png)

Same with high minimum green, slight minimum red and a low maximum blue

![Green and red output](https://github.com/kenning/sd-webui-noise-color-picker/blob/main/images/green_and_red.png)

## TODO

- Would be nice to improve on the UI
- I guess it should handle strange inputs like a min being higher than a max
