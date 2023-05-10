# Main program where the game runs from.

# Import the necessary modules.
# Import numpy.array() so that I can do matrix math.
from numpy import array
# Import pickle in order to enable persistent storage.
import pickle
# Import the rooms and MOVEMENT variables from the Rooms.py file.
from Rooms import rooms, MOVEMENT
# Import the Player object.
from Player import player

# Define the possible player actions.
ACTIONS = ("quit",     # Quit the game
           "save",     # Save the current game
           "load",     # Load a previous game save
           "get",      # Add an item to the player's inventory
           "use",      # Use an item from the player's inventory
           "move",     # Display the possible movement options
           "inspect",  # Inspect an item in the current room
           )


def valid_input(prompt="What would you like to do?\n> "):
    """Forces the player to select a valid action."""
    print("\u2014" * 14 + "COMMANDS" + "\u2014" * 14)
    response = None
    while response not in ACTIONS and response not in list(map(lambda action: action[0], ACTIONS)):
        print("Actions:")
        for action in ACTIONS:
            print(f"* {action} ({action[0]})")
        response = input(prompt).lower()
    return response


def save():
    """Save the Player object and the rooms dictionary to a file."""
    with open('game.dat', 'wb') as file:
        pickle.dump(player, file)
        pickle.dump(rooms, file)
    print("Game successfully saved!")


def load():
    """Load the Player object and the rooms dictionary from a file."""
    # Using global variables in order to reduce the size.
    global player
    global rooms
    try:
        with open("game.dat", "rb") as file:
            player = pickle.load(file)
            rooms = pickle.load(file)
        print("Game successfully loaded!")
    except FileNotFoundError:
        print("Game file not found! :(")


def main(player_object):
    """Main game loop"""
    choice = None
    while choice != "quit":
        # Unpack the current room variables.
        room = rooms.get(player.position, "Invalid room setting - something broke :(")
        print(room.describe())
        choice = valid_input()
        if choice == "quit" or choice == "q":
            print("Thanks for playing! :)")
        elif choice == "save" or choice == "s":
            save()
        elif choice == "load" or choice == "l":
            load()
        elif choice == "get" or choice == "g":
            print("\nGETTING")
            room.get_item(player_object)
        elif choice == "use" or choice == "u":
            print("\nUSING")
            room.use_item(player_object)
        elif choice == "move" or choice == "m":
            print("\nMOVING")
            room.move(player_object)
        elif choice == "inspect" or choice == "i":
            print("\nINSPECTING")
            room.inspect_item(player_object)


if __name__ == "__main__":
    main(player)
