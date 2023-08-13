POPULATION_SIZE = 400
GRID_SIZE = 20
STORE_CAPACITY = 20
WORKPLACE_CAPACITY = 14
INITIAL_INFECTIONS = 0.05*POPULATION_SIZE
RECOVERY_PERIOD = 10 # Days, until then you are still infectious
IMMUNITY_PERIOD = 100 # Studies showed 8-10 months immunity


AGE_DISTRIBUTION = [0.16, 0.17, 0.158, 0.140, 0.120, 0.108, 0.08, 0.04, 0.014, 0.01]
AGE_DISTRIBUTION_EXPANDED = [weight for weight in AGE_DISTRIBUTION for _ in range(10)]  # Repeat each weight 10 times
mortality_rate = {
    9: 0.148, # 90 - 99 yo, I handle the 100 yo case in my assign_mortality_rate function.
    8: 0.148, 
    7: 0.080, 
    6: 0.036, 
    5: 0.013, 
    4: 0.004, 
    3: 0.002, 
    2: 0.002, 
    1: 0.002, # 10 - 19 yo  
    0: 0.000 # 0 - 9 yo
}

NUM_DAYS = 1095

INFECTED_AGE = []
PASSED_AGE = []