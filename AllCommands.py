# Pandas Syntax Reference Guide
# This file contains all the syntax patterns used in the Panda_JupyterNB.ipynb file

# ==================== IMPORTS ====================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================== DATA LOADING ====================
# Reading CSV files
data = pd.read_csv('matches - matches.csv')
deliveries = pd.read_csv('deliveries.csv')

# ==================== BASIC DATA EXPLORATION ====================
# Display data
data                        # Shows entire dataframe
type(data)                  # Returns data type

# Data preview
data.head()                 # Top 5 rows (default)
data.head(2)                # Top 2 rows
data.tail(3)                # Bottom 3 rows

# Shape and size
data.shape                  # Returns (rows, columns) tuple
data.shape[0]               # Number of rows
data.shape[1]               # Number of columns
len(data)                   # Number of rows

# Data information
data.info()                 # Overall dataset information
data.describe()             # Mathematical summary (numerical columns only)

# ==================== COLUMN OPERATIONS ====================
# Single column selection
data['winner']              # Returns Series
data['winner'].shape        # Shape of Series
type(data['winner'])        # Type of single column (Series)

# Multiple column selection
data[['team1','team2','winner']]           # Returns DataFrame
data[['team1','team2','winner']].shape     # Shape of multiple columns
type(data[['team1','team2','winner']])     # Type of multiple columns (DataFrame)

# ==================== ROW OPERATIONS (iloc) ====================
# Single row selection
data.iloc[0]                # First row (Series)
data.iloc[0].shape          # Shape of single row
type(data.iloc[0])          # Type of single row (Series)

# Multiple row selection
data.iloc[1:3]              # Rows 1 to 2 (slicing)
data.iloc[1:3].shape        # Shape of sliced rows
type(data.iloc[1:3])        # Type of sliced rows (DataFrame)
data.iloc[[1,5,7]]          # Specific rows by index list

# Row and column selection combined
data.iloc[:,[4,5,10]]       # All rows, specific columns by index

# ==================== FILTERING ====================
# Boolean filtering
data['city'] == 'Hyderabad'            # Boolean mask
mask = data['city'] == 'Hyderabad'     # Store mask in variable
data[mask]                              # Apply mask to filter data
data[mask].shape[0]                     # Count filtered rows

# Date filtering
data['date'] >= '2017-01-01'            # Date comparison
mask2 = data['date'] >= '2017-01-01'    # Store date mask
data[mask2].shape                       # Apply date filter

# Multiple condition filtering
data[mask & mask2].shape[0]             # AND operation with masks

# Function for filtering
def match_count(city):
    mask = data['city'] == city
    return data[mask].shape[0]

match_count('Rajkot')                   # Call filtering function

# ==================== VALUE COUNTS ====================
# Categorical data analysis
data['winner'].value_counts()           # Count unique values
data['winner'].value_counts().head(8)   # Top 8 most frequent values
data['toss_decision'].value_counts()    # Another categorical column

# ==================== PLOTTING ====================
# Bar plots
data['winner'].value_counts().plot(kind='bar')     # Vertical bar chart
data['winner'].value_counts().head().plot(kind='barh')  # Horizontal bar chart

# Pie chart
data['toss_decision'].value_counts().plot(kind='pie')

# Histogram
data['win_by_runs'].plot(kind='hist')

# ==================== SERIES OPERATIONS ====================
# Working with Series
ms = data['winner'].value_counts()      # Create Series
ms.index                                # Get index values
ms.values                               # Get actual values
ms.index[0:5]                          # Slice index
ms['Royal Challengers Bangalore']      # Access by label

# Series arithmetic
merged = data['team1'].value_counts() + data['team2'].value_counts()
merged['Mumbai Indians']                # Access specific team

# ==================== SORTING ====================
# Series sorting
merged.sort_values()                    # Ascending sort
merged.sort_values(ascending=False)     # Descending sort

# DataFrame sorting
data.sort_values('city')                # Sort by single column (ascending)
data.sort_values('city', ascending=False)  # Sort by single column (descending)

# Multiple column sorting
data.sort_values(['city','date'])       # Sort by multiple columns
data.sort_values(['city','date'], ascending=[True,False])  # Mixed sorting

