# Zillow Analysis

This repository contains a Python script to extract and filter data from a Google Sheet containing Zillow-related information.

## Files

- `zillow.py`: Python script that downloads data from a Google Sheet and filters it based on specific criteria
- `zillow_data.csv`: Generated CSV file containing the filtered data with key_row, regiontype, and regionname columns

## How It Works

The script performs the following operations:
1. Downloads data from the specified Google Sheet
2. Extracts the key_row (column 1), regionname (column 3), and regiontype (column 6)
3. Filters out rows that don't have values in the regionname column
4. Saves the filtered data to zillow_data.csv

## Requirements

- Python 3.x
- pandas
- requests
