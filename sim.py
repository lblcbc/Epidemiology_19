import random
import math
import numpy as np
from termcolor import colored


POPULATION_SIZE = 100
GRID_SIZE = 10
STORE_CAPACITY = 20
WORKPLACE_CAPACITY = 14
INITIAL_INFECTIONS = 0.05*POPULATION_SIZE

AGE_DISTRIBUTION = [0.16, 0.17, 0.158, 0.140, 0.120, 0.108, 0.08, 0.04, 0.014, 0.01]
AGE_DISTRIBUTION_EXPANDED = [weight for weight in AGE_DISTRIBUTION for _ in range(10)]  # Repeat each weight 10 times

NUM_DAYS = 50

# Location class, represents single points on the grid
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
    


class Area:
    def __init__(self, location):
        self.location = location
        self.inhabitants = []

    area_dict = {}

    @staticmethod # means it doesn't depend on instance self
    def setup_area_dict(houses, workplaces, stores, outdoors):
        Area.area_dict = {
            House: {"location_attribute": "house_location", "list": houses},
            Workplace: {"location_attribute": "workplace_location", "list": workplaces},
            Store: {"location_attribute": "store_location", "list": stores},
            Outdoor: {"location_attribute": "outdoor_location", "list": outdoors}
        }
    # Function allows me to set it up in simulation where I will have houses, workaplces, store, outdoors etc, 
    # and House Workpalce store Outdoor etc will have been defined by then

    @staticmethod
    def move_out(person, area_type):
        target_location = getattr(person, Area.area_dict[area_type]['location_attribute'])
        area_list = Area.area_dict[area_type]['list']

        for area in area_list:
            if area.location == target_location:
                area.inhabitants.remove(person)
                break # for efficiency so it doesn't keep searching through area_list once correct area found

    @staticmethod
    def move_in(person, area_type):
        target_location = getattr(person, Area.area_dict[area_type]['location_attribute'])
        area_list = Area.area_dict[area_type]['list']

        for area in area_list:
            if area.location == target_location:
                area.inhabitants.append(person)
                person.location = target_location
                break

    
    @staticmethod
    def calculate_infections(areas):
        for area in areas:
            for person in area.inhabitants:
                if not person.infected:
                    infected_count = len([person for person in area.inhabitants if person.infected])
                    person.interactions += infected_count - 1
                    person.infection_probability = area.scaled_infection_probability(person.interactions)
                    person.determine_infection(person.infection_probability)



class House(Area):
    def __init__(self, location):
        super().__init__(location)
        self.symbol = "H"

    def scaled_infection_probability(self, interactions, max_prob = 0.6, steepness = 0.5, midpoint = 0):
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



class Population:
    def __init__(self, age, id=None):
        self.age = age
        self.id = id
        self.is_kid = 1 <= self.age < 20
        self.is_young = 20 <= self.age < 26 
        self.is_parent = 26 <= self.age < 53
        self.is_grandparent = 53 <= self.age
        self.is_adult = 20 <= self.age
        self.is_working_age = 20 <= self.age <= 65 # we ignore university, we will only have school for kids
        self.parents = []
        self.grandparents = []
        self.location = None
        self.house_location = None
        self.workplace_location = None
        self.store_location = None
        self.outdoor_location = None
        self.is_working = False
        self.is_shopping = False
        self.interactions = 0
        self.infection_probability = 0
        self.infected = False
        self.infected_today = False
    
    def determine_infection(self, infection_probability):
        if random.random() < infection_probability:
            self.infected = True



