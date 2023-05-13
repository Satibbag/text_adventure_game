# Main program that the game runs from.

# Import the necessary modules.
# Import pickle in order to enable persistent storage.
import pickle
from Items import Item
from Rooms import Room
from Player import player
# Importing os so that the screen can be cleared when the user uses the "clear" command.
import os

# Define the possible player actions.
ACTIONS = ("quit",  # Quit the game
           "save",  # Save the current game
           "load",  # Load a previous game save
           "get",  # Add an item to the player's inventory
           "use",  # Use an item from the player's inventory
           "move",  # Display the possible movement options
           "inspect",  # Inspect an item in the current room
           "view inventory",  # Display the player's current inventory.
           "clear",  # Clears the terminal screen.
           "test",  # Purely for testing purposes.
           )

# Initializes the game_data dictionary.
game_data = {}


def valid_input(prompt="What would you like to do?\n> "):
    """Forces the player to select a valid action."""
    response = None
    while response not in ACTIONS and response not in list(map(lambda action: action[0], ACTIONS)):
        print("\033[1m\u2014" * 14 + "COMMANDS" + "\u2014" * 14 + "\033[0m")
        for action in ACTIONS:
            if action != "test":
                print(f"* {action.title()} ({action[0]})")
        response = input(prompt).lower().strip()
        if response not in ACTIONS and response not in list(map(lambda action: action[0], ACTIONS)):
            print(f'"{response}" is not a valid command. Please enter a valid command.\n')
    return response


def save():
    """Save the Player object and the rooms dictionary to a file."""
    global game_data

    with open("game.dat", "wb") as file:
        game_data = {"player": player,
                     "rooms": rooms,
                     "items": items}
        pickle.dump(game_data, file)

    print("Game successfully saved!")


def load():
    """Load the Player object and the rooms dictionary from a file."""
    global game_data
    global player
    global rooms
    global items

    try:
        with open("game.dat", "rb") as file:
            game_data = pickle.load(file)

            player = game_data["player"]
            rooms = game_data["rooms"]
            items = game_data["items"]

        print("Game successfully loaded!")

    except FileNotFoundError:
        print("Game file not found! :(")


def main():
    """Main game loop"""
    global player
    global rooms
    global items

    print("In this game, you play as a crew member aboard the space ship the \033[3mUSS Prospect\033[0m.")
    print()
    print("You wake up to the sound of alarms going off and warning lights flashing all over the ship.")
    print("Suddenly, you hear an announcement over the PA system...")
    print("\033[0;31mWARNING: We are trapped in the gravitational pull of a black hole! Destruction is imminent! "
          "Get to the escape pods immediately!\033[0m")

    choice = None
    while choice != "quit":
        # Unpack the current room variables.
        room = rooms.get(player.position, "Invalid room setting - something broke :(")
        print(room.describe())
        if player.position == (1, 0, -1):
            player.won = True
            break
        choice = valid_input()
        if choice == "quit" or choice == "q":
            break
        elif choice == "save" or choice == "s":
            save()
        elif choice == "load" or choice == "l":
            load()
        elif choice == "get" or choice == "g":
            print("\033[1;34m\nGETTING ITEM\033[0m")
            room.get_item(player)
        elif choice == "use" or choice == "u":
            print("\033[1;34m\nUSING ITEM\033[0m")
            room.use_item(player)
        elif choice == "move" or choice == "m":
            print("\033[1;34m\nMOVING\033[0m")
            room.move(player)
        elif choice == "inspect" or choice == "i":
            print("\033[1;34m\nINSPECTING ITEM\033[0m")
            room.inspect_item(player)
        elif choice == "view inventory" or choice == "v":
            print("\033[1;34m\nVIEWING INVENTORY\033[0m")
            room.view_inventory(player)
        elif choice == "clear" or choice == "c":
            os.system("cls")

        # Purely for testing purposes.
        elif choice == "test" or choice == "t":
            print(player)
            print()
            for room_item in rooms:
                print(f"{rooms[room_item]}\n")

    if player.won:
        print("Congratulations on beating the game!")

    print("Thanks for playing! :)")


# --------------------------------------------------------------------------------------------------------------------
rooms = {}

# Found In: Laboratory
# Used In: Control Room
keycard = Item("Keycard",
               "An electronic keycard used to access locked areas.",
               "You pickup the keycard. It shines with a metallic sheen.",
               "You swipe the keycard, and the locked door clicks open.",
               "key",
               unlocked_directions=["north"])

# Found In: Captain's Quarters
# Used In: Security Office
access_code = Item("Access Code",
                   "A piece of paper with a code written on it.",
                   "You find an access code.",
                   "You enter the code and the door opens.",
                   "key",
                   unlocked_directions=["west"])

# Found In: Security Room
# Used In: Cargo Hold
security_card = Item("Security Card",
                     "A high-level security card used for accessing secured areas.",
                     "You found a security card. It grants access to highly restricted zones.",
                     "You slide the security card into the card reader, and the door unlocks.",
                     "key",
                     unlocked_directions=["west"])

# Found In: Lounge
# Used In: Medical Bay
code_breaker = Item("Code Breaker",
                    "A portable device capable of deciphering security codes.",
                    "You found a code breaker. It can bypass security systems.",
                    "With the code breaker, you easily decrypt the security code, granting access to the locked room",
                    "key",
                    unlocked_directions=["west"])

# Found In: Observation Deck
# Used In: Engineering Bay
key = Item("Key",
           "A standard looking golden key.",
           "You find a standard key. How quaint.",
           "You slide the key into the lock and turn it. The door unlocks with a click.",
           "key",
           unlocked_directions=["north"])

