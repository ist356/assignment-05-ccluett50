import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

# Load the data
path = r"C:\Users\conno\OneDrive - Syracuse University\Fall 2024\IST 356\ist356\assignment 5\assignment-05-ccluett50\code"
survey_data = pd.read_csv(f"{path}/cache/survey.csv")
states_data = pd.read_csv(f"{path}/cache/states.csv")

years = survey_data['year'].unique()

col_dfs = {}
for year in years:
    col_dfs[year] = pd.read_csv(f"{path}/cache/col_{year}.csv")

combined_col = pd.concat([col_dfs[year] for year in years])
combined_col['year'] = combined_col['year'].astype(str)


#st.dataframe(combined_col)

# Clean the data
survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

survey_states_combined = survey_data.merge(states_data, left_on='If you\'re in the U.S., what state do you work in?', right_on='State', how='inner')
#st.dataframe(survey_states_combined)

survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']
survey_states_combined['year'] = survey_states_combined['year'].astype(str)

combined = survey_states_combined.merge(combined_col, left_on=['year', '_full_city'], right_on=['year', 'City'], how='inner')

#st.dataframe(combined)


#Cleaning salary column
combined['__annual_salary_cleaned'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)


#Adjusting salary based on cost of living

combined['_annual_salary_adjusted'] = round((combined['__annual_salary_cleaned'] / combined['Cost of Living Index']) * 100, 2)
st.dataframe(combined)

# Save the data
survey_data.to_csv(f'{path}/cache/survey_dataset.csv', index=False)

# Create the reports

# Report 1
report1 = combined.pivot_table(index='_full_city', columns='How old are you?', values='_annual_salary_adjusted', aggfunc='mean')

st.dataframe(report1)

report1.to_csv(f'{path}/cache/annual_salary_adjusted_by_location_and_age.csv')

# Report 2

report2 = combined.pivot_table(index='_full_city', columns='What is your highest level of education completed?', values='_annual_salary_adjusted', aggfunc='mean')

st.dataframe(report2)

report2.to_csv(f'{path}/cache/annual_salary_adjusted_by_location_and_education.csv')

