# COVID-19 Worldwide Analytics: Data from Our World in Data
## https://github.com/owid/covid-19-data/tree/master/public/data

# RQ1: is there a correlation between pop. 65+ and pop. 70+ in terms of total deaths?
# RQ2: is there a correlation between gdp per capia and total deaths? (chi-square)
# RQ3: diabetes prevelance
# RQ4: stringency index correlation with covid figures


#========================================================================================
### Importing packages

import pandas as pd # pandas for most everything
import numpy as np
import seaborn as sns # data visualization
from matplotlib import pyplot as plt # data visualization
import statsmodels.api as sm # stats procedures
from statsmodels.formula.api import ols # regression procedures
import scipy.stats as stats # stats procedures
from scipy.stats import chi2_contingency # chi2/contingency tables
from statsmodels.stats.outliers_influence import OLSInfluence # regression procedures


#========================================================================================
### Reading in the data

data = pd.read_excel('/Users/zoezirlin/Desktop/COVID DATA/owid-covid-data.xlsx') # excel file


#========================================================================================
# Finding out how many countries are represented in this dataset

freq = pd.value_counts(data['location']) #creating frequency table through pandas value count function 
freq #printing the frequency table


#========================================================================================
# Analyzing total new cases by country

pt1 = pd.pivot_table(data, index = ['location'], values = ['new_cases'], aggfunc = np.sum)
pt1 # Here we see that we have too many countries (categories) to visualize all at once
# We will need to segment the data!
 

#========================================================================================
# Segmenting dataset into six separate dataframes by continent designation of country

pd.value_counts(data['continent']) # checking the counts of each continent to ensure normal distribution
# oceania has significantly less instances that europe, which has the most
# europe and asia have the most instances

europe = data[data['continent']=='Europe'] # creating dataframe that has only european countries
europe = europe.sort_values(['total_deaths'], ascending = False) # sorting the df by total deaths from most to least

asia = data[data['continent']=='Asia']
asia = asia.sort_values(['total_deaths'], ascending = False)

africa = data[data['continent']=='Africa']
africa = africa.sort_values(['total_deaths'], ascending = False)

north_america = data[data['continent']=='North America']
north_america = north_america.sort_values(['total_deaths'], ascending = False)

south_america = data[data['continent']=='South America']
south_america = south_america.sort_values(['total_deaths'], ascending = False)

oceania = data[data['continent']=='Oceania']
oceania = oceania.sort_values(['total_deaths'], ascending = False)


#========================================================================================
### Analyzing European Countries

# Europe - Average of total cases per million, shows the rate of death positioned against population of country

pte1 = pd.pivot_table(europe, index = ['location'], values = ['total_cases_per_million'], aggfunc = np.mean)
pte1 = pte1.sort_values(['total_cases_per_million'], ascending=[False])
pte1[:5]
# vatican has the most average cases per million, perhaphs because they have such miniscule population
# small countries seem to have the most cases per million


# Europe- Sum of new deaths, shows the total of deaths over the weeks reported

pte2 = pd.pivot_table(europe, index = ['location'], values = ['total_deaths'], aggfunc = np.sum)
pte2 = pte2.sort_values(['total_deaths'], ascending=[False])
pte2[:5]
# U.K. leads in total deaths, followed by italy, france, spain and belgium (IN EUROPE)



# Europe- Sum of new cases per million, shows the rate of total of cases by country

pte3 = pd.pivot_table(europe, index = ['location'], values = ['new_cases_per_million'], aggfunc = np.sum)
pte2 = pte3.sort_values(['new_cases_per_million'], ascending=[False])
pte3[:5]


# Visualizing Death Counts for European Countries by Total Deaths

plt.figure(figsize=(25,7))
sns.set()
sns.set_context("talk")

chart = sns.barplot(x='location', y='new_deaths', estimator=sum,
                    data=europe,
                    palette='Paired'
)

plt.xticks(
    rotation=45, 
    horizontalalignment='right',
    fontweight='light',
)

chart.set_title('Death Count by Location in European Countries')
chart.set_xlabel('Location')
chart.set_ylabel('Death Count')


# Visualizing COVID-19 Cases for European Countries by Total Cases

plt.figure(figsize=(25,7))
sns.set()
sns.set_context("talk")

chart = sns.barplot(x='location', y='new_cases', estimator=sum,
                    data=europe,
                    palette='Paired'
)

plt.xticks(
    rotation=45, 
    horizontalalignment='right',
    fontweight='light',
)

chart.set_title('Case Count by Location in European Countries| Note: Ordered by Most Deaths to Least')
chart.set_xlabel('Location')
chart.set_ylabel('Case Count')


#========================================================================================
### Analyzing Asian Countries

# Asia - Average of total cases per million, shows the rate of death positioned against population of country

pta1 = pd.pivot_table(asia, index = ['location'], values = ['total_cases_per_million'], aggfunc = np.mean)
pta1 = pta1.sort_values(['total_cases_per_million'], ascending=[False])
pta1[:5]
# Qatar has the most average cases per million


# Asia- Sum of new deaths, shows the total of deaths over the weeks reported

pta2 = pd.pivot_table(asia, index = ['location'], values = ['total_deaths'], aggfunc = np.sum)
pta2 = pta2.sort_values(['total_deaths'], ascending=[False])
pta2[:5]
# India has the most cumulative total deaths


