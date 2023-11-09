import pandas as pd #Data manipulation library
import os #Module for file operations
import re #Module for pattern searching 

"""Function to read each CSV file individually into a pandas DataFrame, 
extract the week ending date from the file's name using a regular expression, 
calculate the corresponding week starting date, 
and then add these as new columns to the df ."""

def csv_extraction(source_file):
    
    #Read the CSV file into a pandas DataFrame for conversion
    df = pd.read_csv(source_file)
    #Variable date_match declared using the search function from the re module to find a o find a date pattern (YYYY-MM-DD) in the source_file string
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', source_file)
    #Conditional statement to check if date_match found a pattern that matches the date format
    if date_match:
    #Extracts the matched pattern (the date) from date_match and groups them
        week_end = date_match.group(1)
    #Convert the week_end string to a datetime object and perform subtraction to find the week_start_date
        week_end_date = pd.to_datetime(week_end)
    #Calculate the week_start as 6 days before week_end
        week_start_date = week_end_date - pd.Timedelta(days=7)
    #Add the week start and end dates as new columns to the DataFrame
        df['week_start'] = week_start_date.strftime('%Y-%m-%d')
        df['week_end'] = week_end_date.strftime('%Y-%m-%d')
    
    return df

spotify_sa_df = pd.DataFrame()
source_files = os.listdir('/Desktop/Spotify API/CSV') 

#Loop through the files, call the csv_extraction function and create a new DataFrame 
for f in source_files:
    if f.endswith('.csv'):
        file_path = os.path.join('/Desktop/Spotify API/CSV', f) #Using os module to process .csv files
        print(f"Processing file: {file_path}")
        #Calling the function to align df columns with corresponding .csv date from file_path and concatenate into rows (starting with a new index)
        spotify_sa_df = pd.concat([spotify_sa_df, csv_extraction(file_path)], ignore_index=True)

#Save the DataFrame to an Excel file
spotify_sa_df.to_excel('spotify_sa_chart.xlsx', engine="openpyxl")