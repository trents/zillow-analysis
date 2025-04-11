"""
zillow.py - Script to extract and filter data from a Google Sheet
"""
import pandas as pd
import requests
import io

def main():
    sheet_url = "https://docs.google.com/spreadsheets/d/1mRriPayOE0q67VBvX3M0mL5WJaZQQvRxoYefNFqiOmQ/export?format=csv"
    
    try:
        response = requests.get(sheet_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        df = pd.read_csv(io.StringIO(response.text))
        
        
        result_df = pd.DataFrame({
            'key_row': df.iloc[:, 0],
            'regionname': df.iloc[:, 2],
            'regiontype': df.iloc[:, 5]
        })
        
        result_df = result_df.dropna(subset=['regionname'])
        
        result_df.to_csv('zillow_data.csv', index=False)
        
        print(f"Successfully created zillow_data.csv with {len(result_df)} rows.")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
