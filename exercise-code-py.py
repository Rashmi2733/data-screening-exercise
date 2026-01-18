#Getting all the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
#Simple EDA

#Showing top 10 cities and states with detention facilities
def top_graphs(df, col_name, xvalue):
    top_df = df[col_name].value_counts().reset_index().head(10)
    plt.bar(top_df[col_name], top_df['count'], color = 'green')
    plt.xlabel(f"{xvalue}")
    plt.ylabel("Count")
    plt.title(f"Top 10 {xvalue} with Detention Facilities")
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
#Plotting top 10 facilities based on population
plt.barh(df_10['Name'], df_10['Total Population'])
plt.ylabel("Detention Facility")
plt.xlabel("Total Population")
plt.title(f"Top 10 Detention Facilities according to population")
plt.gca().invert_yaxis()
plt.grid()
plt.show()
#Getting the top states with total population
top_10_states = df.groupby('StateName')[['Total Population']].sum().reset_index().sort_values(by="Total Population", ascending = False).head(10)
top_10_states
#Plotting top 10 States based on population
plt.bar(top_10_states['StateName'], top_10_states['Total Population'])
plt.xlabel("State")
plt.ylabel("Total Population")
plt.title(f"Top 10 States according to population")
plt.xticks(rotation=90)
plt.grid()
plt.show()
