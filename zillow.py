"""
zillow.py - Script to extract and filter data from a Google Sheet
"""
import pandas as pd
import requests
import io
import os

def main():
    sheet_url = "https://docs.google.com/spreadsheets/d/1mRriPayOE0q67VBvX3M0mL5WJaZQQvRxoYefNFqiOmQ/export?format=csv"
    
    try:
        print("Attempting to fetch data from Google Sheets...")
        response = requests.get(sheet_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        df = pd.read_csv(io.StringIO(response.text))
        print("Successfully fetched data from Google Sheets.")
        
    except Exception as e:
        print(f"Error fetching from Google Sheets: {e}")
        print("Using local KEYS.csv as backup...")
        
        if os.path.exists("KEYS.csv"):
            df = pd.read_csv("KEYS.csv")
            print("Successfully loaded data from KEYS.csv")
        else:
            print("Error: KEYS.csv not found")
            return 1
    
    state_abbrev_map = {}
    if os.path.exists("KEYS.csv"):
        keys_df = pd.read_csv("KEYS.csv")
        for _, row in keys_df.iterrows():
            if row['region_type'] == 'state' and not pd.isna(row['zillow_region_name']) and not pd.isna(row['state_abbreviation']):
                state_abbrev_map[row['zillow_region_name']] = row['state_abbreviation']
    
    result_df = pd.DataFrame({
        'key_row': df.iloc[:, 0],
        'regionname': df.iloc[:, 2],
        'regiontype': df.iloc[:, 5]
    })
    
    result_df = result_df.dropna(subset=['regionname'])
    
    result_df = result_df[result_df['regionname'] != "RegionName"]
    
    def get_location(row):
        if row['regiontype'] == 'country':
            return 'US'
        elif row['regiontype'] == 'state':
            return state_abbrev_map.get(row['regionname'], '')
        elif row['regiontype'] == 'metro':
            if isinstance(row['regionname'], str) and len(row['regionname']) >= 2:
                return row['regionname'][-2:]
            return ''
        return ''
    
    result_df['location'] = result_df.apply(get_location, axis=1)
    
    result_df.to_csv('zillow_data.csv', index=False)
    
    print(f"Successfully created zillow_data.csv with {len(result_df)} rows.")
    
    return 0

if __name__ == "__main__":
    exit(main())
