import random
from constants import *


def assign_mortality_rates(population):
    for person in population:
        age_group = person.age // 10  # This will give values like 1 for [10, 19], 2 for [20, 29], and so on.
        
        if age_group == 10: # Handle edge case for age 100
            age_group = 9
        
        person.mortality_rate = mortality_rate[age_group]


def determine_infection(person, infection_probability):
        if random.random() < infection_probability:
            person.infected = True
            INFECTED_AGE.append(person.age)
            person.days_infected = 1
            person.life_fufilled = random.randint(1,10)

def calculate_infections(areas):
        for area in areas:
            for person in area.inhabitants:
                if not person.infected and not person.immune:
                    infectious_count = len([person for person in area.inhabitants if person.infectious])
                    person.interactions += infectious_count
                    person.infection_probability = area.scaled_infection_probability(person.interactions)
                    determine_infection(person, person.infection_probability)


def update_infected(population, houses):
    for person in population:
        if person.infected:
            person.days_infected += 1
            if person.days_infected == person.life_fulfilled:
                if random.random() < person.mortality_rate:
                    population.remove(person)
                    PASSED_AGE.append(person.age)
                    for house in houses:
                        if house.location == person.house_location:
                            house.inhabitants.remove(person) 
                    continue
                else:
                    person.life_fulfilled = 20 # Arbitrary number high enough to ensure recovery
            if person.days_infected > 10:
                person.days_infected = 0
                person.infected = False
                person.infectious = False
                person.life_fulfilled = 5
                person.immune = True
        if person.immune:
                person.immunity_days += 1
                if person.immunity_days > IMMUNITY_PERIOD:
                    person.immunity_days = 0
                    person.immune = False

