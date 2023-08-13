# Epidemiology_19 🦠

In this project, we use to explore how infections spread through a modelled society/city. Welcome to the grid :). Note, this project does **not** aim to provide guidance regarding guidelines for current or future pandemics, but was rather a way to further develop my Python and simulation-design skills

<img width="624" alt="Screenshot 2023-08-12 at 23 45 09" src="https://github.com/lblcbc/Epidemiology_19/assets/136857271/8b9d21d5-5dda-42f0-82ad-80f486aa29b0">


Briefly, in this model, I build a grid environment (20x20 - though it can be scaled up to "anything") with a set population size (400, which can also be scaled up to "anything", as long as the grid is large enough). The population size is generated roughly following the 2019 global population distribution (roughly; weights guide random choices), forming "grandparents", "parents", "young adults", and "kids". As seen in the code, grandparents live in their own houses, either single or as a couple, parents (2) are assigned 1-4 kids, and then the kids are assigned grandparents if their parents are assigned parents. Young adults live in couples in their own separate houses as well. House locations are randomly scattered across the grid, and then each eligible person is assigned to their nearest store and workplace (unless at full capacity, in which case assigned to the next closest store etc). The simulated is then run through days, primarily involving 5 activities: staying home, going to work, going to the store, walking, travelling, and visiting grandparents (on weekends) - with different conditions and weighted random likelihoods. I did not add a school functionality, as I found insight from workplaces and restrictions sufficient enough, though this would not be very difficult to add to this project. While this project does not aim to directly simulate the COVID-19 pandemic or guide/critique guidelines, infection rates are informed by the [microCOVID project](https://www.microcovid.org/?casesPastWeek=260&distance=normal&duration=480&interaction=workplace&personCount=13&riskProfile=hasCovid&scenarioName=custom&setting=filtered "microCOVID Project")  or critique COVID-19 guidelines I start with no restrictions regardless of infection numbers and then increase guideline restrictions for levels I, II, and III. Below are the summary findings and visuals. 


### Baseline: 
~ 18 (4.5%) (1 year)
~ 50 (12.5%) (3 years)

### Guideline I: All infectious (have symptoms) don't leave home
~ 10 (2.5%) (1 year)
~ 30 (7.5%) (3 years)

### Guideline II: Guideline I + 50% work-from-home, ~50% reduction of extended family visits and travels.
~ 10 (2.5%) (1 year)
~ 30 (7.5%) (3 years)

!! This is because the model was initially, on purpose, built such that if not visiting family or travelling then people would choose to spend leisure by walking outside. However, to better represent a city, outdoor space is limited! Therefore, while infection chance is low, many people will have found themselves on the same outdoor grid space as others, and then still returning home to their roommates, parents and/or kids. This insignificantly reduced deaths and infection numbers (even after re-running to check these weren't random best/worst-case scenarios).

### Guideline III: Guideline II + grandparents rarely (10% chance) leave to shop, 90% work-from-home, no visiting family, walks, or travelling
~ 0 (0.0%) (1 year)
~ 0 (0.0%) (3 years)

We see dramatic results, and we know why. Not only were these guidelines very strict, there are key factors at play. Firstly, travelling, in this model, was the only way to introduce new infections into what would otherwise be a closed society/economy. If fully closed (as in this case, but regardless of any guidelines), as long as immunity lasts long enough, all infections will occur initially, and then be eradicated. Realistically, however, even if long-haul travel was largely restricted in real-life, inter-city travel remained, and so travelling in earlier guidelines allowed us to introduce this realistic element. The second key detail particularly ensures no passings or even infections among the elderly: no kids/grandkids visits, no walks or travelling, and crucially, not shopping at the same times as the very few workers who still worked in office. Therefore, some workers (whose age group were also the initially infected) would get infected at work, infect their households, but not go to the store at the same time, or visit, elderly (beyond working age)




Infection numbers on the histogram show total infections, including reinfection. This was done on purpose to take reinfection into account, but I write this to highlight that, as a result, mortality rates can't be estimated from the plot (they will be too low - people can be re-infected, but they can't re-pass). The mortality rates can be seen from the code, and the population size allows for roughly those rates to materialise in the simulation (given random element).
