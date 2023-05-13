# Import the necessary modules.
# Import numpy.array() so that I can properly store the movement directions.
from numpy import array

# Define the possible movement commands and their
# respective arrays.
MOVEMENT = {"north": array([0, 1, 0]),
            "south": array([0, -1, 0]),
            "east": array([1, 0, 0]),
            "west": array([-1, 0, 0]),
            "up": array([0, 0, 1]),
            "down": array([0, 0, -1])}


# Defines the Room class that will be used to generate room objects.
class Room:
    """Base Room Object"""

    def __init__(self, room_name="", room_items=None, usable_items=None,
                 allowed_movements=None, descriptions=None, unlocked=False):
        self.room_name = room_name  # The name of the room.

        if room_items is None:
            room_items = []
        if usable_items is None:
            usable_items = []
        if allowed_movements is None:
            allowed_movements = []
        if descriptions is None:
            descriptions = {}

        self.room_items = room_items  # Items that are in the room.
        self.room_items_names = []
        for item in self.room_items:
            self.room_items_names.append(item.name.lower())

        self.usable_items = usable_items  # Usable items
        self.usable_items_names = []
        for usable_item in self.usable_items:
            self.usable_items_names.append(usable_item.name.lower())

        self.allowed_movements = allowed_movements  # The possible valid movement directions
        self.descriptions = descriptions  # (room_items,usable_items) : description text

        self.unlocked = unlocked

    def __str__(self):
        """Purely for debugging purposes."""
        description_strings = ""
        for description_string in self.descriptions:
            description_strings += f"\n{description_string} \u2014 {self.descriptions[description_string]}"

        current_description_key = tuple(self.room_items_names), tuple(self.usable_items_names)
        current_description_text = self.descriptions.get(current_description_key, "\033[31mInvalid room setting - something broke :(\033[0m")

        return "ROOM\n"\
               f"Room Name: {self.room_name}\n" \
               f"Room Items: {self.room_items}\n" \
               f"Room Item Names: {self.room_items_names}\n" \
               f"Usable Items: {self.usable_items}\n" \
               f"Usable Item Names: {self.usable_items_names}\n" \
               f"Allowed Movements: {self.allowed_movements}\n" \
               f"Descriptions: {description_strings}\n" \
               f"Current Description: {current_description_text}"

    def unlock(self, new_directions):
        """Adds new possible directions to a room once a certain part of it is unlocked."""
        if self.unlocked:
            for direction in new_directions:
                self.allowed_movements.append(direction)

    def get_item(self, player):
        """Gets an item from the room and adds it to the player's inventory."""
        if self.room_items:
            all_hidden = True
            for item in self.room_items:
                if not item.hidden:
                    all_hidden = False
            if all_hidden:
                print("\033[31mThere aren't any items to pick up.\n\033[0m")
                return
            print("What item would you like to pick up?")
            for item in self.room_items:
                if item.hidden:
                    continue
                print(f"\033[36m* {item.name.title()}\033[0m")
            picked_item = input("> ").lower().strip()

            if picked_item == "cancel":
                return

            if picked_item in self.room_items_names:
                for item in self.room_items:
                    # Checks to see if the current item is the one the user inputted.
                    if item.name.lower() == picked_item:
                        # Displays the pickup_text for the item that the player picked up.
                        print(f"\033[0;32m{item.pickup_text}\033[0m")
                        # Adds the picked up item to the player's inventory.
                        player.inventory.append(item)
                        # Adds the picked up item's name to the player's inventory names list.
                        player.inventory_names.append(item.name)
                        # Removes the picked up item from the list of items in the room.
                        self.room_items.remove(item)
                        # Removes the name of the picked up item from the list of item names in the room.
                        self.room_items_names.remove(picked_item)
            else:
                # Displays a message if the inputted item isn't a valid item.
                print(f"\033[31mCouldn't find the {picked_item} item in the room.\033[0m")

        else:
            # Displays a message if there aren't any items to pickup in the room.
            print("\033[31mThere aren't any items to pick up.\n\033[0m")

    def use_item(self, player):
        """Use an item from the player's inventory."""
        if player.inventory:
            self.view_inventory(player)
            used_item = input("What item would you like to use?\n"
                              "(Note: After you use an item, you can't pick it up again.)\n> ").lower().strip()

            if used_item == "cancel":
                return

            if used_item in player.inventory_names:
                if used_item in self.usable_items_names:
                    # Loops through the list of items in the player's inventory.
                    for item in player.inventory:
                        # Checks to see if the player has won the game.
                        if item.name.lower().strip() == "id card":
                            player.won = True
                            return
                        # Checks to see if the current item is the one the user inputted.
                        if item.name.lower().strip() == used_item:
                            # Displays the use_text for the item that the player used.
                            print(f"\033[0;32m{item.use_text}\033[0m")
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
                            item.special(self)
                else:
                    # Displays a message if the inputted item isn't a valid usable item.
                    print(f"\033[31mThe {used_item} item isn't a usable item in this room.\n\033[0m")
            else:
                # Displays a message if the inputted item isn't a valid item in the player's inventory.
                print(f"\033[31mCould not find the {used_item} item in your inventory.\033[0m")

        else:
            # Displays a message if there aren't any items in the player's inventory.
            print("\033[31mThere aren't any items in your inventory.\n\033[0m")

    def inspect_item(self, player):
        """Describe an item in the current room or the player's inventory."""
        room_or_inventory = input("Would you like to inspect an item in the room or "
                                  "in your inventory?\n> ").lower().strip()

        if room_or_inventory == "cancel":
            return

        if room_or_inventory == "room" or room_or_inventory == "r":
            if self.room_items:
                print("Which item in the room would you like to inspect?")
                for item in self.room_items:
                    print(f"\033[36m* {item.name.title()}\033[0m")
                inspected_item = input("> ").lower().strip()

                if inspected_item == "cancel":
                    return

                if inspected_item in self.room_items_names:
                    # Loops through the list of items in the room.
                    for item in self.room_items:
                        # Checks to see if the current item is the one the user inputted.
                        if item.name.lower().strip() == inspected_item:
                            # Displays the description_text for the item that the player inspected.
                            print(f"\033[34m{item.description_text}\033[0m")
                else:
                    # Displays a message if the inputted item isn't a valid item.
                    print(f"\033[31mCouldn't find the {inspected_item} item in the room.\n\033[0m")

            else:
                # Displays a message if there aren't any items to inspect in the room.
                print("\033[31mThere aren't any items in the room to inspect.\n\033[0m")

        elif room_or_inventory == "inventory" or room_or_inventory == "i":
            if player.inventory:
                print("Which item in your inventory would you like to inspect?")
                self.view_inventory(player)
                inspected_item = input("> ").lower().strip()

                if inspected_item == "cancel":
                    return

                if inspected_item in player.inventory_names:
                    # Loops through the list of items in the player's inventory.
                    for item in player.inventory:
                        # Checks to see if the current item is the one the user inputted.
                        if item.name.lower().strip() == inspected_item:
                            # Displays the description_text for the item the player inspected.
                            print(f"\033[34m{item.description_text}\033[0m")
                else:
                    # Displays a message if the inputted item isn't a valid item.
                    print(f"\033[31mCouldn't find the {inspected_item} item in your inventory.\n\033[0m")

            else:
                # Displays a message if there aren't any items to inspect in the room.
                print("\033[31mThere aren't any items in your inventory to inspect.\n\033[0m")

    def view_inventory(self, player):
        """Display the player's inventory as a bulleted list."""
        if player.inventory:
            print("Your current inventory:")
            for item in player.inventory:
                print(f"\033[36m* {item.name.title()}\033[0m")
        else:
            print("\033[31mThere are no items currently in your inventory.\n\033[0m")

    def move(self, player):
        """Asks the player which way they would like to move."""
        print("You can go in the following directions:")
        for direction in self.allowed_movements:
            print(f"* {direction.title()}")

        inputted_direction = input("Which direction would you like to move?\n> ").lower().strip()

        if inputted_direction == "cancel":
            return

        if inputted_direction in MOVEMENT:
            # Checks to see if the inputted direction is an allowed movement direction in
            # the current room.
            if inputted_direction in self.allowed_movements:
                # Informs the user which direction they moved in.
                print(f"\033[34mYou move {inputted_direction.title()}.\033[0m")
                # Updates the player's current position.
                player.position = MOVEMENT[inputted_direction]
            else:
                # Displays a message if the inputted direction isn't an allowed movement.
                print(f"\033[31mYou can't move {inputted_direction} from here.\n\033[0m")
        else:
            # Displays a message if the inputted direction isn't a valid movement direction.
            print(f"\033[31m'{inputted_direction}' isn't a valid direction.\n\033[0m")

    def describe(self):
        """Describes the room the player is in based off of the current state of the room (which items are in the room and which items in the room are usable)."""
        # Generates a key to represent the current state of the room.
        description_key = tuple(self.room_items_names), tuple(self.usable_items_names)
        print(description_key)
        description_text = f"\033[4m\033[3;35m{self.descriptions.get(description_key, 'Invalid room setting - something broke :(')}\033[0m"

        # Returns a description of the room based off of the current state of the room.
        return "\n" + "\033[1m\u2014" * 100 + "\n" + description_text + "\n" + "\u2014" * 100 + "\033[0m"
