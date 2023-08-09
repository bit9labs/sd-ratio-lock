## sd-ratio-lock

An extension for [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) that maintains a locked ratio between the image width and height sliders.

#### Text2Image View
![Ratio Lock](./screenshots/screenshot.png?raw=true "Ratio Lock")

## Installation

The extension can be installed directly from within the **Extensions** tab within the Webui.

Manual install from within the webui directory:

	git clone https://github.com/bit9labs/sd-ratio-lock extensions/sd-ratio-lock

and restart your stable-diffusion-webui. The lock ratio dropdown will appear under the width and height sliders.

## Use

Select an option from the Image Ratio dropdown. This will lock the height slider to the width slider. To unlock the sliders select None from the dropdown. Select the magnifying glass to attempt to identify the Ratio based on the current width and heights.

NOTICE: Currently the way that gradio callbacks work this only works when the width changes. Also since this is a client to server to client solution the order of operations sometimes gets missed. (i.e. It requires you to jiggle the width slider to get the correct height)

## Roadmap

- Allow for custom ratios
- Increase tolerance for the find button

## Credit
