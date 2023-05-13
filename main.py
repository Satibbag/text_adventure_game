# Main program that the game runs from.

# Import the necessary modules.
# Import pickle in order to enable persistent storage.
import pickle
from Items import Item
from Rooms import Room
from Player import player
# Importing os so that the screen can be cleared when the user uses the "clear" command.
import os

import re

# Define the possible player actions.
ACTIONS = ("quit",  # Quit the game
           "save",  # Save the current game
           "load",  # Load a previous game save
           "get",  # Add an item to the player's inventory
           "use",  # Use an item from the player's inventory
           "move",  # Display the possible movement options
           "inspect",  # Inspect an item in the current room
           "view inventory",  # Display the player's current inventory.
           # "clear",  # Clears the terminal screen.
           "test",  # Purely for testing purposes.
           )

# Initializes the game_data dictionary.
game_data = {}


def valid_input(prompt="\033[35mWhat would you like to do?\n>\033[0m"):
    """Forces the player to select a valid action."""
    response = None
    while response not in ACTIONS and response not in list(map(lambda action: action[0], ACTIONS)):
        print("\033[1;34m\u2014" * 14 + "COMMANDS" + "\u2014" * 14 + "\033[0m")
        for action in ACTIONS:
            if action != "test":
                print(f"* {action.title()} ({action[0]})")
        response = input(prompt).lower().strip()
        if response not in ACTIONS and response not in list(map(lambda action: action[0], ACTIONS)):
            print(f'\033[31m"{response}" is not a valid command. Please enter a valid command.\n\033[0m')
    return response


def save():
    """Save the Player object and the rooms dictionary to a file."""
    global game_data

    with open("game.dat", "wb") as file:
        game_data = {"player": player,
                     "rooms": rooms,
                     "items": items}
        pickle.dump(game_data, file)

    print("\033[1;34mGame successfully saved!\033[0m")


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

        print("\033[1;34mGame successfully loaded!\033[0m")

    except FileNotFoundError:
        print("\033[31mGame file not found! :(\033[0m")


def main():
    """Main game loop"""
    global player
    global rooms
    global items

    print("\nIn this game, you play as a crew member aboard the \033[3mUSS Prospect\033[0m, a space ship sent out by "
          "the U.S. Space Force to explore beyond our solar system.")
    print()
    print("You wake up to the sound of alarms going off and warning lights flashing all over the ship.")
    print("It doesn't look like there's anyone else still on the ship.")
    print("Suddenly, you hear the robotic, monotone voice of an automated announcement over the PA system...")
    print("\033[1;31mWARNING: We are trapped in the gravitational pull of a black hole! Destruction is imminent! "
          "Get to the escape pods immediately!\033[0m")
    print()
    print("\033[3;32mWhat do you do?\033[0m")

    choice = None
    while choice != "quit":
        # Checks to see if the player has won.
        if player.won:
            print("\033[1m\033[4;35You escaped the game!!!\033[0m")
            print("\033[1m\033[4;35Congratulations on beating the game!\033[0m")
            return
        # Unpack the current room variables.
        room = rooms.get(player.position, "\033[31mInvalid room setting - something broke :(\033[0m")
        print(room.describe())
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

    print("\033[1m\033[4;35mThanks for playing! :)\033[0m")


# --------------------------------------------------------------------------------------------------------------------

rooms = {}

# Found In: Laboratory
# Used In: Control Room
keycard = Item("keycard",
               "An electronic keycard used to access locked areas.",
               "You pickup the keycard. It shines with a metallic sheen.",
               "You swipe the keycard, and the locked door clicks open.",
               "key",
               True,
               unlocked_directions=["north"])

# Found In: Captain's Quarters
# Used In: Security Office
access_code = Item("access code",
                   "A piece of paper with a code written on it.",
                   "You find a piece of paper with what looks like an access code written on it.",
                   "You enter the code and the door opens.",
                   "key",
                   unlocked_directions=["north"])

# Found In: Security Room
# Used In: Cargo Hold
security_card = Item("security card",
                     "A high-level security card used for accessing secured areas.",
                     "You found a security card! It grants access to highly restricted zones.",
                     "You slide the security card into the card reader, and the door unlocks.",
                     "key",
                     unlocked_directions=["west"])