def generate_population_and_assign_houses(population_size, grid_size):
    # Generate the population ages
    population = []
    ages = random.choices(
        population=range(1, 101), # Assuming peopl live up to 100
        weights=AGE_DISTRIBUTION_EXPANDED,
        k=population_size
    )
    for age in ages:
        population.append(Population(age))

    population.sort(key=lambda x: x.age, reverse=True)

    for i, person in enumerate(population): # We use enumerate as it allows us, for each iteration to get both the current index (id) and the current element (person)
        person.id = i
    
    # Divide the population into kids, adults, and elders
    parents = [person for person in population if person.is_parent]
    kids = [person for person in population if person.is_kid]
    youngs = [person for person in population if person.is_young]
    grandparents = [person for person in population if person.is_grandparent]

    random.shuffle(parents)
    random.shuffle(kids)

    all_grandparents = []
    all_parents = []  # List to store all parents for assigning their parents later
    all_youngs = []  # List to store all youngs for assigning their grandparents later
    all_kids = [] # List to store all kids for assigning their grandparents later

    # Form family units with adults and kids, assign them to houses
    houses = []
    while parents or kids:
        house = House(None)

        # Decide how many parents will live in this house - either two or the remaining number of parents
        num_parents = 2 if len(parents) >= 2 else len(parents)

        # If there's only one or two parents left, they will take all the remaining kids
        if len(parents) not in {1, 2}:
            num_kids = random.randint(1, 4)  # Select 1-4 kids
        else:  # Otherwise, decide randomly how many kids will live in this house
            num_kids = len(kids) # This means that total number in house may be more than 2+4 (ex. 1 + 6 or smth), given how the randoms may occur

        # Add parents to the house
        current_parents = []  # List to keep track of the parents currently being added to the house
        for _ in range(num_parents):  
            if parents:
                parent = parents.pop()
                parent.house_location = house.location
                house.inhabitants.append(parent)
                current_parents.append(parent)  # Add each parent to the current_parents list
                all_parents.append(parent)  # Add each parent to the all_parents list

        # Add kids to the house and assign them parents
        for _ in range(num_kids):
            if kids:
                kid = kids.pop()
                kid.house_location = house.location
                house.inhabitants.append(kid)
                for parent in current_parents:  # Assign all current parents to the kid
                    kid.parents.append(parent)
                all_kids.append(kid)

        houses.append(house)

    # Assign youngs to a separate house and link them to 
    while youngs:
        for young in youngs:
            house = House(None)
            for _ in range(2):
                if youngs:
                    young = youngs.pop()
                    young.house_location = house.location
                    house.inhabitants.append(young)
            houses.append(house)
            all_youngs.append(young)  # Add each young to the all_youngs list

    # Assign each elder to a separate house and link them to adults
    while grandparents:
        num_grandparents = random.randint(1, 2)
        house = House(None)
        current_grandparents = [] # Temporary list to keep track of grandparents in this iteration

        for _ in range(num_grandparents):
            if grandparents:
                grandparent = grandparents.pop()
                grandparent.house_location = house.location
                house.inhabitants.append(grandparent)
                current_grandparents.append(grandparent)
                all_grandparents.append(grandparent)
        
        houses.append(house)

        # Link each grandparent in a house to parent and kid or young adults
        parents_wo_grandparents = [parent for parent in all_parents if len(parent.parents) == 0]
        youngs_wo_grandparents = [young for young in all_youngs if len(young.grandparents) == 0]

        if parents_wo_grandparents and youngs_wo_grandparents:
            if random.choice([True, False]):
                    random_parent = random.choice(parents_wo_grandparents)
                    for grandparent in current_grandparents: 
                        random_parent.parents.append(grandparent)
            
                        for kid in all_kids:
                            if random_parent in kid.parents and grandparent not in kid.grandparents:
                                kid.grandparents.append(grandparent)                
            else:
                random_young = random.choice(youngs_wo_grandparents)
                for grandparent in current_grandparents: 
                    random_young.grandparents.append(grandparent)
        
        elif parents_wo_grandparents:
            random_parent = random.choice(parents_wo_grandparents)
            for grandparent in current_grandparents:
                random_parent.parents.append(grandparent)
    
                for kid in all_kids:
                    if random_parent in kid.parents and grandparent not in kid.grandparents:
                        kid.grandparents.append(grandparent)
        
        elif youngs_wo_grandparents:
            random_young = random.choice(youngs_wo_grandparents)
            for grandparent in current_grandparents:
                random_young.grandparents.append(grandparent)

    # Generate random locations
    locations = [Location(x, y) for x in range(grid_size) for y in range(grid_size)]
    random.shuffle(locations)

    # Now assign the random locations to the houses
    for house, location in zip(houses, locations):
        house.location = location
        for inhabitant in house.inhabitants:
            inhabitant.house_location = location

    return population, houses


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


