class Population:
    def __init__(self, age, id=None):
        self.id = id
        
        self.age = age
        self.is_kid = 1 <= self.age < 20
        self.is_young = 20 <= self.age < 26 
        self.is_parent = 26 <= self.age < 53
        self.is_grandparent = 53 <= self.age
        self.is_adult = 20 <= self.age
        self.is_working_age = 20 <= self.age <= 65 
        
        self.parents = []
        self.grandparents = []
        
        self.location = None
        self.house_location = None
        self.workplace_location = None
        self.store_location = None
        self.outdoor_location = None
        
        self.is_working = False
        self.is_shopping = False
        self.is_travelling = False
        self.is_walking = False
        
        self.mortality_rate = None
        self.interactions = 0
        self.infection_probability = 0
        self.infected = False
        self.infectious = False
        self.days_infected = 0
        self.life_fulfilled = 5 # Day(s) after infection which person may die, having peacefully and happily fufilled their life, default is half of 10 (recovery_period)
        self.immune = False
        self.immunity_days = 0