# Found In: Lounge
# Used In: Medical Bay
code_breaker = Item("code breaker",
                    "A portable device capable of deciphering security codes.",
                    "You found a code breaker! It can bypass security systems.",
                    "With the code breaker, you easily decrypt the security code, granting access to the locked room.",
                    "key",
                    unlocked_directions=["west"])

# Found In: Observation Deck
# Used In: Engineering Bay
key = Item("key",
           "A standard looking golden key.",
           "You found a standard key. How quaint.",
           "You slide the key into the lock and turn it. The door unlocks with a click.",
           "key",
           True,
           unlocked_directions=["west"])

# Found In: Cargo Hold
# Used In: Medical Bay
password = Item("password",
                "A sticky note with a password sloppily scrawled onto it.",
                "You fold up the sticky note and put it into your pocket.",
                "You type the password into the computer. The slides open with a swish.",
                "key",
                unlocked_directions=["north"])

# Found In: Laboratory
# Used In: Captain's Quarters
cabinet_key = Item("cabinet key",
                   "A small key for a cabinet.",
                   "You found a small key! It appears to go to a cabinet of some kind.",
                   "You insert the key into the cabinet, unlocking the door and find a good old-fashioned key inside.",
                   "tool",
                   True,
                   revealed_objects=[key])

# Found In: Control Room
# Used In: Laboratory
cutter = Item("plasma cutter",
              "A handheld tool that emits a high-energy beam capable of cutting through metal.",
              "You found a plasma cutter! It can slice through sturdy materials.",
              "You activate the plasma cutter, and its energy blade effortlessly slices through the metal box.\nAfter cutting "
              "open the box, you see that there was a small key and a keycard hidden inside of the metal box.",
              "tool",
              revealed_objects=[keycard, cabinet_key])

# Found In: ID Badge Room
# Used In: The Escape Pods
id_card = Item("id card",
               "A small ID card with a picture of one of your former crewmates.",
               "You found an ID! Use it to access certain parts of the ship."
               "You scan the ID card with the reader on the escape pod...\nand the escape pod opens!!",
               "tool")

items = {"keycard": keycard,
         "access_code": access_code,
         "security_card": security_card,
         "code_breaker": code_breaker,
         "key": key,
         "password": password,
         "plasma_cutter": cutter,
         "cabinet_key": cabinet_key,
         "id_card": id_card}

# Lounge
r = Room("Lounge", [items["code_breaker"]], [], ["east"])
r.descriptions[(("code breaker",), ())] = f"{r.room_name} \u2014 You look around the room and see a " \
                                          "\033[0m\033[4;32m\033[1mcode breaker\033[3;35m."
r.descriptions[((), ())] = f"{r.room_name} \u2014 It doesn't look like there's anything of use in here..."
rooms[(0, 0, 0)] = r

# Observation Deck
r = Room("Observation Deck", [items["access_code"]], [], ["west", "north"])
base_description = f"{r.room_name} \u2014 There's a large window looking out into space. All you can really see through\n" \
                   "it though is the massive black hole that's pulling you in to your imminent demise. How charming.\n"
r.descriptions[(("access code",), ())] = base_description + "You also see a \033[0m\033[4;32m\033[1mpiece of paper\033[3;35m " \
                                                            "on the table in the corner."
r.descriptions[((), ())] = base_description
rooms[(1, 0, 0)] = r

# Medical Bay
r = Room("Medical Bay", [], [items["code_breaker"], items["password"]], ["south"])
base_description = f"{r.room_name} \u2014 Overturned or broken medical instruments and devices are strewn all over the room.\n"
r.descriptions[((), ("code breaker", "password"))] = base_description + "There's a door straight ahead with a " \
                                                                        "\033[0m\033[4;32m\033[1mcomputer connected to " \
                                                                        "it\033[3;35m, and a door to your left with a " \
                                                                        "note\non the keypad that says \033[34m\"Forgot " \
                                                                        "password to this door... Sorry for the inconvenience! " \
                                                                        ":)\"\n\033[3;35mOh, well that's just great!"
r.descriptions[((), ("password",))] = base_description + "There's a door straight ahead " \
                                                         "\033[0m\033[4;32m\033[1mcomputer connected to it\033[3;35m, " \
                                                         "and an open door to your left."
