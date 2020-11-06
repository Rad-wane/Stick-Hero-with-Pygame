# Stick hero with Python

Dev. by : Porphyre 


## Game play:

Using the left click, a growing stick is drawn. Once the click ends, the stick rotates. If it's length is enough, the hero moves to the other obstacle. If not, the hero drops and dies. A game over screen is then displayed.   
The game over screen can be removed, and the game restarted with the right click, a new game is launched. 
The score of the game is incremented with 1 each time the hero moves from one obstacle to another. 
A high score is updated each time accordingly and displayed in the game over screen. 

## The code:

This game uses OOP, the code has comments for clarity. 

It uses mainly `pygame`. Images used for animations are in `images`, so are `sounds`. The font used is the one used in the game *Flappy Bird* : `04B_19` with sizes 40 ans 35.

`pygame` & `pygame.mixer` were initialized so that the game run smoothly :
* The screen dimensions chosen are : `540x868`
* The frame rate is set to 160
* `pygame.mixer` has the following initialization arguments : `frequency`=44100,`size`=16,`channels`=1,`buffer`=512

Besides `pygame`, I imported `sys`, `colors.py`, `random`, `sys`, `time` and 3 lists of images for the animation of the hero : `walkRight`, `idle` and `dying`

A `Obstacle` class is created and has the following attributes :
* `color` that is set to black
* `pos` that gives a tuple with the coordinates of the top left point of the obstacle
* `width` that sets the with
* `height` that sets the height
And the following methods : 
* `draw` that draws the obstacle in the screen in position 
* `move` that moves the obstacle to the left by a `dist`
* `get_tr_pos` that return the top right position of the obstacle
* `get_tl_pos` that return the top left position of the obstacle
* `get_width` that return the width of the obstacle

Outside the class, some miscellaneous functions:
* `move_hero` that moves the hero in both directions 
* `score_dis_on` that displays the current score all the time 
* `high_score_dis` the displays the high score if the game ended 
* `game_over_screen` that shows the game over screen with : `current score`, `high score` and info to start again, and if it is a new high score, show `"high score !"` in turquoise

3 obstacles are then created, 2 with random widths, and the hero is placed on top of the first one. Then we enter the main game loop after setting some global variables. 

In the main game loop : 
* We animate the hero (once every 13 frames) depending on 3 states : 
    * if the hero is `idle`
    * if the hero is moving : `walkRight`
    * if the hero is `dying` (in this case, the last picture of the animation is kept until the game ends)
*  There's an event loop to quit the game : `close` or the `Esc` button
*  if we left click and maintain the click, a growing vertical stick is drawn. once the click ends, the  stick is rotated:
    * if the length of the stick is short : the stick rotation continue to 180°. The hero then drops and the game is over.
    * if the length of the stick is too long, the stick stays in the 90°, the hero moves to it's extremity and then drops. The game is over. 
    * if the length of the stick is enough, the stick stays in the 90°, the hero moves to the second obstacle. Then all is moved to the left and an new obstacle is generated.The Game continue. 
*   There is a process to regulate the position of the hero so that he will always be on the top right of the obstacles.
*   If the game is over, click right to start again, or `Esc` to close the game. 

There's a sound : at the start, a shift is completed, while rotating the stick and when the hero is dead.

For further details, see the code : `stick_hero.py`


