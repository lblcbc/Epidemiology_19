# Epidemiology_19 🦠

In this project, we use to explore how infections spread through a modelled society/city. Welcome to the grid :). Note, this project does **not** aim to provide guidance regarding guidelines for current or future pandemics, but was rather a way to further develop my Python and simulation-design skills

<img width="624" alt="Screenshot 2023-08-12 at 23 45 09" src="https://github.com/lblcbc/Epidemiology_19/assets/136857271/8b9d21d5-5dda-42f0-82ad-80f486aa29b0">


Briefly, in this model, I build a grid environment (20x20 - though it can be scaled up to "anything") with a set population size (400, which can also be scaled up to "anything", as long as the grid is large enough). The population size is generated roughly following the 2019 global population distribution (roughly; weights guide random choices), forming "grandparents", "parents", "young adults", and "kids". As seen in the code, grandparents live in their own houses, either single or as a couple, parents (2) are assigned 1-4 kids, and then the kids are assigned grandparents if their parents are assigned parents. Young adults live in couples in their own separate houses as well. House locations are randomly scattered across the grid, and then each eligible person is assigned to their nearest store and workplace (unless at full capacity, in which case assigned to the next closest store etc). The simulated is then run through days, primarily involving 5 activities: staying home, going to work, going to the store, walking, travelling, and visiting grandparents (on weekends) - with different conditions and weighted random likelihoods. I did not add a school functionality, as I found insight from workplaces and restrictions sufficient enough, though this would not be very difficult to add to this project. While this project does not aim to directly simulate the COVID-19 pandemic or guide/critique guidelines, infection rates are informed by the [microCOVID project](https://www.microcovid.org/?casesPastWeek=260&distance=normal&duration=480&interaction=workplace&personCount=13&riskProfile=hasCovid&scenarioName=custom&setting=filtered). I start with no restrictions regardless of infection numbers, and then increase guideline restrictions to levels I, II, and III. Below are the summary findings and visuals. 


## Summary Results
### Baseline: 
###### Passed count:
##### ~ 18 (4.5%) (1 year)
##### ~ 50 (12.5%) (3 years)

![baseline_age_3](https://github.com/lblcbc/Epidemiology_19/assets/136857271/ae1b5cb9-a2d5-440c-8194-315d34d8f836)


#### Guidelines I: All infectious (have symptoms) don't leave home
##### ~ 10 (2.5%) (1 year)
##### ~ 30 (7.5%) (3 years)

![I_age_3](https://github.com/lblcbc/Epidemiology_19/assets/136857271/2f3f342d-a31a-44d6-ba9f-ebedd6c8d4f8)


#### Guidelines II: Guideline I + masks, assumed to reduce infection rates by 50%
##### ~ 9 (2.5%) (1 year)
##### ~ 26 (7.5%) (3 years)

![II_age_3](https://github.com/lblcbc/Epidemiology_19/assets/136857271/db77e7cf-7b5e-4a24-9c84-4f61e82515d3)


#### Guidelines III: Guideline II + 90% reduction in shopping, 90% work-from-home, no visiting family, walks, or travelling
##### ~ 0-1 (0.0-0.25%) (1 year)
##### ~ 0-1 (0.0-0.25%) (3 years)

![III_age_3](https://github.com/lblcbc/Epidemiology_19/assets/136857271/2a7eb528-2d0b-4079-b019-dd7b2e3d6f91)



(3-year) infection numbers on the histogram show total infections, allowing us to reflect reinfections. This is to not however that as a result, mortality rates can't be estimated from the plot (they will be too low - people can be re-infected, but they can't re-pass). The mortality rates can be seen from (and are anyway dictated by) the code.


## Summary Images
#### Baseline 1 Year

![baseline_population_1](https://github.com/lblcbc/Epidemiology_19/assets/136857271/b35795b5-a11e-45c7-b7cd-aa5d2d6e3c46)

##### To best compare guidelines, we will use a 3-year horizon:
#### Baseline (3 Years)

![baseline_population_3](https://github.com/lblcbc/Epidemiology_19/assets/136857271/0bbb360c-3e72-4e3e-a72f-49ec3f40c0a6)

#### Guidelines I (3 Years)

![I_population_3](https://github.com/lblcbc/Epidemiology_19/assets/136857271/135e4c32-1bd9-47e9-8831-1c58c4e66f94)


#### Guidelines II (3 Years)

![II_population_3](https://github.com/lblcbc/Epidemiology_19/assets/136857271/6efe6ca1-0ceb-4888-bc79-66643eaa231b)

The images clearly show how masks significantly helped curb infection numbers - particularly stemming from a lower likelihood of infection from travel - the only way new infections are introduced in this simulation. However, in this simulation (which is still far from real-life applicable) mortality rates remained largely similar. Shopping with the elderly and family visits were enough to eventually trigger infections for older age groups. 

#### Guidelines III (3 Years)

![III_population_3](https://github.com/lblcbc/Epidemiology_19/assets/136857271/b4ea6f2e-c98e-46b3-8b2a-27ce71da6a98)

We see dramatic results, and we know why. Not only were these guidelines very strict, there are key factors at play. Firstly, travelling, in this model, was the only way to introduce new infections into what would otherwise be a closed society/economy. If fully closed (as in this case, but regardless of any guidelines), as long as immunity lasts long enough, all infections will occur initially, and then be eradicated. Realistically, however, even if long-haul travel was largely restricted in real-life, inter-city travel remained, and so travelling in earlier guidelines allowed us to introduce this realistic element. The second key detail particularly ensures no passings or even infections among the elderly: no kids/grandkids visits, no walks or travelling, and crucially, not shopping at the same times as the very few workers who still worked in office. Therefore, some workers (whose age group were also the initially infected) would get infected at work, infect their households, but not go to the store at the same time, or visit, elderly (beyond working age)



Overall, the main takeaway, and to no surprise is for all those who are infectious to immediately stay home and not go to work, and doing what you can to reduce the risk of infection, particularly when travelling (meeting new people). Infections are muted more quickly in closed communities.
