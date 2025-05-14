# Comparing Opinion Polls vs PH 2025 Election Results

This project analyzes the 2025 Philippines election results and compares them with opinion polls conducted before the election. The analysis focuses on how accurately different polling stations predicted the actual top 12 senators.

Disclaimer: This is an **unofficial quick analysis project** and is purely exploratory in nature. The findings are not part of any formal study and **should not be considered as official election analysis**.

## Features

The project includes a Streamlit app with two main pages:

1. **Polling Station Analysis**: 
   - Select a polling station from a dropdown menu
   - View detailed comparison between the polling station's predictions and actual results
   - See side-by-side comparison of predicted vs. actual top 12 candidates
   - Visualize poll percentages for top candidates with color-coded bars (green for correctly predicted candidates, red for incorrect predictions)

2. **Summary of Accuracy**:
   - View overall ranking of polling stations by accuracy
   - See visualization of polling station accuracy
   - Get insights on most and least accurate polling stations
   - Understand which candidates were most commonly missed or incorrectly included in predictions

## Data

The app uses processed data from:
- `data/processed/actual_results.csv`: The actual election results
- `data/processed/opinion_polls.csv`: Opinion poll data from various polling stations
- `data/processed/name_mapping.csv`: Mapping of candidate names for standardization

These are sourced from the following:

## Sources:

- Election Results: [abs-cbn.com](https://halalanresults.abs-cbn.com/)
- Opinion Polls: [Wikipedia](https://en.m.wikipedia.org/wiki/Opinion_polling_for_the_2025_Philippine_Senate_election)

## Notes:

- This only covers the recent opinion polls. Polls before April 2025 are not included.
- This uses *partial* results from a third-party, but should be mostly accurate. Data was used when it was around ~95% transmitted.


## How to Run

1. Make sure you have Python installed (Python 3.7+ recommended)
2. Install the required packages:
   ```
   pip install streamlit pandas matplotlib seaborn numpy
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
4. The app will open in your default web browser

## Project Structure

- `app.py`: The Streamlit application
- `process_election_data.py`: Script to process raw data into CSV files
- `notebook.ipynb`: Jupyter notebook with original analysis
- `data/`: Directory containing raw and processed data
  - `raw/`: Raw data files
  - `processed/`: Processed CSV files

## Analysis Methodology

The analysis compares each polling station's predicted top 12 candidates with the actual top 12 elected senators. Accuracy is calculated as the percentage of correctly predicted candidates in the top 12.