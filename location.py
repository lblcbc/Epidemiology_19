import math

class Location:
    def __init__(self, x, y, area_type="Outdoor"):
        self.x = x
        self.y = y
        self.area_type = area_type

    def distance_to(self, other_location):
        return math.sqrt((self.x - other_location.x) ** 2 + (self.y - other_location.y) ** 2)
    
    def __eq__(self, other_location): # Facilitates comparing of two locations
        if isinstance(other_location, Location):
            return self.x == other_location.x and self.y == other_location.y
        return False
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