# Found In: Cargo Hold
# Used In: Medical Bay
password = Item("Password",
                "A sticky note with a password sloppily scrawled onto it.",
                "You fold up the sticky note and put it into your pocket.",
                "You type the password into the computer. The slides open with a swish.",
                "key",
                unlocked_directions=["north"])

# Found In: Control Room
# Used In: Laboratory
cutter = Item("Plasma Cutter",
              "A handheld tool that emits a high-energy beam capable of cutting through metal.",
              "You acquired a plasma cutter. It can slice through sturdy materials.",
              "You activate the plasma cutter, and its energy blade effortlessly slices through the metal box.",
              "tool")

# Found In: Laboratory
# Used In: Captain's Quarters
cabinet_key = Item("Cabinet Key",
                   "A small key for a cabinet.",
                   "You found a small key. It appears to go to a cabinet of some kind.",
                   "You insert the key into the cabinet, unlocking the door and find a keycard inside.",
                   "tool")

# Found In: Lounge
# Used In: Engineering Bay
energy_cell = Item("Energy Cell",
                   "A power source used to energize various devices.",
                   "You acquired an energy cell. It can provide power to compatible devices.",
                   "You insert the energy cell into the empty slot, and the device powers on.",
                   "tool")

items = {"keycard": keycard,
         "access_code": access_code,
         "security_card": security_card,
         "code_breaker": code_breaker,
         "key": key,
         "password": password,
         "cutter": cutter,
         "cabinet_key": cabinet_key,
         "energy_cell": energy_cell}

# Lounge
r = Room("Lounge", [items["code_breaker"], items["energy_cell"]], [], ["east"])
r.descriptions[(("code_breaker", "energy_cell"), ())] = f"{r.room_name} \u2014 You look around the room and see a Code Breaker " \
                                                        "and an Energy Cell."
r.descriptions[(("code_breaker",), ())] = f"{r.room_name} \u2014 You look around the room and see an Energy Cell."
r.descriptions[(("energy_cell",), ())] = f"{r.room_name} \u2014 You look around the room and see a Code Breaker."
r.descriptions[((), ())] = f"{r.room_name} \u2014 It doesn't look like there's anything of use in here..."
rooms[0, 0, 0] = r

# Observation Deck
r = Room("Observation Deck", [items["key"]], [], ["west", "north"])
r.descriptions[(("key",), ())] = f"{r.room_name} \u2014 There's a large window looking out into space. All you can " \
                                 f"really see through it though is the massive black hole that's pulling you in to your " \
                                 f"imminent demise. How charming. You also see a key on the table in the corner."
r.descriptions[((), ())] = f"{r.room_name} \u2014 There's a large window looking out into space. All you can really see " \
                           f"through it though is the massive black hole that's pulling you in to your imminent demise. " \
                           f"How charming."
rooms[1, 0, 0] = r

# Medical Bay
r = Room("Medical Bay", [], [items["code_breaker"], items["password"]], ["south"])
r.descriptions[((), ("code_breaker", "password"))] = f"{r.room_name} \u2014 Overturned or broken medical instruments " \
                                                     f"and devices are strewn all over the room. There's a door straight " \
                                                     f"ahead with a computer connected to it, and a door to your left " \
                                                     f"with a note on the keypad that says \033[3m\"Forgot password to " \
                                                     f"this door... Sorry for the inconvenience! :)\"\033[0m " \
                                                     f"Oh well that's just great!"
r.descriptions[((), ("password",))] = f"{r.room_name} \u2014 Overturned or broken medical instruments and devices are " \
                                      f"strewn all over the room. There's a door straight ahead with a computer " \
                                      f"connected to it, and an open door to your left."
r.descriptions[((), ())] = f"{r.room_name} \u2014 Overturned or broken medical instruments and devices are strewn all " \
                           f"over the room. There are open doorways straight "

# Engineering Bay

# Laboratory

# Control Room

# Captain's Quarters

# Maintenance Bay

# Security Office

# ID Room

# Cargo Hold

# Escape Pods

# key = Item("key",
#            "A golden key",
#            "You pick up the key.",
#            "You use the key to unlock the cellar door.",
#            "key",
#            unlocked_directions=["down"])
#
# stick = Item("stick",
#              "A brown stick",
#              "You pick up the stick.",
#              "You use the stick.")
#
# items = {"key": key, "stick": stick}
#
# # Entryway
# r = Room("Entryway", [items["key"]], [items["stick"]], ["east"])
# r.descriptions[(("key",), ("stick",))] = f"{r.room_name} - There's a mound of dirt."
# r.descriptions[(("key",), ())] = f"{r.room_name} - An uncovered key with scattered dirt around it and a used stick."
# r.descriptions[((), ())] = f"{r.room_name} - Scattered dirt and a used stick."
# rooms[0, 0, 0] = r
#
# # Room 1
# r = Room("Room 1", [items["stick"]], [items["key"]], ["west"])
# r.descriptions[(("stick",), ("key",))] = f"{r.room_name} - There's a locked cellar door and a stick on the ground."
# r.descriptions[((), ("key",))] = f"{r.room_name} - There's a locked cellar door."
# r.descriptions[((), ())] = f"{r.room_name} - There's an unlocked cellar door."
# rooms[(1, 0, 0)] = r
#
# # Cellar
# r = Room("Cellar", allowed_movements=["up"])
# r.descriptions[((), ())] = f"{r.room_name} - You beat the game!"
# rooms[(1, 0, -1)] = r


if __name__ == "__main__":
    main()
