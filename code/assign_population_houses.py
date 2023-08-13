import random
from population import *
from constants import *
from location import *
from area import House
#from masked_area import House


def generate_population_and_assign_houses(population_size, grid_size):
    # Generate the population ages
    population = []
    ages = random.choices(
        population=range(1, 101), # Assuming people live up to 100
        weights=AGE_DISTRIBUTION_EXPANDED,
        k=population_size
    )
    for age in ages:
        population.append(Population(age))

    population.sort(key=lambda x: x.age, reverse=True) # Makes it more realisitc between age of adults paired (makes them similar)

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

        # Link each grandparent in a house to parent and kid or young adult
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