# Permanent sorting (inplace)
# data.sort_values('city', ascending=False, inplace=True)

# ==================== DUPLICATE REMOVAL ====================
# Remove duplicates
data.drop_duplicates(subset=['city'])                       # Remove city duplicates
data.drop_duplicates(subset=['city']).shape[0]              # Count unique cities
data.drop_duplicates(subset=['season','winner'])            # Multiple column duplicates

# Keep specific duplicate
data.drop_duplicates(subset=['season'], keep='last').sort_values('season', ascending=True)
data.drop_duplicates(subset=['season'], keep='last')[['season','winner']].sort_values('season', ascending=True)

# ==================== GROUP BY OPERATIONS ====================
# Basic grouping
umpire = data.groupby('umpire1')        # Create grouped object
len(umpire)                             # Number of groups
umpire.size()                           # Size of each group
umpire.size().sort_values(ascending=False)  # Sorted group sizes

# Group methods
umpire.first()                          # First row of each group
umpire.last()                           # Last row of each group
umpire.groups                           # Dictionary of groups and indices

# Access specific group
umpire.get_group('Aleem Dar')           # Get specific group data

# Aggregation operations
runs = deliveries.groupby('batsman')    # Group by batsman
runs['batsman_runs'].sum()              # Sum runs for each batsman
runs['batsman_runs'].sum().sort_values(ascending=False)  # Sorted totals

# Complex grouping examples
runs.get_group('V Kohli')               # Specific batsman data

# ==================== ADVANCED FILTERING & ANALYSIS ====================
# Finding batsmen who hit most 4s
mask = deliveries['batsman_runs'] == 4   # Filter for 4s
four = deliveries[mask]                  # Get all 4s
batsmanName = four.groupby('batsman')    # Group 4s by batsman
batsmanName.size().sort_values(ascending=False).head()  # Top 4-hitters

# Nested grouping analysis
vkruns = runs.get_group('V Kohli')
opponent = vkruns.groupby('bowling_team')['batsman_runs'].sum().sort_values(ascending=False)

# Function for complex analysis
def scored_runs(batsman_name):
    all_batsman = deliveries.groupby('batsman')
    individual_batsman = all_batsman.get_group(batsman_name)
    return individual_batsman.groupby('bowling_team')['batsman_runs'].sum().sort_values(ascending=False).iloc[0]

scored_runs('V Kohli')

# ==================== COMPLEX ANALYSIS EXAMPLE ====================
# Death over analysis (overs 16-20)
death_over_filter = deliveries['over'] > 15     # Create filter
death_over = deliveries[death_over_filter]      # Apply filter
all_batsman = death_over.groupby('batsman')     # Group by batsman
balls_Played = all_batsman.size()               # Count balls faced

# Multiple condition filtering
mask = balls_Played > 200                       # Players with >200 balls
requiredPlayer = balls_Played[mask]             # Filter players
requiredPlayerList = requiredPlayer.index.tolist()  # Convert to list

# Using isin() for filtering
mask = death_over['batsman'].isin(requiredPlayerList)
newPlayerDataframe = death_over[mask]

# Calculate strike rate
runs = newPlayerDataframe.groupby('batsman')['batsman_runs'].sum()
balls = newPlayerDataframe.groupby('batsman')['batsman_runs'].count()
strike_rate = (runs/balls) * 100
strike_rate.sort_values(ascending=False).head(1)

# ==================== SUMMARY OF KEY METHODS ====================
"""
Data Loading:
- pd.read_csv()

Data Exploration:
- .head(), .tail(), .shape, .info(), .describe(), len()

Selection:
- df['column'], df[['col1', 'col2']], df.iloc[]

Filtering:
- Boolean masks, comparison operators, .isin()

Aggregation:
- .value_counts(), .sum(), .count(), .size()

Grouping:
- .groupby(), .get_group(), .groups

Sorting:
- .sort_values()

Duplicates:
- .drop_duplicates()

Plotting:
- .plot(kind='bar'), .plot(kind='pie'), .plot(kind='hist')

Series Operations:
- .index, .values, arithmetic operations

Advanced:
- .iloc[], inplace operations, multiple conditions with &, |
"""
