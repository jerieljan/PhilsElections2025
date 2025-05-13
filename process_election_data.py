import pandas as pd
import re
import os

# Create processed data directory if it doesn't exist
os.makedirs('data/processed', exist_ok=True)

def standardize_name(name):
    """
    Standardize politician names to a consistent format.
    Convert to title case and handle special cases.
    """
    # Remove all-caps formatting
    name = name.title()

    # Handle specific cases first (before general rules)
    specific_cases = {
        "Go, Bong Go": "Bong Go",
        "Bong Revilla, Ramon, Jr.": "Ramon Bong Revilla Jr.",
        "Bong Revilla": "Ramon Bong Revilla Jr.",
        "Pacquiao, Manny Pacman": "Manny Pacquiao",
        "Tolentino, Francis Tol": "Francis Tolentino",
        "Salvador, Phillip Ipe": "Phillip Salvador",
        "Revillame, Willie Wil": "Willie Revillame",
        "Tulfo, Ben Bitag": "Ben Tulfo",
        "Bosita, Colonel": "Bonifacio Bosita",
        "Rodriguez, Atty. Vic": "Vic Rodriguez",
    }

    # Check if the name (after title case) matches any specific case
    for key, value in specific_cases.items():
        if key.lower() == name.lower():
            return value

    # Handle comma-separated names (Last, First)
    if ',' in name:
        parts = name.split(',')
        if len(parts) >= 2:
            # Rearrange to "First Last" format
            name = ' '.join([part.strip() for part in parts[1:] + [parts[0]]])

    # Remove nicknames
    name = re.sub(r'\bPacman\b', '', name)
    name = re.sub(r'\bTol\b', '', name)
    name = re.sub(r'\bWil\b', '', name)
    name = re.sub(r'\bBitag\b', '', name)

    # Fix common name variations
    name_mapping = {
        'Bato Dela Rosa': 'Bato dela Rosa',
        'Panfilo Lacson': 'Ping Lacson',
        'Francis Tolentino': 'Francis Tolentino',
        'Phillip Ipe Salvador': 'Phillip Salvador',
        'Willie Revillame': 'Willie Revillame',
        'Ben Tulfo': 'Ben Tulfo',
        'Colonel Bosita': 'Bonifacio Bosita',
        'Atty. Vic Rodriguez': 'Vic Rodriguez',
        'Rodante Marcoleta': 'Rodante Marcoleta',
        'Kiko Pangilinan': 'Francis Kiko Pangilinan',
    }

    for key, value in name_mapping.items():
        if key.lower() in name.lower():
            name = value

    # Clean up extra spaces
    name = re.sub(r'\s+', ' ', name).strip()

    return name

def read_actual_results():
    """
    Read and process the actual election results data.
    """
    with open('data/raw-actual-results.md', 'r') as f:
        lines = f.readlines()

    # Extract header and data rows
    header = lines[0].strip().split('|')[1:-1]  # Remove first and last empty elements
    header = [h.strip() for h in header]

    data = []
    for line in lines[2:]:  # Skip header and separator lines
        if '|' in line:
            row = line.strip().split('|')[1:-1]  # Remove first and last empty elements
            row = [cell.strip() for cell in row]
            data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data, columns=header)

    # Standardize candidate names
    df['Standardized Name'] = df['Candidate Name'].apply(standardize_name)

    # Clean up number of votes (remove commas)
    df['Number of Votes'] = df['Number of Votes'].str.replace(',', '').astype(int)

    return df

def read_opinion_polls():
    """
    Read and process the opinion poll data.
    """
    with open('data/raw-opinion-poll-data.md', 'r') as f:
        lines = f.readlines()

    # Extract header and data rows
    header = []
    for cell in lines[0].strip().split('|')[1:-1]:  # Remove first and last empty elements
        cell = cell.strip()
        # Handle multi-line headers with <br>
        cell = cell.replace('<br>', ' ')
        header.append(cell)

    data = []
    for line in lines[2:]:  # Skip header and separator lines
        if '|' in line:
            row = line.strip().split('|')[1:-1]  # Remove first and last empty elements
            row = [cell.strip() for cell in row]
            data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data, columns=header)

    # Standardize candidate names
    df['Standardized Name'] = df['Candidate'].apply(standardize_name)

    # Convert poll percentages to numeric values
    for col in df.columns[2:]:  # Skip Candidate and Party columns
        if 'OCTA' in col or 'SWS' in col or 'Pulse Asia' in col or 'WR Numero' in col or 'Arkipelago Analytics' in col or 'The Center' in col or 'DZRH' in col or 'Publicus Asia' in col:
            # Remove % signs and convert to float
            df[col] = df[col].str.replace('%', '').str.replace('**', '').str.replace('*', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def main():
    # Process actual results data
    results_df = read_actual_results()
    print(f"Processed {len(results_df)} candidates from actual results")

    # Process opinion poll data
    polls_df = read_opinion_polls()
    print(f"Processed {len(polls_df)} candidates from opinion polls")

    # Save processed data to CSV
    results_df.to_csv('data/processed/actual_results.csv', index=False)
    polls_df.to_csv('data/processed/opinion_polls.csv', index=False)

    # Create a mapping file to help with name matching
    name_mapping = pd.DataFrame({
        'Original Name': list(results_df['Candidate Name']) + list(polls_df['Candidate']),
        'Standardized Name': list(results_df['Standardized Name']) + list(polls_df['Standardized Name'])
    }).drop_duplicates()

    name_mapping.to_csv('data/processed/name_mapping.csv', index=False)
    print(f"Created name mapping with {len(name_mapping)} entries")

    print("Data processing complete. Files saved to data/processed/")

if __name__ == "__main__":
    main()
