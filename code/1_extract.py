import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
'''
In the extract phase you pull your data from the internet and store it locally for further processing. This way you are not constantly accessing the internet and scraping data more than you need to. This also decouples the transformation logic from the logic that fetches the data. This way if the source data changes we don't need to re-implement the transformations. 

- For each file you extract save it in `.csv` format with a header to the `cache` folder. The basic process is to read the file, add lineage, then write as a `.csv` to the `cache` folder. 
- Extract the states with codes google sheet. Save as `cache/states.csv`
- Extract the survey google sheet, and engineer a `year` column from the `Timestamp` using the `extract_year_mdy` function in `pandaslib.py`. Then save as `cache/survey.csv`
- For each unique year in the surveys: extract the cost of living for that year from the website, engineer a `year` column for that year, then save as `cache/col_{year}.csv` for example for `2024` it would be `cache/col_2024.csv`

After you've completed this part commit your changes to git, but DO NOT PUSH.'''

#TODO Write your extraction code here

# Load the data
survey_df = pd.read_csv("https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv")

us_name_df = pd.read_csv("https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv")

# Clean the data
survey_df['year'] = survey_df['Timestamp'].apply(pl.extract_year_mdy)

#survey_df['What country do you work in?'] = survey_df['What country do you work in?'].apply(pl.clean_country_usa)

# Save the data
path = r"C:\Users\conno\OneDrive - Syracuse University\Fall 2024\IST 356\ist356\assignment 5\assignment-05-ccluett50\code"
survey_df.to_csv(f'{path}/cache/survey.csv', index=False)

us_name_df.to_csv(f'{path}/cache/states.csv', index=False)

# Extract the cost of living data

years = survey_df['year'].unique()

for year in years:
    url = f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0"
    col_df = pd.read_html(url)[1]
    col_df['year'] = str(year)
    col_df.to_csv(f'{path}/cache/col_{year}.csv', index=False)


# Save the data
st.dataframe(survey_df)
st.dataframe(us_name_df)


