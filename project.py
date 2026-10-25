import sys
import random
import re

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Room:
    def __init__(self, name, description, position, items, possible_directions, locked = False, lights = True):
        self.name = name
        self.description = description
        self.position = position
        self.items = items
        self.possible_directions = possible_directions
        self.locked = locked
        self.lights = lights

    def check_problems(self):
        if self.locked == True:
           return "Unfortunately, you cannot enter in that room. You need a key!"
        if self.lights == False:
            return "Unfortunately, you cannot see anything in this room. You need a torch!"
        return ""

    def available_items(self):
        if self.items == []:
            return "There are no items here."
        else:
            return f"Available items: {', '.join(self.items)}"

    def collect_item(self,item, item_description, map):
        if item in self.items:
            self.items.remove(item)
            return f"You collect a {item}, check the inventory.\n{item_description[item].description}"
        elif len(self.items) == 1:
            return f"Only {', '.join(self.items)} is avaiable to collect."
        else:
            return "You cannot collect anything. There are no items here."

class Player:
    def __init__(self, name, position , inventory = None, oxygen = 100, alive = True):
        self.name = name
        self.position = position
        self.inventory = [] if inventory is None else inventory
        self.oxygen = oxygen
        self.alive = alive
        if self.oxygen > 0:
            self.alive = True
        else:
            self.alive = False

    def show_inventory(self):
        if self.inventory == []:
            return "Your inventory is empty."
        else:
            return f"Your inventory contains: {', '.join(self.inventory)}"

    def update_inventory(self, item, list_items):
        if item in list_items:
            self.inventory.append(item)
        else:
            pass

    def move(self, direction):
        self.position = get_new_position(self.position,direction)

    def check_oxygen(self):
        if self.oxygen <= 0:
            self.alive = False
        return self.oxygen

