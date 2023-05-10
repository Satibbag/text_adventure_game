# Import the necessary modules.
# Import the Item class so that Items can be generated.
from Items import Item
# Importing numpy.array() so that I can do matrix math.
from numpy import array

# Define the possible movement commands and their
# respective arrays.
MOVEMENT = {"north": array([0, 1, 0]),
            "south": array([0, -1, 0]),
            "east": array([1, 0, 0]),
            "west": array([-1, 0, 0])}


# Define the Room class that will be used to generate
# rooms.
class Room:
    """Base Room Object"""

    def __init__(self, room_items=None, usable_items=None,
                 allowed_movements=None, descriptions=None):
        # Initialize the room_items list if no value for room_items is given.
        if room_items is None:
            room_items = []
        # Initialize the usable_items list if no value for usable_items is given.
        if usable_items is None:
            usable_items = []
        # Initialize the allowed_movements list if no value for allowed_movements is given.
        if allowed_movements is None:
            allowed_movements = []
        # Initialize the descriptions dictionary if no value for descriptions is given.
        if descriptions is None:
            descriptions = {}

        self.room_items = room_items  # Items that are in the room.
        # Define the room_items_names list.
        self.room_items_names = []
        for item in self.room_items:
            self.room_items_names.append(item.name)

        self.usable_items = usable_items  # Usable items
        # Define the usable_items_names list.
        self.usable_items_names = []
        for usable_item in self.usable_items:
            self.usable_items_names.append(usable_item.name)

        self.allowed_movements = allowed_movements  # The possible valid movement directions
        self.descriptions = descriptions  # (room_items,usable_items) : description text

    #     def __str__(self):
    #         pass

    def get_item(self, player):
        """Gets an item from the room and adds it to the player's inventory."""
        # TODO: List the items in the room that the player can pick up.
        # Checks to see if there are items in the current room.
        if self.room_items:
            # Lists the items in the room as a bulleted list.
            for item in self.room_items:
                print(f"* {item.name}")
            # Asks the user which item they would like to pickup.
            picked_item = input("What item would you like to pick up?\n> ").lower().strip()
            # Checks to see if the inputted item is a valid item in the room.
            if picked_item in self.room_items_names:
                # Loops through the list of items in the room.
                for item in self.room_items:
                    # Checks to see if the current item is the one the user inputted.
                    if item.name == picked_item:
                        # Displays the pickup_text for the item that the player picked up.
                        print(item.pickup_text)
                        # Adds the picked up item to the player's inventory.
                        player.inventory.append(item)
                        # Removes the picked up item from the list of items in the room.
                        self.room_items.remove(item)
                        # Removes the name of the picked up item from the list of item names in the room.
                        self.room_items_names.remove(picked_item)
            else:
                # Displays a message if the inputted item isn't a valid item.
                print(f"Couldn't find the {picked_item} item in the room.")
        else:
            # Displays a message if there aren't any items to pickup in the room.
            print("There aren't any items to pick up.\n")

    def use_item(self, player):
        """Use an item from the player's inventory."""
        # Checks to see if there are items in the player's inventory.
        if player.inventory:
            # Displays the player's current inventory as a bulleted list.
            print("Your current inventory:")
            for item in player.inventory:
                print(f"* {item.name}")
            # Asks the user which item they would like to use.
            used_item = input("What item would you like to use?\n> ").lower().strip()

            print(player.inventory_names)

            # Checks to see if the inputted item is a valid item in the player's inventory.
            if used_item in player.inventory_names:
                # Checks to see if the inputted item is a valid usable item.
                if used_item in self.usable_items_names:
                    # Loops through the list of items in the player's inventory.
                    for item in player.inventory:
                        # Checks to see if the current item is the one the user inputted.
                        if item.name == used_item:
                            # Displays the use_text for the item that the player used.
                            print(item.use_text)
                            # Removes the used item from the player's inventory.
                            player.inventory.remove(item)
                            # Removes the used item's name from the list of names of items in
                            # the player's inventory.
                            player.inventory_names.remove(used_item)
                            # Removes the used item from the list of usable items in the room.
                            self.usable_items.remove(item)
                            # Removes the used item's name from the list of names of usable items.
                            self.usable_items_names.remove(used_item)
                            # Runs a special action depending on the type of object that was used.
                            item.special(item, self)
                else:
                    # Displays a message if the inputted item isn't a valid usable item.
                    print(f"The {used_item} item isn't a usable item.\n")
        else:
            # Displays a message if there aren't any items in the player's inventory.
            print("There aren't any items in your inventory.\n")

    # noinspection DuplicatedCode
    def inspect_item(self, player):
        """Describe an item in the current room or the player's inventory."""
        # Asks the user if they would like to inspect an item in the room or in their inventory.
        room_or_inventory = input("Would you like to inspect an item in the room or "
                                  "in your inventory?\n> ").lower().strip()
        # Checks to see if the user wants to inspect an item in the room or in their inventory.
        if room_or_inventory == "room" or room_or_inventory == "r":
            # Checks to see if there are items in the current room.
            if self.room_items:
                print("Which item in the room would you like to inspect?")
                # Displays the items in the current room as a bulleted list.
                for item in self.room_items:
                    print(f"* {item.name}")
                # Asks the user which item in the room they would like to inspect
                inspected_item = input("> ").lower().strip()
                # Checks to see if the inputted item is a valid item in the room.
                if inspected_item in self.room_items_names:
                    # Loops through the list of items in the room.
                    for item in self.room_items:
                        # Checks to see if the current item is the one the user inputted.
                        if item.name == inspected_item:
                            # Displays the description_text for the item that the player inspected.
                            print(item.description_text)
                else:
                    # Displays a message if the inputted item isn't a valid item.
                    print(f"Couldn't find the {inspected_item} item in the room.\n")
            # Displays a message if there aren't any items to inspect in the room.
            print("There aren't any items in the room to inspect.\n")

        elif room_or_inventory == "inventory" or room_or_inventory == "i":
            # Checks to see if there are items in the player's inventory.
            if player.inventory:
                print("Which item in your inventory would you like to inspect?")
                # Displays the items in the player's inventory as a bulleted list.
                for item in player.inventory:
                    print(f"* {item.name}")
                # Asks the user which item in their inventory they would like to inspect.
                inspected_item = input("> ").lower().strip()
                # Checks to see if the inputted item is a valid item in the player's inventory.
                if inspected_item in player.inventory_names:
                    # Loops through the list of items in the player's inventory.
                    for item in player.inventory:
                        # Checks to see if the current item is the one the user inputted.
                        if item.name == inspected_item:
                            # Displays the description_text for the item the player inspected.
                            print(item.description_text)
                else:
                    # Displays a message if the inputted item isn't a valid item.
                    print(f"Couldn't find the {inspected_item} item in your inventory.\n")
            # Displays a message if there aren't any items to inspect in the room.
            print("There aren't any items in your inventory to inspect.\n")

    # TODO: Add an "inventory" command that allows the player to view the items currently in their inventory.

    def move(self, player):
        """Asks the player which way they would like to move."""
        # Tells the user which directions they can move in as a bulleted list.
        print("You can go in the following directions:")
        for direction in self.allowed_movements:
            print(f"* {direction}")
        # Asks the user which direction they would like to move in.
        inputted_direction = input("Which direction would you like to move?\n> ").lower().strip()
        # Checks to see if the inputted direction is a valid movement direction.
        if inputted_direction in MOVEMENT:
            # Checks to see if the inputted direction is an allowed movement direction in
            # the current room.
            if inputted_direction in self.allowed_movements:
                # Informs the user which direction they moved in.
                print(f"You move {inputted_direction}.")
                # Updates the player's current position.
                player.position = MOVEMENT[inputted_direction]

            else:
                # Displays a message if the inputted direction isn't an allowed movement.
                print(f"You can't move {inputted_direction} from here.\n")
        else:
            # Displays a message if the inputted direction isn't a valid movement direction.
            print(f"'{inputted_direction}' isn't a valid direction.\n")

    def describe(self):
        # Generates a key to represent the current state of the room (which items are
        # in the room and which items in the room are usable).
        description_key = tuple(self.room_items_names), tuple(self.usable_items_names)
        # Returns a description of the room based off of the current state of the room.
        return "\n\u2014" * 100 + "\n" + self.descriptions.get(description_key, "Invalid  room setting - something broke :(") \
            + "\n" + "\u2014" * 100

    # TODO: Add a "clear" command that clears previous outputs from the terminal screen.


rooms = {}

# -----------------------------------------------
key = Item("key",
           "A golden key",
           "You pick up the key.",
           "You use the key to unlock the cellar door.")
stick = Item("stick",
             "A brown stick",
             "You pick up the stick.",
             "You use the stick.")

# Entryway
r = Room([key], [stick], ["east"])
# Error if key picked up before the stick is used.
r.descriptions[(("key",), ("stick",))] = "Entry: There's a mound of dirt."
r.descriptions[(("key",), ())] = "Enry: An uncovered key with scattered dirt around it and a used stick."
r.descriptions[((), ())] = "Entry: Scattered dirt and a used stick."
rooms[(0, 0, 0)] = r

# Room 1
r = Room([stick], [key], ["west"])
r.descriptions[(("stick",), ("key",))] = "Room 1 - There's a locked cellar door and a stick on the ground."
r.descriptions[((), ("key",))] = "Room 1 - There's a locked cellar door."
r.descriptions[((), ())] = "Room 1 - There's an unlocked cellar door, you can now move \"down\"."
rooms[(1, 0, 0)] = r

# Cellar
r = Room(allowed_movements=["up"])
r.descriptions[((), ())] = "Cellar - You beat the game!"
rooms[(1, 0, -1)] = r