# Asia- Sum of new cases per million, shows the rate of total of cases by country

pta3 = pd.pivot_table(asia, index = ['location'], values = ['new_cases_per_million'], aggfunc = np.sum)
pta3 = pta3.sort_values(['new_cases_per_million'], ascending=[False])
pta3[:5]
# Qatar has the most new cases per million, as well as having the most total cases per million


# Visualizing Death Counts for Asian Countries by Total Deaths

plt.figure(figsize=(25,7))
sns.set()
sns.set_context("talk")

chart = sns.barplot(x='location', y='new_deaths', estimator=sum,
                    data=asia,
                    palette='Paired'
)

plt.xticks(
    rotation=45, 
    horizontalalignment='right',
    fontweight='light',
)

chart.set_title('Death Count by Location in Asian Countries')
chart.set_xlabel('Location')
chart.set_ylabel('Death Count')


# Visualizing COVID-19 Cases for Asian Countries by Total Cases

plt.figure(figsize=(25,7))
sns.set()
sns.set_context("talk")

chart = sns.barplot(x='location', y='new_cases', estimator=sum,
                    data=asia,
                    palette='Paired'
)

plt.xticks(
    rotation=45, 
    horizontalalignment='right',
    fontweight='light',
)

chart.set_title('Case Count by Location in Asian Countries| Note: Ordered by Most Deaths to Least')
chart.set_xlabel('Location')
chart.set_ylabel('Case Count')


#========================================================================================
# Taking care of the NA variables
print(data.isnull()) # printing true/false is na for variables

print(data.isnull().sum())

# every variable has null counts except for location and date!

# create new dataset for regression procedures without NAs


#========================================================================================
# Statistical procedures


## Correlative relationships
corr = data.corr()
    # handwashing facilities x extreme poverty: -.7703
    # hospital beds per thousand x median age: .6606
    # life expectancy x hand washing facilities: .825
    # extreme poverty x life expectancy: -.748
    # female smokers x aged 70+: .781
    # stringency index x positive rate: .329 (low, kind like it doesnt much work)
# Variables of interest
    # continent: categorical (need to recode)
    # date: continuous
    # total cases: continuous
    # new cases: continuous
    # total deaths: continuous
    # new deaths: continuous
    # total cases/mil: continuous
    # new cases/mil: continuous
    # total deaths/mil: continuous
    # total cases/mil: continuous
    # stringency index: continuous
    # population density: continuous
    # gdp per capita: continuous
    # life expectancy: continuous


# Regression procedure: predicting total cases


# Scatterplot for total cases by stringency index
plt.figure(figsize=(7,7))
sns.set()
sns.set_context("talk")

chart = sns.scatterplot(data=data, y='total_cases', x= 'stringency_index', palette='Paired')

chart.set_title('Scatterplot for Total Cases by Stringency Index')
chart.set_xlabel('Stringency Index')
chart.set_ylabel('Total Cases')


# Scatterplot for total cases by gdp per capita
plt.figure(figsize=(7,7))
sns.set()
sns.set_context("talk")

chart = sns.scatterplot(data=data, y='total_cases', x= 'gdp_per_capita', palette='Paired')

chart.set_title('Scatterplot for Total Cases by GPA Per Capita')
chart.set_xlabel('Stringency Index')
chart.set_ylabel('Total Cases')


# Scatterplot for total cases by life expectancy
plt.figure(figsize=(7,7))
sns.set()
sns.set_context("talk")

chart = sns.scatterplot(data=data, y='total_cases', x= 'life_expectancy', palette='Paired')

chart.set_title('Scatterplot for Total Cases by Life Expectancy')
chart.set_xlabel('Stringency Index')
chart.set_ylabel('Total Cases')


# Creating new dataset without NAs 
data1 = data.copy()
data1 = data1.dropna()

pd.value_counts(data['location'])
# this widdled down dataframe has 164 countries
# there are 195 countries in the world
# this represents 84% of countries


# Regression procedure no.1
X = data1[['life_expectancy']]
y = data1['total_cases']
X = sm.add_constant(X)

model_1 = sm.OLS(y,X).fit()
predictions_1 = model_1.predict(X)

model_1.summary()


# Regression procedure no.2
X = data1[['life_expectancy']]
y = data1['total_deaths']
X = sm.add_constant(X)

model_1 = sm.OLS(y,X).fit()
predictions_1 = model_1.predict(X)

model_1.summary()


# Regression procedure no.3
X = data1[['cardiovasc_death_rate']]
y = data1['total_deaths']
X = sm.add_constant(X)

model_1 = sm.OLS(y,X).fit()
predictions_1 = model_1.predict(X)

model_1.summary()


# Regression procedure no.4
## significant model, 78% of the variability explained
X = data1[['handwashing_facilities']]
y = data1['extreme_poverty']
X = sm.add_constant(X)

model_1 = sm.OLS(y,X).fit()
predictions_1 = model_1.predict(X)

model_1.summary()


# Regression procedure no.5
## significant model, 50% of the variability explained
X = data1[['handwashing_facilities']]
y = data1['life_expectancy']
X = sm.add_constant(X)

model_1 = sm.OLS(y,X).fit()
predictions_1 = model_1.predict(X)

model_1.summary()



