class Game:
    def __init__(self):
        self.map = {
            (0, 0): Room(
                "Control Room",
                "The spacecraft's main control center. "
                "Broken monitors flicker, and warning messages "
                "flash across the screens.",
                (0,0),
                [],
                ("right", "down")
            ),

            (1, 0): Room(
                "Laboratory",
                "A scientific laboratory filled with damaged "
                "equipment. Strange experiments appear to have "
                "been abandoned in a hurry.",
                (1,0),
                [],
                ("right", "left", "down")
            ),

            (2, 0): Room(
                "Storage",
                "A dark storage compartment containing scattered "
                "crates and abandoned supplies. Something useful "
                "might be hidden among the debris.",
                (2,0),
                [],
                ("left", "down")

            ),

            (0, 1): Room(
                "Engine Room",
                "The spacecraft's engines are severely damaged. "
                "Sparks fly from exposed cables, and the entire "
                "room vibrates with unstable machinery.",
                (0,1),
                [],
                ("right", "up", "down")
            ),

            (1, 1): Room(
                "Main Hall",
                "The central corridor of the spacecraft. "
                "Emergency lights illuminate the damaged walls. "
                "From here, you can explore different sections "
                "of the ship.",
                (1,1),
                [],
                ("right", "left", "up", "down")
            ),

            (2, 1): Room(
                "Medical Bay",
                "An abandoned medical facility. Empty hospital "
                "beds and malfunctioning medical equipment "
                "suggest that the crew evacuated suddenly.",
                (2,1),
                [],
                ("left", "up", "down")
            ),

            (0, 2): Room(
                "Reactor",
                "The spacecraft's nuclear reactor is unstable. "
                "Warning alarms echo through the chamber, "
                "and the temperature is dangerously high.",
                (0,2),
                [],
                ("right", "up")
            ),

            (1, 2): Room(
                "Airlock",
                "A reinforced chamber separating the spacecraft "
                "from the vacuum of space. The pressure control "
                "system appears to be malfunctioning.",
                (1,2),
                [],
                ("right", "left", "up")
            ),

            (2, 2): Room(
                "Escape Pod",
                "You have discovered the emergency escape pod! "
                "However, its activation system requires special "
                "equipment before you can leave the spacecraft.",
                (2,2),
                [],
                ("left", "up"),
                locked = True
            )
        }
        self.items = {
            "torch": Item(
                "torch",
                "A portable flashlight that illuminates dark rooms."
            ),
            "key": Item(
                "key",
                "A metallic key used to unlock secured doors."
            ),
            "oxygen_tank": Item(
                "oxygen_tank",
                "An emergency oxygen supply that restores your oxygen levels."
                "\nType 'use oxygen_tank' whenever you want to refill the oxygen."
            ),
            "access_card": Item(
                "access_card",
                "A security card required to unlock the escape pod."
            ),
            "battery": Item(
                "battery",
                "A high-capacity power cell needed to activate the escape pod."
            )
        }

    @property
    def current_room(self):
        return self.map[self.player.position]

    def introduction(self):
        print("=" * 100)
        print("WELCOME TO THE SPACE GAME".center(100))
        print("YOUR GOAL IS TO ESCAPE FROM THE SPACECRAFT".center(100))
        print("=" * 100)
        self.player = Player(get_name(), (1,1))
        print(f"\n{self.player.name}, you wake up in the Main Hall of a damaged spacecraft.")
        print("The oxygen system is failing.")
        print(f"You have {self.player.oxygen} units of oxygen remaining.")
        print("Find the necessary equipment and reach the escape pod!")

    def display(self):
        if self.current_room.lights == True:
            print("\n" + "=" * 60)
            print(f"LOCATION: {self.current_room.name.upper()}")
            print("-" * 60)
            print(f"Directions: {', '.join(self.current_room.possible_directions)}")
            print(self.current_room.available_items())
            print(f"Oxygen remaining: {self.player.check_oxygen()}/100")
            print("-" * 60)
            print("Commands: inventory | collect 'item name' | quit")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("WARNING: NO LIGHT DETECTED".center(60))
            print("=" * 60)
            print("LOCATION: UNKNOWN")
            print("-" * 60)
            print("You cannot see anything around you.")
            print("Directions: UNKNOWN")
            print("Available items: UNKNOWN")
            print(f"Oxygen remaining: {self.player.check_oxygen()}/100")
            print("-" * 60)
            print("Commands: inventory | quit")
            print("=" * 60)

    def run(self):
        try:
            while not check_win(self.player):
                self.player.check_oxygen()
                if self.player.alive:
                    self.display()
                    if self.current_room.lights == False and "torch" in self.player.inventory:
                        put = input("\nType 'use torch' to illuminate the room > ")
                        print(self.use_torch(put))
                        self.display()
                    inp = input("\nWhat would you like to do? > ").lower().strip()
                    if inp in ["right", "left", "up", "down"]:
                        print(self.handle_movement(inp))
                    elif inp == "inventory":
                        print(self.player.show_inventory())
                    elif inp.startswith("collect "):
                        print(self.handle_collection(inp))
                    elif inp == "use oxygen_tank":
                        print(self.use_oxygen())
                    elif inp == "quit":
                        sys.exit("Thanks for playing Space Escape!")
                    else:
                        print("Invalid command. Try to collect an item, open the inventory or enter a direction.")
                else:
                    sys.exit("You ran out of oxygen. You lost.")

            inp = input("Press enter to escape!!!")
            if inp == "":
                self.end()
            else:
                pass
        except KeyboardInterrupt:
            sys.exit("\nThanks for playing Space Escape!")

    def handle_movement(self, d):
        if d in self.current_room.possible_directions:
            new_pos = get_new_position(self.player.position,d)
            if self.map[new_pos].locked == False:
                self.player.move(d)
                warning = calculate_oxygen(self.player)
                if self.map[new_pos].lights == True:
                    return f"You are now in {self.current_room.name}.\n{self.current_room.description}\n{warning}"
                else:
                    return f"{self.map[new_pos].check_problems()}\n{warning}"
            else:
                return f"{self.map[new_pos].check_problems()}\nYou remain in {self.current_room.name}."
        else:
            return f"You cannot go in that direction. Try: {', '.join(self.current_room.possible_directions)}."

    def handle_collection(self, i):
        if self.current_room.lights == True:
            item_name = i.removeprefix("collect ").strip()
            self.player.update_inventory(item_name, self.current_room.items)
            if "key" in self.player.inventory:
                self.map[(2,2)].locked = False
            return self.current_room.collect_item(item_name, self.items, self.map)
        else:
            return "You do not see anything!"

    def use_torch(self, put):
        item = put.removeprefix("use ").strip()
        if item == "torch":
            self.current_room.lights = True
            return "You use torch, the room is now illuminated."
        else:
            return "You did not use torch. The room is still dark."

    def use_oxygen(self):
            self.player.oxygen = 100
            self.player.inventory.remove("oxygen_tank")
            return "You use oxygen_tank, your oxygen is now full."

    def random_items_lights(self):
        available_rooms = []
        available_items = []
        for coord in self.map:
            if coord not in [(2, 2), (1, 1)]:
                available_rooms.append(coord)
        for i in self.items:
            if i not in ["torch", "key"]:
                available_items.append(i)

        random_items = random.sample(available_items, k=len(available_items))
        for i in random_items:
            random_coord = available_rooms[random.randrange(len(available_rooms))]
            self.map[random_coord].items.append(i)
            available_rooms.remove(random_coord)

        random_room = random.sample(available_rooms, k = 2)
        self.map[random_room[0]].lights = False
        self.map[random_room[1]].lights = False
        self.map[random_room[0]].items.append("key")

        rooms_illuminated = []
        for room in available_rooms:
            if self.map[room].lights == True:
                rooms_illuminated.append(room)
        random_room_illuminated = random.choice(rooms_illuminated)
        self.map[random_room_illuminated].items.append("torch")

    def end(self):
        print("\n" + "=" * 70)
        print("MISSION ACCOMPLISHED!".center(70))
        print("=" * 70)
        print(f"\nCongratulations, Captain {self.player.name}!")
        print("You have successfully activated the escape pod.")
        print("As the spacecraft collapses behind you,")
        print("your escape pod launches into the darkness of space.")
        print("\nAgainst all odds, you survived!")
        print(f"Remaining oxygen: {self.player.oxygen}")
        print("\nThank you for playing SPACE ESCAPE!")
        print("=" * 70)
        sys.exit(0)

def get_name():
    while True:
        name = input("Astronaut, What's your name?: ").title().strip()
        if re.search(r"^[A-Za-z ]+$", name):
            return name
        else:
            print("Invalid name, please use letters only!")

def get_new_position(pos, direction):
    x,y = pos
    if direction == "right":
        x += 1
    elif direction == "left":
        x -= 1
    elif direction == "up":
        y -= 1
    elif direction == "down":
        y += 1
    return (x,y)

def calculate_oxygen(p):
    if p.position == (0,2):
        p.oxygen -= 10
        return "Warning! You are losing more oxygen here."
    else:
        p.oxygen -= 5
        return ""

def check_win(p):
    if p.alive == True and p.position == (2,2):
        if "battery" in p.inventory and "access_card" in p.inventory:
            return True
        else:
            return False
    else:
        return False

def main():
    game = Game()
    game.random_items_lights()
    game.introduction()
    game.run()

if __name__ == "__main__":
    main()
