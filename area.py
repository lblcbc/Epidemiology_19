import numpy as np


class Area:
    def __init__(self, location):
        self.location = location
        self.inhabitants = []

    area_dict = {}

    @staticmethod # Means it doesn't depend on instance self
    def setup_area_dict(houses, workplaces, stores, outdoors):
        Area.area_dict = {
            House: {"location_attribute": "house_location", "list": houses},
            Workplace: {"location_attribute": "workplace_location", "list": workplaces},
            Store: {"location_attribute": "store_location", "list": stores},
            Outdoor: {"location_attribute": "outdoor_location", "list": outdoors}
        }

    # Didn't really end up using area_dict functionality, but was created in part of code production

    @staticmethod
    def move_out(person, area_type):
        target_location = getattr(person, Area.area_dict[area_type]['location_attribute'])
        area_list = Area.area_dict[area_type]['list']

        for area in area_list:
            if area.location == target_location:
                area.inhabitants.remove(person)
                break # For efficiency so it doesn't keep searching through area_list once correct area found

    @staticmethod
    def move_in(person, area_type):
        target_location = getattr(person, Area.area_dict[area_type]['location_attribute'])
        area_list = Area.area_dict[area_type]['list']

        for area in area_list:
            if area.location == target_location:
                area.inhabitants.append(person)
                person.location = target_location
                break


class House(Area):
    def __init__(self, location):
        super().__init__(location)
        self.symbol = "H"

    def scaled_infection_probability(self, interactions, max_prob = 0.60, steepness = 0.5, midpoint = 0):
        if interactions == 0:
            return 0
        else:
            return max_prob / (1 + np.exp(-steepness * (interactions - midpoint)))
        
class Workplace(Area):
    def __init__(self, location):
        super().__init__(location)
        self.symbol = "W"

    def scaled_infection_probability(self, interactions, max_prob = 0.42, steepness = 0.3, midpoint = 0):
        if interactions == 0:
            return 0
        else:
            return max_prob / (1 + np.exp(-steepness * (interactions - midpoint)))
        
class Store(Area):
    def __init__(self, location):
        super().__init__(location)
        self.symbol = "S"

    def scaled_infection_probability(self, interactions, max_prob = 0.07, steepness = 0.3, midpoint = 0):
        if interactions == 0:
            return 0
        else:
            return max_prob / (1 + np.exp(-steepness * (interactions - midpoint)))
        
class Outdoor(Area):
    def __init__(self, location):
        super().__init__(location)
        self.symbol = "-"

    def scaled_infection_probability(self, interactions, max_prob = 0.05, steepness = 0.3, midpoint = 8):
        if interactions == 0:
            return 0
        else:
            return max_prob / (1 + np.exp(-steepness * (interactions - midpoint)))

