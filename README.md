# Epidemiology_19


### Passed
Baseline: 
~ 18 (4.5%) (1 year)
~ 50 (12.5%) (3 years)

Guideline I: All infectious (have symptoms) don't leave home
~ 10 (2.5%) (1 year)
~ 30 (7.5%) (3 years)

Guideline II: Guideline I + 50% work-from-home, ~50% reduction of extended family visits and travels.
~ 10 (2.5%) (1 year)
~ 30 (7.5%) (3 years)
!! This is because the model was initially, on purpose, built such that if not visiting family or travelling then people would choose to spend leisure by walking outside. HOWEVER, to better represent a city, outdoor space is limited! Therefore, while infection chance is low, many people will have found themselves on the same outdoor grid space as others, and then still returning home to their roommates, parents and/or kids. Seemingly, this just about cancelled out interactions at work and stores, which, while reduced, still took place. Similarly, extended family visits and travels, while reduced, still took place, and thus, paired with more walking, and a closed dense city grid, infection numbers remained very similar. Some of this is also down to randomness, while multiple simulations were run under the same guidelines, it could be that the sample image above represented a near "best case scenario", and this one for guideline II a less effective outcome.

Infection numbers on the histogram show total infections, including reinfection. This was done on purpose to take reinfection into account, but I write this to highlight that, as a result, mortality rates can't be estimated from the plot (they will be too low - people can be re-infected, but they can't re-pass). The mortality rates can be seen from the code, and the population size allows for roughly those rates to materialise in the simulation (given random element).
