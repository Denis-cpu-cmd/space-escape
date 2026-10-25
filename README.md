# Space Escape

#### Video Demo: https://youtu.be/4Z_Ck8kFSxc

#### Description

Space Escape is a text-based adventure game I made for the final project of Harvard's CS50's Introduction to Programming with Python (CS50P).

In the game, the player wakes up on a damaged spaceship and has to find a way to escape before running out of oxygen. The spaceship has nine rooms arranged in a 3×3 grid. To escape, the player needs to find a battery and an access card, as well as a key to unlock the Escape Pod.

The game is not only about finding the right items. Some rooms are randomly chosen to be dark, so the player needs a torch to explore them properly. Oxygen is limited, and entering the Reactor consumes more oxygen than entering other rooms. Because of this, the player has to be careful about where they go and how much time they spend exploring.

#### Gameplay

The player moves around the spaceship using the commands `up`, `down`, `left`, and `right`. There are also commands to check the inventory, collect items, use the torch, restore oxygen with an oxygen tank, and quit the game.

The goal is to collect everything needed, reach the Escape Pod, and escape before running out of oxygen. If the player does not manage their resources carefully, they can lose before reaching the end.

#### Implementation and Files

The main code is in `project.py`. I organized the game using four classes:

- `Item` represents the different items and their descriptions.
- `Room` contains information about each room, including its exits, items, lighting, and locked status.
- `Player` keeps track of the player's position, inventory, and oxygen.
- `Game` sets up the spaceship and manages the main game loop and player commands.

I used a dictionary with coordinate tuples to represent the spaceship. I found this useful because it makes it easier to keep track of rooms and calculate where the player can move.

I also used the `random` module to randomize item placement and dark rooms. The `re` module is used to validate the player's name, and `sys` is used to exit the program. Some tasks, such as calculating movement, oxygen consumption, and checking if the player has won, are handled by separate functions.

The file `test_project.py` contains tests for movement, oxygen consumption, and the conditions needed to win. I included different cases, such as missing items, having no oxygen left, or being in the wrong room.

#### Design Choices

I decided to make the game text-based because I wanted to focus on the logic and the Python code instead of spending time creating graphics. I also wanted each playthrough to be a little different, which is why I added random item placement and dark rooms.

One of the main challenges was keeping track of everything happening in the game, especially the player's position, since most of the game mechanics depends on it. Making all the classes and functions work well together was also difficult, but it pushed me to improve my problem-solving skills and learn how to think more logically when writing code.

Overall, this project gave me the chance to practise object-oriented programming, dictionaries, tuples, lists, input validation, and testing while building something interactive.

#### Requirements and How to Run

Python 3 is required to run the game. It uses only Python's built-in libraries. `pytest` is needed only if you want to run the tests.

To start the game:

```bash
python project.py
```

To run the tests:

```bash
pytest test_project.py
```
