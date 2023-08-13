import random

from constants import *
from area import *
from epidemic import *
from prints import print_grids


infected_count = []
healthy_count = []
immune_count = []
passed_count = []

def reset_counts():
    global infected_count, healthy_count, immune_count, passed_count
    infected_count = []
    healthy_count = []
    immune_count = []
    passed_count = []

def simulate_day(population, houses, workplaces, stores, outdoors, num_days):
    for area in stores + workplaces + outdoors:
        area.inhabitants = []

    # Set up building dict
    Area.setup_area_dict(houses, workplaces, stores, outdoors)

    # Initially infected population
    adults = [person for person in population if person.is_adult and not person.is_grandparent]
    initally_infected = random.sample(adults, int(INITIAL_INFECTIONS))
    for person in initally_infected:
        person.infected = True
        person.infectious = True
        print(f"ID: {person.id}, Age: {person.age}")

    for person in population:
        person.location = person.house_location
        if person.is_working_age and not person.infectious:
            if random.random() < 0.1: # 90% work from home effectively
                person.is_working = True

    for day in range(num_days):
        if day % 5 != 0 and day % 6 != 0: 
            for step in range(4):
                if step == 0:
                    for person in population:
                        person.interactions = 0
                        person.infection_probability = 0
                        person.is_shopping = False
                        person.is_travelling = False
                        person.is_walking = False
                        if person.infected:
                            person.infectious = True 
                          

                    update_infected(population, houses)
                
                    healthy_count.append(len([person for person in population if not person.infected and not person.immune]))
                    immune_count.append(len([person for person in population if person.immune]))
                    infected_count.append(len([person for person in population if person.infected]))
                    passed_count.append(POPULATION_SIZE - healthy_count[-1] - infected_count[-1] - immune_count[-1])

                    """
                    if day == 0 or day % 100 == 0:
                        print(f"Day: {day}, Healthy: {healthy_count[-1]}, Infected: {infected_count[-1]}, Immune: {immune_count[-1]}, Passed: {passed_count[-1]}")
                        print_grids(houses, stores, workplaces, outdoors, GRID_SIZE)
                    """

                elif step == 1:
                    for person in population:
                        if not person.infectious:
                            if person.is_working:
                                Area.move_out(person, House)
                                Area.move_in(person, Workplace)

                            if person.is_adult and random.random() < 0.1: # reduced
                                person.is_shopping = True
                            
                            if person.is_shopping and not person.is_working:
                                Area.move_out(person, House)
                                Area.move_in(person, Store)
                            
                            # No travelling or walking
                            """
                            if person.is_adult and not person.is_working and not person.is_shopping:
                                if random.random() < 0.2: 
                                    person.is_travelling = True
                                    if random.random() < 0.25 and not person.immune:
                                        person.infected = True I can set it true here and they still will only be able to infect people next day so it's fine setting infected true here already
                                else:
                                    person.is_walking = True
                            """
                            

                    calculate_infections(workplaces)
                    calculate_infections(stores)

                elif step == 2:
                    for person in population:
                        if not person.infectious:
                            if person.is_shopping and not person.is_working:
                                Area.move_out(person, Store)
                                Area.move_in(person, House)

                            elif person.is_working and not person.is_shopping:
                                Area.move_out(person, Workplace)
                                Area.move_in(person, House)
                            
                            elif person.is_working and person.is_shopping:
                                Area.move_out(person, Workplace)
                                Area.move_in(person, Store)

                            elif person.is_walking:
                                outdoor_locations = [outdoor.location for outdoor in outdoors]
                                random_outdoor_location = random.choice(outdoor_locations)
                                person.outdoor_location = random_outdoor_location
                                Area.move_out(person, House)
                                Area.move_in(person, Outdoor)
                        
                    calculate_infections(outdoors)

                elif step == 3:
                    for person in population:
                        if not person.infectious:
                            if person.is_working and person.is_shopping:
                                Area.move_out(person, Store)
                                Area.move_in(person, House)
                            if person.is_walking:
                                Area.move_out(person, Outdoor)
                                Area.move_in(person, House)

                    calculate_infections(houses)

        else:
            for step in range(3):
                if step == 0:
                    for person in population:
                        person.interactions = 0
                        person.infection_probability = 0
                        person.is_shopping = False
                        person.is_travelling = False
                        person.is_walking = False
                        if person.infected:
                            person.infectious = True

                    update_infected(population, houses)

                    healthy_count.append(len([person for person in population if not person.infected and not person.immune]))
                    immune_count.append(len([person for person in population if person.immune]))
                    infected_count.append(len([person for person in population if person.infected]))
                    passed_count.append(POPULATION_SIZE - healthy_count[-1] - infected_count[-1] - immune_count[-1])
                    
                elif step == 1:
                    # No visiting grandparents, walking or travelling
                    """
                    for person in population:
                        if not person.infectious:
                            if person.is_kid and person.grandparents and random.random() < 0.25: # reduced from 0.5
                                grandparent = random.choice(person.grandparents)
                                Area.move_out(person, House)
                                for house in houses:
                                    if house.location == grandparent.house_location:
                                        house.inhabitants.append(person)
                                        person.location = grandparent.house_location
                                        break

                            if person.is_young and person.grandparents:
                                today_prob = random.random()
                                if today_prob < 0.1: # reduced from 0.2
                                    grandparent = random.choice(person.grandparents)
                                    Area.move_out(person, House)
                                    for house in houses: 
                                        if house.location == grandparent.house_location:
                                            house.inhabitants.append(person)
                                            person.location = grandparent.house_location
                                            break
                                elif today_prob > 0.1 and today_prob < 0.9: 
                                    person.is_walking = True
                                    outdoor_locations = [outdoor.location for outdoor in outdoors]
                                    random_outdoor_location = random.choice(outdoor_locations)
                                    person.outdoor_location = random_outdoor_location
                                    Area.move_out(person, House)
                                    Area.move_in(person, Outdoor)
                                else:
                                    person.is_travelling = True
                                    if random.random() < 0.25 and not person.immune:
                                        person.infected = True 

                            if person.is_parent and person.parents:
                                today_prob = random.random()
                                if today_prob < 0.2: # reduced from 0.4
                                    parent = random.choice(person.parents)
                                    Area.move_out(person, House)
                                    for house in houses: move_in doesn't accept individual locations, so doing it manually: move_in(person, House (grandparents))
                                        if house.location == parent.house_location:
                                            house.inhabitants.append(person)
                                            person.location = parent.house_location
                                            break
                                elif today_prob > 0.2 and today_prob < 0.7: 
                                    person.is_walking = True
                                    outdoor_locations = [outdoor.location for outdoor in outdoors]
                                    random_outdoor_location = random.choice(outdoor_locations)
                                    person.outdoor_location = random_outdoor_location
                                    Area.move_out(person, House)
                                    Area.move_in(person, Outdoor)
                                elif today_prob > 0.7 and today_prob < 0.8: # reducing travelling likelyhood (range)
                                    person.is_travelling = True
                                    if random.random() < 0.25 and not person.immune:
                                        person.infected = True
                                else:
                                    person.is_shopping = True
                                    Area.move_out(person, House)
                                    Area.move_in(person, Store)
                    """
                    calculate_infections(houses)
                    calculate_infections(outdoors)
                    calculate_infections(stores)

                elif step == 2:
                    # This step is now irrelevant as no movement has taken place on weekends
                    """
                    for person in population:
                        if not person.infectious:
                            for area in houses + stores + outdoors:
                                if area.location == person.location:
                                    area.inhabitants.remove(person)
                            
                            person.location = person.house_location
                            Area.move_in(person, House)
                    """
                    
