import math
import random
from location import *
from constants import *
from area import Workplace, Store, Outdoor
#from masked_area import Workplace, Store, Outdoor


def generate_stores(population, store_capacity, grid_size, houses):
    population_size = len([person for person in population])
    num_stores = math.ceil(population_size / store_capacity)
    house_coordinates = [(house.location.x, house.location.y) for house in houses]
    locations = [Location(x, y) for x in range(grid_size) for y in range(grid_size) if (x, y) not in house_coordinates]
    random.shuffle(locations)
    store_locations = locations[:num_stores]
    stores = []
    for location in store_locations:
        stores.append(Store(location))
    return stores

def assign_stores(population, stores):
    for person in population:
        available_stores = [store for store in stores if len(store.inhabitants) < STORE_CAPACITY] # strict less than because we don't reevaluate this after assigning, so this makes sure at least 1 place left
        nearest_store = min(available_stores, key=lambda store: person.house_location.distance_to(store.location))
        person.store_location = nearest_store.location
        nearest_store.inhabitants.append(person)

    
def generate_workplaces(population, workplace_capacity, grid_size, houses, stores):
    population_size = len([person for person in population if person.is_working_age])
    num_workplaces = math.ceil(population_size / workplace_capacity)
    house_coordinates = [(house.location.x, house.location.y) for house in houses]
    store_coordinates = [(store.location.x, store.location.y) for store in stores]
    locations = [Location(x, y) for x in range(grid_size) for y in range(grid_size) 
                 if (x, y) not in house_coordinates and (x, y) not in store_coordinates]
    
    random.shuffle(locations)
    workplace_locations = locations[:num_workplaces]
    workplaces = []
    for location in workplace_locations:
        workplaces.append(Workplace(location))
    return workplaces

def assign_workplaces(population, workplaces):
    for person in population:
        if person.is_working_age:
            available_workplaces = [workplace for workplace in workplaces if len(workplace.inhabitants) < WORKPLACE_CAPACITY]
            nearest_workplace = min(available_workplaces, key=lambda workplace: person.house_location.distance_to(workplace.location))
            person.workplace_location = nearest_workplace.location
            nearest_workplace.inhabitants.append(person)


def generate_outdoors(grid_size, houses, stores, workplaces):
    building_coordinates = [(building.location.x, building.location.y) for building in houses + stores + workplaces]
    locations = [Location(x, y) for x in range(grid_size) for y in range(grid_size)
                 if (x, y) not in building_coordinates]
    outdoors = []
    for location in locations:
        outdoors.append(Outdoor(location))
    return outdoors