def simulate_day(population, houses, workplaces, stores, outdoors, num_days):
    for area in stores + workplaces + outdoors: # for areas not houses, as inhabitants for other areas just used to check and satisfy area capacities
        area.inhabitants = []

    # Set up building dict
    Area.setup_area_dict(houses, workplaces, stores, outdoors)

    # Initially infected population
    initally_infected = random.sample(population, int(INITIAL_INFECTIONS))
    for person in initally_infected:
        person.infected = True

    for person in population:
        person.location = person.house_location
        if person.is_working_age:
            if random.random() < 0.6:
                person.is_working = True

    for day in range(num_days):
        for step in range(4):
            if step == 0:
                for person in population:
                    person.interactions = 0
                    person.infection_probability = 0
                
                healthy_count = len([person for person in population if not person.infected])
                infection_count = len([person for person in population if person.infected])
                # here i will append these counts to a plot, only here at step == 0 so 1 a day, not at the next steps
                print(f"Day: {day}, Step: {step}, Healthy: {healthy_count}, Infected: {infection_count}")
                print_grids(houses, stores, workplaces, outdoors, GRID_SIZE)

            elif step == 1:
                for person in population:
                    if person.is_working:
                        Area.move_out(person, House)
                        Area.move_in(person, Workplace) # remember this automatically updates the persons location too!

                    if person.is_adult and random.random() < 0.4:
                        person.is_shopping = True

                    if person.is_shopping and not person.is_working:
                        Area.move_out(person, House)
                        Area.move_in(person, Store)

                Area.calculate_infections(workplaces)
                Area.calculate_infections(stores)

                healthy_count = len([person for person in population if not person.infected])
                infection_count = len([person for person in population if person.infected])
                print(f"Day: {day}, Step: {step}, Healthy: {healthy_count}, Infected: {infection_count}")
                print_grids(houses, stores, workplaces, outdoors, GRID_SIZE)

            elif step == 2:
                for person in population:
                    if person.is_shopping and not person.is_working:
                        Area.move_out(person, Store)
                        Area.move_in(person, House)

                    elif person.is_working and not person.is_shopping:
                        Area.move_out(person, Workplace)
                        Area.move_in(person, House)
                    
                    elif person.is_working and person.is_shopping:
                        Area.move_out(person, Workplace)
                        Area.move_in(person, Store)

                    # leisure walks in this stage too i feel is more accurate than in morning step, but idk
                    # so those who are adults (and maybe even teens idk) 

                    # TODO: when i do death rates, i will do either do check if dies same day as infected, or each day still infected (before) recovery, i do the % chance they die
                    
                    # TODO: then one of the measures will ofc be that if infected then that person stays home and doesn't go to work or shop or outside
                    # I will simulate with different times of tested, so initially i will assume it takes them 3 days to test (we assume they would notice immediately once infected)
                    # and then see how improving testing speeds would benefit
                    # or ACTUALLY IGNORE TESTING, JUST DO HOW QUICKLY PEOPLE DECIDE TO STAY HOME (SO IMMEDIATELY WOULD MEAN THEY DON'T WAIT IT OUT AT ALL AND TRY TO STILL GO TO WORK OR STORE)
                    # and longer would be people still wanting to go to work etc.
                    # may need to change the working logic to is_working to is_working_in_office
                    # this way i can still assing 60% is working, and then 50/50 split (and others) that we do remote, and then further condition that if any infected they don't go in (even if part of 50 that are assigned to work at the office)
                
                healthy_count = len([person for person in population if not person.infected])
                infection_count = len([person for person in population if person.infected])
                print(f"Day: {day}, Step: {step}, Healthy: {healthy_count}, Infected: {infection_count}")
                print_grids(houses, stores, workplaces, outdoors, GRID_SIZE)

            elif step == 3:
                for person in population:
                    if person.is_working and person.is_shopping:
                        Area.move_out(person, Store)
                        Area.move_in(person, House)

                Area.calculate_infections(houses)

                healthy_count = len([person for person in population if not person.infected])
                infection_count = len([person for person in population if person.infected])
                print(f"Day: {day}, Step: {step}, Healthy: {healthy_count}, Infected: {infection_count}")
                print_grids(houses, stores, workplaces, outdoors, GRID_SIZE)
                



