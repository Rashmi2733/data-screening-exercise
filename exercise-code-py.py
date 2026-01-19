#Installing libraries
#Can run the code below if needed
# pip install pandas numpy matplotlib seaborn
#Getting all the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Loading the provided dataset by skiping first six rows of data present in csv (using the windows-1252 encoding since th default utf8 did gave an error)
df = pd.read_csv("messy_ice_detention.csv", skiprows=6, encoding='cp1252')
print(df.head(5))

#Checking the datatypes for each column
df.dtypes

#Checking for any null values
df.isna().sum()

#Checking for empty values in Name, City, State columns
print("Missing Name:")
print(df[df['Name']==" "])
print("-------------------")

print("Missing City:")
print(df[df['City']==" "])
print("-------------------")

print("Missing State:")
print(df[df['State']==" "])
print("-------------------")

#Filling in missing values for Name, State, City columns (through google search)
df.loc[116, "Name"] = 'Sherburne County Jail'
df.loc[123, "Name"] = 'Strafford County Corrections'
df.loc[51, "City"] = 'Chardon'
df.loc[71, "State"] = 'TX'
df.loc[6, "State"] = 'GA'

#Changing all values to uppercase
df['Name'] = df['Name'].str.upper()
df['City'] = df['City'].str.upper()
df['State'] = df['State'].str.upper()

#Since only state code is given, mapping the code to full state names
state_mapping = {"AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"}

df['StateName'] = df['State'].map(state_mapping)
df.sample(5)

#Checking if the Name column has any characters besides alphabetic (and spaces)
df[~df['Name'].astype(str).str.match(r'^[A-Za-z ]+$', na=False)]

#Removing all special characters (besides brackets ())
df['Name'] = df['Name'].str.replace(r"[.\^@%*\+\-#$,_/&]", "", regex=True)

#Recheking Name column for any unique characters
df[~df['Name'].astype(str).str.match(r'^[A-Za-z ]+$', na=False)]

#Removing all open and close brackets without accompanying close and open brackets
#For this code, chatgpt was used using the prompt: For a column containing names, remove brackets if there is a start ["("] but no end [")"] and end [")"] but no start ["("]. If both open and close brackets are present, ignore them and keep them as they are
df['Name'] = (df['Name'].str.replace(r"\([^)]*$", "", regex=True).str.replace(r"^[^(]*\)", "", regex=True))

#Recheking Name column for any unique characters
df[~df['Name'].astype(str).str.match(r'^[A-Za-z ]+$', na=False)]

#Since it seems like the Name at index 6 still has some hidden characters, will inspect it more
df.loc[6, "Name"]

#Removing special character '\xa0'
df['Name'] = df['Name'].str.replace(r"\xa0", " ", regex=True)
df.loc[6, "Name"]

#Replacing short forms
df['Name'] = df['Name'].str.replace(" DET ", ' DETENTION ')


#Simple EDA

#Showing top 10 cities and states with detention facilities
def top_graphs(df, col_name, xvalue):
    top_df = df[col_name].value_counts().reset_index().head(10)
    plt.bar(top_df[col_name], top_df['count'], color = 'green')
    plt.xlabel(f"{xvalue}", fontweight='bold')
    plt.ylabel("Count", fontweight='bold')
    plt.title(f"Top 10 {xvalue} with Detention Facilities", fontweight='bold')
    plt.xticks(rotation = 90)
    plt.grid()
    plt.show()

top_graphs(df, 'StateName', "States")
top_graphs(df, 'City', "Cities")


#Adding all values for population from Level columns
df['Total Population'] = df['Level A'] + df['Level B'] + df['Level C'] + df['Level D']
df.sample(5)


#Getting top 10 detention facilities based on total population
df_10 = df.sort_values(by='Total Population', ascending=False).head(10)
df_10

# #Plotting top 10 Facilities based on population
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 5))

ax = sns.barplot(data=df_10, y="Name", x="Total Population", orient="h", hue='StateName')
ax.set_ylabel("Detention Facility", fontweight="bold")
ax.set_xlabel("Total Population", fontweight="bold")
ax.set_title("Top 10 Detention Facilities by Population", fontweight="bold")
ax.tick_params(axis="y", labelsize=10)
ax.legend(title='State')
plt.tight_layout()
plt.show()

##PLotting the top ten detention centers based on population and also showing the different populations based on the 4 levels

#Setting the index to Name to make it easier to plot
df_plot = df_10.set_index("Name")
#Stacking the levels on a bar graph to get the final population
df_plot[["Level A", "Level B", "Level C", "Level D"]].plot(kind="barh", stacked=True, figsize=(12, 5))

plt.xlabel("Total Population", fontweight="bold")
plt.ylabel("Detention Facility", fontweight="bold")
plt.title("Top 10 Detention Facilities by Population of Different Levels", fontweight="bold")
plt.legend(title="Population Level")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

#Getting the top states with total population
top_10_states = df.groupby('StateName')[['Total Population']].sum().reset_index().sort_values(by="Total Population", ascending = False).head(10)
top_10_states

# #Plotting top 10 States based on population
plt.figure(figsize=(12, 5))

ax = sns.barplot(data=top_10_states, y="StateName", x="Total Population", color ='grey')
ax.set_ylabel("Total Population", fontweight="bold")
ax.set_xlabel("State", fontweight="bold")
ax.set_title("Top 10 States By Population", fontweight="bold")
plt.tight_layout()
plt.show()
