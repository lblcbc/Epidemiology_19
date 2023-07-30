import random
import math

GRID_SIZE = 10
AGE_DISTRIBUTION = [0.16, 0.17, 0.158, 0.140, 0.120, 0.108, 0.08, 0.04, 0.014, 0.01]
AGE_DISTRIBUTION_EXPANDED = [weight for weight in AGE_DISTRIBUTION for _ in range(10)]  # Repeat each weight 10 times

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other_location):
        return math.sqrt((self.x - other_location.x) ** 2 + (self.y - other_location.y) ** 2)

    def __repr__(self):
        return f"Location({self.x}, {self.y})"

class Building:
    def __init__(self, location):
        self.inhabitants = []
        self.location = location

class House(Building):
    def __init__(self, location):
        super().__init__(location)
        self.symbol = "H"

class Workplace(Building):
    def __init__(self, location):
        super().__init__(location)
        self.symbol = "W"

class Store(Building):
    def __init__(self, location):
        super().__init__(location)
        self.symbol = "S"

class Population:
    def __init__(self, age, id=None, home_location=None):
        self.age = age
        self.id = id
        self.home_location = home_location
        self.is_kid = 1 <= self.age < 20
        self.is_young = 20 <= self.age < 26 
        self.is_parent = 26 <= self.age < 56
        self.is_grandparent = 56 <= self.age
        self.is_adult = 20 <= self.age
        self.is_working_age = 20 <= self.age <= 65 # we ignore university, we will only have school for kids
        
        self.parents = []
        self.grandparents = []
        self.lives_with_parents = False
        self.workplace = None
        self.is_shopping = False
        self.store = None

def generate_population_and_assign_houses(population_size, grid_size):
    # Generate the population with ages
    population = []
    ages = random.choices(
        population=range(1, 101),  # Assuming people can live up to 100
        weights=AGE_DISTRIBUTION_EXPANDED,
        k=population_size
    )
    for age in ages:
        population.append(Population(age))

    # Sort the population by age (decreasing order)
    population.sort(key=lambda x: x.age, reverse=True)

    # Assing ids in age descending order
    for i, person in enumerate(population): # We use enumerate as it allos us, for each iteration to get both the current index (id) and the current element (person)
        person.id = i


    # Divide the population into kids, adults, and elders
    parents = [person for person in population if person.is_parent]
    kids = [person for person in population if person.is_kid]
    youngs = [person for person in population if person.is_young]
    grandparents = [person for person in population if person.is_grandparent]

    random.shuffle(parents)
    random.shuffle(kids)

    

    all_parents = []  # List to store all parents for assigning their parents later
    all_youngs = []  # List to store all youngs for assigning their grandparents later
    all_kids = [] #List to store all kids for assigning their grandparents later

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
            num_kids = len(kids)

        # Add parents to the house
        current_parents = []  # List to keep track of the parents currently being added to the house
        for _ in range(num_parents):  
            if parents:
                parent = parents.pop()
                parent.home_location = house.location
                house.inhabitants.append(parent)
                current_parents.append(parent)  # Add each parent to the current_parents list
                all_parents.append(parent)  # Add each parent to the all_parents list

        # Add kids to the house and assign them parents
        for _ in range(num_kids):
            if kids:
                kid = kids.pop()
                kid.home_location = house.location
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
                    young.home_location = house.location
                    house.inhabitants.append(young)
            houses.append(house)
            all_youngs.append(young)  # Add each young to the all_youngs list

    # Assign each elder to a separate house and link them to adults
    for grandparent in grandparents:

        house = House(None)
        grandparent.home_location = house.location
        house.inhabitants.append(grandparent)
        houses.append(house)

        # Link the elder to a random adult (as a parent) if any left
        if all_parents or all_youngs:
            if random.choice([True, False]):
                if all_parents:
                    random_parent = random.choice(all_parents)
                    random_parent.parents.append(grandparent)
                    
        
                    for kid in all_kids:
                        if random_parent in kid.parents and grandparent not in kid.grandparents:
                            kid.grandparents.append(grandparent)

                    #for house in houses:
                        #for person in house.inhabitants:
                            #if person.id == random_parent.id:
                                #for person in house.inhabitants:
                                    #if person.is_kid and grandparent not in person.grandparents:
                                        #person.grandparents.append(grandparent)

                    # The above would also work, but is less efficienct
                 
            else:
                if all_youngs:
                    random_young = random.choice(all_youngs)
                    random_young.parents.append(grandparent)

    # Generate random locations
    locations = [Location(x, y) for x in range(grid_size) for y in range(grid_size)]
    random.shuffle(locations)

    # Now assign the random locations to the houses
    for house, location in zip(houses, locations):
        house.location = location
        for inhabitant in house.inhabitants:
            inhabitant.home_location = location

    return population, houses

def print_grid(houses, grid_size):
    # Initialize a grid of '-' of the appropriate size
    grid = [['-' for _ in range(grid_size)] for _ in range(grid_size)]
    
    for house in houses:
        if house.location:  # Make sure the house has a location
            # We're using 'H' to represent a house
            grid[house.location.x][house.location.y] = 'H'
    
    # Return the grid as a list of strings
    return [' '.join(row) for row in grid]

def print_grid_numbers(houses, grid_size):
    # Initialize a grid of zeros of the appropriate size
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    for house in houses:
        if house.location:  # Make sure the house has a location
            # We're using the number of inhabitants to represent a house
            grid[house.location.x][house.location.y] = len(house.inhabitants)
    
    # Return the grid as a list of strings
    return [' '.join(str(cell) for cell in row) for row in grid]

# Get the population and houses
population, houses = generate_population_and_assign_houses(35, GRID_SIZE)

# Print the population
for person in population:
    # Print the population
    if person.is_parent: 
        print(f"Age: {person.age}, House Location: {person.home_location}, id: {person.id} "
            f"Parents: {', '.join(['id: ' + str(parent.id) for parent in person.parents])}, ")
    elif person.is_young:
        print(f"Age: {person.age}, House Location: {person.home_location}, id: {person.id} "
            f"Grandparents: {', '.join(['id: ' + str(grandparent.id) for grandparent in person.grandparents])}, ")
    elif person.is_kid:
        print(f"Age: {person.age}, House Location: {person.home_location}, id: {person.id} "
            f"Parents: {', '.join(['id: ' + str(parent.id) for parent in person.parents])}, "
            f"Grandparents: {', '.join(['id: ' + str(grandparent.id) for grandparent in person.grandparents])}")
    else:
        print(f"Age: {person.age}, House Location: {person.home_location}, id: {person.id} ")



# Get the grids as lists of strings
print()
grid = print_grid(houses, GRID_SIZE)
grid_numbers = print_grid_numbers(houses, GRID_SIZE)

# Print the grids side-by-side
for row_grid, row_grid_numbers in zip(grid, grid_numbers):
    print(row_grid, "   ", row_grid_numbers)
