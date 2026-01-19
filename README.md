## Data Screening Exercise

This repository contains the code files and other necessary files required for the data screening exercise. 
Both the notebook ([exercise-code-notebook.ipynb](exercise-code-notebook.ipynb)) as well as the python file ([exercise-code-py.py](exercise-code-py.py)) has been provided. To run them, start by installing the required libraries listed in the `requirements.txt` file. The line `pip install -r requirements.txt` in terminal can be run or individually installing them in a notebook works as well (e.g. `pip install pandas`). The code in the notebook has outputs that make it easy to view each output. Both the notebook and the python file (.py) can be run to view the graphs.

A few google searches were conducted to add states, cities, and facility names that were missing. ChatGPT was used to get one code in order to clean up the facility names that had either open or close bracket without the other. The prompt used was: For a column containing names, remove brackets if there is a start [`(`] but no end [`)`] and end [`)`] but no start [`(`]. If both open and close brackets are present, ignore them and keep them as they are. Link for prompt [here](https://chatgpt.com/share/696d3b71-75c4-8004-90eb-2dbf6ff9ccfe).
The `Last Inspection End Month` column only had whole numbers (with one exception of date and few missing values). They were converted into date formats using the 1990 excel date system, hence giving us tentative dates (cannot be sure about the dates since we do not know if the 1994 system was used).

The top ten facilities by total population was found and the corresponding graph is provided ([top-10-facilities-by-population-and-state](top-10-facilities-by-population-and-state.png)). We can also see a statewise differentiation, showing that Texas and Louisiana both have 2 centers in the top 10. 

Beyond this, the graph [top-10-facilities-by-population-of-levels](top-10-facilities-by-population-of-levels.png) shows the total population with a breakdown in terms of the four levels. We mostly see Level A having the higher population with some exceptions for B and C. 

Further, the top 10 states with highest population was also found with the graph provided in the repository ([top-10-states-by-population](top-10-states-by-population.png)), with Texas being at the top, followed by Louisiana, showing comparative results to the previous graph. 

When we look at the population for the different months, we see the highest populations for January and December and lowest from April to August(this is overall population for all years provided) [monthly-population](monthly-population.png). 
