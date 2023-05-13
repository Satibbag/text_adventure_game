# Defines the Item class that will be used to generate item objects.
class Item:
    def __init__(self, name="", description_text="", pickup_text="", use_text="", obj_type="", **kwargs):
        self.name = name
        self.description_text = description_text
        self.pickup_text = pickup_text
        self.use_text = use_text
        self.obj_type = obj_type
        for arg in kwargs:
            if arg == "unlocked_directions":
                self.new_directions = kwargs[arg]

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
                print(f"You can now move {direction}!")
