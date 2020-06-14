<p align="center">
  <h1 align="center">
    jinny's jeep game
  </h1>
</p>
<p align="center">
  :vertical_traffic-light: :car: <em>using pyOpenGL to build a basic car-driving game to avoid obstacles and profit</em> :collision: :construction:
</p>

---

## Dependencies
* Python 2 
* `pip install -r requirements.txt`

## Run
`python src/main.py`

## Basic Premise 
### (Written when I was a tired college senior)

The scene I am modeling is a purply-colored jeep navigating the world. It can move in the space given. Cones exist to be obstacles for the jeep to go around. The wheels are constantly turning, because it is a very fashionable vehicle. The lights could also turn on to help with navigation at night.

## Future Work
* Velocity vectors and basic collision detection are in the works. 
* Data structures have been set up but not completely
implemented. 
* The goal is to have the boundaries be a stopper as well as having the jeep automatically go around the
cones. This collision detection is dependent on getting the velocity vectors fully implemented and functional.
* Multiple viewports was also an idea that was explored, but due to a lack of time, was foregone.
* Center view can be toggled, but is buggy.
* There is a help screen to show all of the options in application. It can be toggled on and off, this can be better demonstrated.
* A plan was to include pedestrians that would walk across the street. The goal was also to include textures on the star and the diamond (which has been done in Blender, see “textureObjects.blend”), however, these goals were hampered by our inability to import Blender textures. 

## Development
This folder contains:
* Blender files (show creation process and allows changes)
* `*.obj` and `*.mtl` files for importing into project
* `ImportObject.py` for importing .obj/.mtl into project
* Compartmentalized class files for jeep (including wheels and lights) and cones (as obstacles)
* You can expand the length of the game by toggling a variable called `gameEnlarge`. You can toggle the sensitivity of how close the Jeep can come close to the different objects by toggling `ckSense`.
* To apply lighting to the game, one can change the value of `applyLighting` to True to see some of the settings that are available in lighting the environment. A developer can also modify the values in the ambient, diffuse, specular, shininess, and location of the light.

## Basic Intro to “Jeep Time Trial”
This game works by giving you control of a jeep. You are able to maneuver through a strip of land that consists of obstacles (traffic cones) and incentives (stars and one diamond). Your goal is to receive the lowest “score,” a measure of time that can be reduced with incentives. You control the jeep with the up and down (forward and backward), left and right (rotation) arrow keys. The setting of the game is on a road, which is made with by importing a road texture applied to a native plane asset.

The game begins with a countdown. During this countdown, you can use the “pageUp” and “pageDown” to toggle through a few different colors of jeep (purple, green, and red). During the countdown to beginning, the jeep is unable to move. Once the game begins, the score follows the jeep as it traverses the entire path. Traffic cones, stars, and a diamond have locations that are randomly generated and stand in the path between the beginning and end of the jeep’s path. Hitting a cone results in an automatic incomplete trial, as well as running off the road on either side. Hitting a star reduces the score by 10 points (a good thing), and hitting the one diamond reduces the score by half of what it is. Since the jeep is able to move forward and backward (wheels follow direction of movement), this feature allows the player to control when those applications happen to it, and allows for strategies for when to save an asset or when to use it. Using the “l” key toggles the jeep’s headlights, giving it better visual and a fun graphic. 

Reaching the end of the path allows for a complete trial. A “complete screen” appears if the player successfully completed a trial, despite how long it takes. This trial is then documented in a database called “results.csv” to compare to players that come afterward. The usage of this is also for multi-players across different times and places to play the same game and be compared to other players. Unsuccessful trials are also documented for the purpose of tracking plays.

There are a few different views available for the game player. First, the player can use the mouse middle button to pan across the entire scene, giving him/her the most vision to the obstacle that he or she is traveling through. In addition to this, using the keys “t” and “b,” one can get a top view (map-like) and a behind view (driver’s view). Using “c,” one can toggle between the panning to be around the entire scene’s original origin, or around the jeep’s current location. Using “r” resets the camera position to the origin. 


### Thank you and enjoy playing!

## License

This code is released under the [MIT License](https://opensource.org/licenses/MIT).