r.descriptions[((), ())] = base_description + "There are open doorways straight ahead of you and to your left."
rooms[(1, 1, 0)] = r

# Engineering Bay
r = Room("Engineering Bay", [], [items["access_code"]], ["east", "west"])
base_description = f"{r.room_name} \u2014 You find yourself in a spacious chamber filled with an array of advanced\n" \
                   "machinery, tools, and workbenches. The room hums with a symphony of whirring gears and electronic\nbeeps."
r.descriptions[((), ("access code",))] = base_description + " Straight ahead of you there's a set of locked double doors " \
                                                            "with a \033[0m\033[4;32m\033[1mkeypad\033[3;35m. There is also " \
                                                            "an\nopen doorway to your left that leads into what looks to be a " \
                                                            "lab of some kind."
r.descriptions[((), ())] = base_description + " Straight ahead of you there's an unlocked set of double doors, and to your " \
                                              "left there's an\nopen doorway that leads into what looks to be a lab of some kind."
rooms[(0, 1, 0)] = r

# Laboratory
r = Room("Laboratory", [items["keycard"], items["cabinet_key"]], [items["plasma_cutter"]], ["east"])
base_description = f"{r.room_name} \u2014 Stepping into the lab, you can't help but notice how eerily quiet it is. Rows " \
                   "of\nscientific equipment and workstations sit abandoned, untouched by human hands. Soft lighting\n" \
                   "casts shadows on the walls, adding to the sense of solitude. The air feels stagnant, hinting\nat the " \
                   "absence of bustling activity."
r.descriptions[(("keycard", "cabinet key"), ("plasma cutter",))] = base_description + " Hidden among some of the equipment, " \
                                                                                      "you see a \033[0m\033[4;32m\033[1mmysterious" \
                                                                                      "\nmetal box\033[3m."
r.descriptions[(("keycard", "cabinet key"), ())] = base_description + " There's a \033[0m\033[4;32m\033[1mkeycard\033[3;35m and a " \
                                                                      "\033[0m\033[4;32m\033[1msmall key\033[3;35m lying on the " \
                                                                      "table next\nto the sliced open metal box."
r.descriptions[(("keycard",), ())] = base_description + " There's a \033[0m\033[4;32m\033[1mkeycard\033[3;35m lying on " \
                                                        "the table next to the sliced\nopen metal box."
r.descriptions[(("cabinet key",), ())] = base_description + " There's a \033[0m\033[1m\033[4;32msmall key\033[3;35m " \
                                                            "lying on the table next to the sliced\nopen metal box."
r.descriptions[((), ())] = base_description + " There's a sliced open metal box discarded on the table."
rooms[(-1, 1, 0)] = r

# Control Room
r = Room("Control Room", [items["plasma_cutter"]], [items["keycard"]], ["south"])
base_description = f"{r.room_name} \u2014 An array of high-tech control panels, blinking lights, and holographic displays\n" \
                   "adorn the walls. The air is filled with the low buzz of machinery and the soft glow of monitors\nilluminates " \
                   "the room."
r.descriptions[(("plasma cutter",), ("keycard",))] = base_description + "In the corner, you spot a \033[0m\033[4;32m\033[1mplasma " \
                                                                        "cutter\033[3;35m resting on a workbench. On the far\n" \
                                                                        "side of the room is a locked door with a \033[0m\033[1m\033[4;32m" \
                                                                        "keycard reader\033[3;35m adjacent to it."
r.descriptions[((), ("keycard",))] = base_description + " On the far side of the room is a locked door with a " \
                                                        "\033[0m\033[4;32m\033[1mkeycard reader\033[3;35m adjacent\nto it."
r.descriptions[((), ())] = base_description + " There is an open doorway on the far side of the room."
rooms[(1, 2, 0)] = r

# Captain's Quarters
r = Room("Captain's Quarters", [items["key"]], [items["cabinet_key"]], ["south"])
base_description = f"{r.room_name} \u2014 The Captain's Quarters is an elegantly furnished sanctuary nestled within the\nspacecraft. " \
                   "The room exudes an air of authority, with polished wooden furniture and a commanding\nview of the stars through a " \
                   "panoramic window."
r.descriptions[(("key",), ("cabinet key",))] = base_description + " Adjacent to the desk, a \033[0m\033[4;32m\033[1m" \
                                                                          "locked cabinet\033[3;35m stands."
