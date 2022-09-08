# Computer Vision Hackathon

## Initialize environment

Clone this repository locally:

`git clone git@github.com:Sam-Sweere-Vantage-AI/cv-hackathon.git`

Go into the repository directory:

`cd cv-hackathon`

Create a virtual environment:

`python3 -m venv venv`

(Developed on `Python 3.10.4` but should work with any `python 3.X`)

Activate the environment:

`source venv/bin/activate`

Install the dependencies:

`pip install -r requirements.txt`

## The Goal
The game itself consists out of a simple dodge game. Dodge the obstacles to stay alive as long as possible!
However, you cannot control the Vantage player with your mouse or keyboard. Only with your webcam!

The team/player that is able to reach the furthest level wins! 

## Creating your custom webcam controller

You can build your webcam controller in the `camera_controller.py` file. 
This file contains the `CameraController` class. Every tick of the game, the `get_location` of this class is called, given the latest input image.
Using this input `image`, you have to control the player by returning the `x` and `y` coordinates of the player.
You can use any technique you want as long as the final `x` and `y` coordinates are based on the `image`.

Finally, you can also return an image that will be drawn in the game's background. By default, this is the input `image`.
But for visualization and debugging, it can be practical to draw/change this image.

## Playing the game

Run `python3 run_game.py`

For fairness, stay out of the `dodge_game` files.
