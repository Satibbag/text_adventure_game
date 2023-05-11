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
ACTIONS = ("quit",     # Quit the game
           "save",     # Save the current game
           "load",     # Load a previous game save
           "get",      # Add an item to the player's inventory
           "use",      # Use an item from the player's inventory
           "move",     # Display the possible movement options
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


rooms = {}

key = Item("key",
           "A golden key",
           "You pick up the key.",
           "You use the key to unlock the cellar door.",
           "key",
           unlocked_directions=["down"])

stick = Item("stick",
             "A brown stick",
             "You pick up the stick.",
             "You use the stick.")

items = {"key": key, "stick": stick}

# Entryway
r = Room("Entryway", [items["key"]], [items["stick"]], ["east"])
r.descriptions[(("key",), ("stick",))] = f"{r.room_name} - There's a mound of dirt."
r.descriptions[(("key",), ())] = f"{r.room_name} - An uncovered key with scattered dirt around it and a used stick."
r.descriptions[((), ())] = f"{r.room_name} - Scattered dirt and a used stick."
rooms[0, 0, 0] = r

# Room 1
r = Room("Room 1", [items["stick"]], [items["key"]], ["west"])
r.descriptions[(("stick",), ("key",))] = f"{r.room_name} - There's a locked cellar door and a stick on the ground."
r.descriptions[((), ("key",))] = f"{r.room_name} - There's a locked cellar door."
r.descriptions[((), ())] = f"{r.room_name} - There's an unlocked cellar door."
rooms[(1, 0, 0)] = r

# Cellar
r = Room("Cellar", allowed_movements=["up"])
r.descriptions[((), ())] = f"{r.room_name} - You beat the game!"
rooms[(1, 0, -1)] = r


if __name__ == "__main__":
    main()