# r.descriptions[((), ("cabinet key",))]
r.descriptions[(("key",), ())] = base_description + " Inside of the unlocked cabinet is a \033[0m\033[4;32m\033[1m" \
                                                    "key\033[3;35m"
r.descriptions[((), ())] = base_description
rooms[(1, 3, 0)] = r

# Security Office
r = Room("Security Office", [items["security_card"]], [items["key"]], ["north", "south"])
base_description = f"{r.room_name} \u2014 The walls are covered with surveillance monitors displaying various sections of\n" \
                   "the vessel, ensuring constant vigilance. A sturdy desk holds the control panel for the security\nsystem, " \
                   "its array of buttons and switches ready to be engaged."
r.descriptions[(("security card",), ("key",))] = base_description + " Notably, a \033[0m\033[1m\033[4;32msecurity card\033[3;35m " \
                                                                    "lies\non the desk. There is also a little locked room to " \
                                                                    "your left that looks like it may have \033[0m\033[1m\033[4;32m" \
                                                                    "ID\nbadges\033[3;35m in it."
r.descriptions[((), ("key",))] = base_description + " There is also a little locked room\nto your left that looks like it " \
                                                    "may have \033[0m\033[1m\033[4;32mID badges\033[3;35m in it."
r.descriptions[(("security card",), ())] = base_description + " There is also an open doorway to\nyour left that leads to the ID Badge room."
r.descriptions[((), ())] = base_description + " There is also an open doorway to\nyour left that leads to the ID Badge room."
rooms[(0, 2, 0)] = r

# ID Room
r = Room("ID Room", [items["id_card"]], [], ["east"])
base_description = f"{r.room_name} \u2014 The room is meticulously organized, with lockers lining the walls, each bearing " \
                   f"the name\nand compartment of a crew member. At the heart of the room, a desk with a card printer hums quietly,\n" \
                   f"ready to produce or update ID badges."
r.descriptions[(("id card",), ())] = base_description + " Among the neatly arranged badges, you spot an \033[0m\033[1m\033[4;32m" \
                                                        "ID badges\033[3;35m left\nbehind."
r.descriptions[((), ())] = base_description
rooms[(-1, 2, 0)] = r

# Cargo Hold
r = Room("Cargo Hold", [items["password"]], [items["security_card"]], ["south"])
base_description = f"{r.room_name} \u2014 The room is filled with rows of storage containers, crates, and packages, stacked\n" \
                   "high and secured with sturdy straps."
r.descriptions[(("password",), ("security card",))] = base_description + " Amidst all the cargo, a specific \033[0m\033[1m\033[4;32m" \
                                                                         "piece of paper\033[3;35m catches your\neye for some " \
                                                                         "reason. Additionally, there is a locked room that requires " \
                                                                         "a \033[0m\033[1m\033[4;32msecurity badge\033[3;35m to your\nleft."
r.descriptions[(("password",), ())] = base_description + " Amidst all the cargo, a specific \033[0m\033[1m\033[4;32mpiece of paper" \
                                                         "\033[3;35m catches your\neye for some reason. There is also an " \
                                                         "unlocked doorway to your left that leads out to the escape\npods."
r.descriptions[((), ("security card",))] = base_description + " Additionally, there is also a locked doorway to your left\nthat " \
                                                             "leads out to the escape pods."
r.descriptions[((), ())] = base_description + "There is also an unlocked doorway to your left that " \
                                                                         "leads out\nto the escape pods."
rooms[(0, 3, 0)] = r

# Escape Pods
r = Room("Escape Pods", [], [items["id_card"]], ["east"])
base_description = f"{r.room_name} \u2014 The room is equipped with a series of sleek and streamlined escape pods, " \
                   f"arranged in\nan orderly fashion."
r.descriptions[((), ("id card",))] = base_description + "There's been a malfunction with the escape pods! You need to scan " \
                                                        "an \033[0m\033[1m\033[4;32mID badge\033[3;35m in\norder to override " \
                                                        "the safety protocols and jettison an escape pod with you in it."
r.descriptions[((), ())] = ""
rooms[(-1, 3, 0)] = r


if __name__ == "__main__":
    main()
    print("\nThanks for playing! :)")
