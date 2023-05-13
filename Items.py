# Defines the Item class that will be used to generate item objects.
class Item:
    def __init__(self, name="", description_text="", pickup_text="", use_text="", obj_type="", hidden=False, **kwargs):
        self.name = name
        self.description_text = description_text
        self.pickup_text = pickup_text
        self.use_text = use_text
        self.obj_type = obj_type
        self.hidden = hidden
        self.revealed_objects = None
        for arg in kwargs:
            if arg == "unlocked_directions":
                self.new_directions = kwargs[arg]
            if arg == "revealed_objects":
                self.revealed_objects = kwargs[arg]

    # Returns the item's description text as the Item's string representation.
    def __str__(self):
        return self.description_text

    # Special function that does a different action depending on the
    # type of object that is defined.
    def special(self, curr_room):
        # Checks to see if the current object is a key.
        if self.obj_type == "key":
            for direction in self.new_directions:
                curr_room.allowed_movements.append(direction)
                print(f"\033[34mYou can now move {direction}!\033[0m")
        if self.revealed_objects:
            for revealed_object in self.revealed_objects:
                curr_room.room_items[curr_room.room_items.index(revealed_object)].hidden = False