def print_grids(houses, stores, workplaces, outdoors, grid_size):
    # Initialize a grid of '-' and '0' of the appropriate size
    grid = [["e" for _ in range(grid_size)] for _ in range(grid_size)]
    grid_numbers = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    all_inhabitants_count = 0

    for house in houses:
        if house.location:
            grid[house.location.x][house.location.y] = colored("H", "blue")
            grid_numbers[house.location.x][house.location.y] = colored(len(house.inhabitants), "blue")
            

    for store in stores:
        if store.location:
            grid[store.location.x][store.location.y] = colored("S", "green")
            grid_numbers[store.location.x][store.location.y] = colored(len(store.inhabitants), "green")
            

    for workplace in workplaces:
        if workplace.location:
            grid[workplace.location.x][workplace.location.y] = colored("W", "yellow")
            grid_numbers[workplace.location.x][workplace.location.y] = colored(len(workplace.inhabitants), "yellow")

    for outdoor in outdoors:
        if outdoor.location:
            grid[outdoor.location.x][outdoor.location.y] = "-"
            grid_numbers[outdoor.location.x][outdoor.location.y] = len(outdoor.inhabitants)




    # Convert the grids to lists of strings
    grid = [' '.join(row) for row in grid]
    grid_numbers_colored = [' '.join(str(cell) for cell in row) for row in grid_numbers]
    
    # Print both grids side by side
    for row_grid, row_grid_numbers in zip(grid, grid_numbers_colored):
        print(row_grid, "   ", row_grid_numbers)

    for area in houses + workplaces + stores + outdoors:
        if area.location:
            all_inhabitants_count += len(area.inhabitants)
            
    print(all_inhabitants_count)

    print()



# Prints logic
def print_population_info(population):
    for person in population:
        if person.is_parent: 
            print(f"Age: {person.age}, House: {person.house_location}, id: {person.id} "
                f"Parents: {', '.join(['id: ' + str(parent.id) for parent in person.parents])}, "
                f"Store: {person.store_location}, ")
        elif person.is_young:
            print(f"Age: {person.age}, House: {person.house_location}, id: {person.id} "
                f"Grandparents: {', '.join(['id: ' + str(grandparent.id) for grandparent in person.grandparents])}, "
                f"Store: {person.store_location}, ")
        elif person.is_kid:
            print(f"Age: {person.age}, House: {person.house_location}, id: {person.id} "
                f"Parents: {', '.join(['id: ' + str(parent.id) for parent in person.parents])}, "
                f"Grandparents: {', '.join(['id: ' + str(grandparent.id) for grandparent in person.grandparents])}, "
                f"Store: {person.store_location}, ")
        else:
            print(f"Age: {person.age}, House: {person.house_location}, id: {person.id}, "
                f"Store: {person.store_location}, ")

def check_grid(population_size, grid_size):
    if population_size/2 > grid_size**2:
        raise ValueError("GRID IS TOO SMALL!")


def sim():
    check_grid(POPULATION_SIZE, GRID_SIZE)
    population, houses = generate_population_and_assign_houses(POPULATION_SIZE, GRID_SIZE)
    stores = generate_stores(population, STORE_CAPACITY, GRID_SIZE, houses)
    workplaces = generate_workplaces(population, WORKPLACE_CAPACITY, GRID_SIZE, houses, stores)
    outdoors = generate_outdoors(GRID_SIZE, houses, stores, workplaces)
    assign_stores(population, stores)
    assign_workplaces(population, workplaces)
    print_population_info(population)
    print()
    print("Simulation Grid, with Max All-At-Once Allocation")
    print_grids(houses, stores, workplaces, outdoors, GRID_SIZE)
    print()
    simulate_day(population, houses, workplaces, stores, outdoors, NUM_DAYS)

sim()
