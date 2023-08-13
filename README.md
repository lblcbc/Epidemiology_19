# Epidemiology_19


### Baseline: 
~ 18 (4.5%) (1 year)
~ 50 (12.5%) (3 years)

### Guideline I: All infectious (have symptoms) don't leave home
~ 10 (2.5%) (1 year)
~ 30 (7.5%) (3 years)

### Guideline II: Guideline I + 50% work-from-home, ~50% reduction of extended family visits and travels.
~ 10 (2.5%) (1 year)
~ 30 (7.5%) (3 years)

!! This is because the model was initially, on purpose, built such that if not visiting family or travelling then people would choose to spend leisure by walking outside. HOWEVER, to better represent a city, outdoor space is limited! Therefore, while infection chance is low, many people will have found themselves on the same outdoor grid space as others, and then still returning home to their roommates, parents and/or kids. This insignificantly reduced deaths and infection numbers (even after re-running to check these weren't random best/worst case scenarios).

### Guideline III: Guideline II + grandparents rarely rarely (10% chance) leave to shop, 90% work-from-home, no visiting family, walks, or travelling
~ 0 (0.0%) (1 year)
~ 0 (0.0%) (3 years)

We see dramatic results, and we know why. Not only were these guidelines very strict, there are key factors at play. Firstly, travelling, in this model, was the only way to introduce new infections into what would otherwise be a closed society/economy. If fully close (as in this case, but regardless of any guidelines), as long as immunity lasts long enough, all infections will occur initially, and then be eradicated; again as the society is closed, so no new infections enter. Realistically, however, even if long-haul travel was largely restricted, inter-city travel remained, and so travelling in earlier guidelines allowed us to introduce this realistic element. The second key detail, particularly ensures no passings or even infections among elderly, were 1. no kids/grandkids visits, no walks or travelling, and crucially, not shopping at same times as the very few workers who still worked in office. Therefore, some workers (whose age group were also the initially infected) would get infected at work, infect their households, but not go to the store at the same 




Infection numbers on the histogram show total infections, including reinfection. This was done on purpose to take reinfection into account, but I write this to highlight that, as a result, mortality rates can't be estimated from the plot (they will be too low - people can be re-infected, but they can't re-pass). The mortality rates can be seen from the code, and the population size allows for roughly those rates to materialise in the simulation (given random element).


The grid could also be scaled up 
