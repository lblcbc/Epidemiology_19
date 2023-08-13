import matplotlib.pyplot as plt
import numpy as np
from termcolor import colored
import seaborn as sns

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
def print_population_info(population, houses):
    for house in houses:
        print("new house")
        for person in house.inhabitants:
            print(f"Age: {person.age}")
    
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



def plot_counts(healthy_count, infected_count, death_count, immune_count):
    days = list(range(len(healthy_count)))

    sns.set_style("whitegrid")
    plt.figure(figsize=(20, 12))

    plt.stackplot(days, 
                  infected_count, 
                  immune_count,
                  healthy_count,
                  death_count, 
                  labels=['Infected', 'Immune', 'Healthy', 'Deaths'], 
                  colors=['orange', 'paleturquoise', 'blue', 'red'], 
                  alpha=0.6)

    # Aesthetic configurations
    plt.xlabel('Days', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.title('Population Over Time', fontsize=20)
    plt.legend(loc='lower center', fontsize=14)
    plt.tight_layout()
    sns.despine()

    plt.show()



def plot_age_dist(infected_age, passed_age):

    age_bins = list(range(0, 111, 10))
    labels = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99", "100-109"]


    def flatten(data):
        flattened = []
        for item in data:
            if hasattr(item, "__iter__"):  
                flattened.extend(item)
            else:
                flattened.append(item)
        return flattened

    all_infected_ages = flatten(infected_age)
    all_passed_ages = flatten(passed_age)

    sns.set_style("whitegrid")
    plt.figure(figsize=(20, 12))  
    

    plt.hist(all_infected_ages, bins=age_bins, alpha=0.6, label='Infected', color='blue', rwidth=0.8)
    

    plt.hist(all_passed_ages, bins=age_bins, alpha=0.6, label='Passed', color='red', rwidth=0.8)
    

    plt.xlabel('Age Brackets', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.title('Age Distribution of Infected and Passed Individuals', fontsize=20)
    plt.xticks(ticks=np.array(age_bins[:-1]) + 5, labels=labels, fontsize=14)  
    plt.yticks(fontsize=14)
    plt.legend(loc='upper right', fontsize=14)
    plt.tight_layout()
    sns.despine()

    plt.show()

