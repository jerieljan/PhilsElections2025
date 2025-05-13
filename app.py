import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Philippines Elections 2025 Analysis",
    page_icon="🗳️",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    actual_results = pd.read_csv('data/processed/actual_results.csv')
    opinion_polls = pd.read_csv('data/processed/opinion_polls.csv')
    name_mapping = pd.read_csv('data/processed/name_mapping.csv')
    return actual_results, opinion_polls, name_mapping

actual_results, opinion_polls, name_mapping = load_data()

# Get the actual top 12 senators
actual_top12 = actual_results.head(12)['Standardized Name'].tolist()

# Function to get the top 12 candidates from a opinion polling
def get_top12_from_poll(poll_column):
    # Create a dataframe with just the candidate names and their poll results
    poll_df = opinion_polls[['Standardized Name', poll_column]].copy()
    # Remove rows with NaN values
    poll_df = poll_df.dropna(subset=[poll_column])
    # Sort by poll results in descending order
    poll_df = poll_df.sort_values(by=poll_column, ascending=False)
    # Return the top 12 candidates
    return poll_df.head(12)['Standardized Name'].tolist()

# Create a dataframe to store the comparison results
def generate_comparison_results():
    poll_columns = [col for col in opinion_polls.columns if col not in ['Candidate', 'Party', 'Standardized Name']]
    comparison_results = []

    # For each opinion polling
    for poll_column in poll_columns:
        # Get the top 12 candidates from this poll
        poll_top12 = get_top12_from_poll(poll_column)

        # Count how many candidates from the actual top 12 are in this poll's top 12
        correct_count = sum(1 for candidate in poll_top12 if candidate in actual_top12)

        # Calculate accuracy percentage
        accuracy = (correct_count / 12) * 100

        # Add to results
        comparison_results.append({
            'Opinion Polling': poll_column,
            'Correct Predictions': correct_count,
            'Accuracy (%)': accuracy,
            'Predicted Top 12': poll_top12
        })

    # Convert to dataframe
    return pd.DataFrame(comparison_results)

comparison_df = generate_comparison_results()

# Sidebar setup
with st.sidebar:
    """
    # Comparison of Opinion Polls vs Actual PH 2025 Election Results
    
    This project analyzes the **2025 Philippines election results** and compares them with **opinion polls
    conducted before the election.** The analysis focuses on how accurately different polling stations
    predicted the actual top 12 senators.
    
    1. **Select an Opinion Polling**: Choose an opinion polling to compare with the actual results.
    2. Switch to the **Summary** tab to view the accuracy of each opinion polling and findings.
    
    Sources:
    - Election Results: [abs-cbn.com](https://halalanresults.abs-cbn.com/)
    - Opinion Polls: [Wikipedia](https://en.m.wikipedia.org/wiki/Opinion_polling_for_the_2025_Philippine_Senate_election)
    
    """
    st.info("NOTE: Actual results used are *partial* but mostly definitive results from transmitted election returns. Roughly around ~95% transmitted at the time of capture.")

# Initialize tabs
individual_polling, summary = st.tabs(["Individual Opinion Polling", "Summary"])

# Opinion Polling Analysis Page
with individual_polling:
    st.title("Opinion Polling Predictions vs Actual Results")
    
    # Get list of opinion pollings
    poll_columns = [col for col in opinion_polls.columns if col not in ['Candidate', 'Party', 'Standardized Name']]
    
    # Create dropdown for selecting opinion polling
    selected_poll = st.selectbox("Select Opinion Polling", poll_columns)
    
    # Get the selected opinion polling's data
    poll_data = comparison_df[comparison_df['Opinion Polling'] == selected_poll].iloc[0]
    
    # Display accuracy information
    st.subheader(f"Opinion Polling: {selected_poll}")
    st.write(f"Correct Predictions: {poll_data['Correct Predictions']} out of 12 ({poll_data['Accuracy (%)']}%)")
    
    # Create columns for side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Predicted Top 12")
        for i, candidate in enumerate(poll_data['Predicted Top 12'], 1):
            # Check if this candidate is in the actual top 12
            is_correct = candidate in actual_top12
            status = "✓" if is_correct else "✗"
            
            # Get the actual rank if the candidate is in the top 12
            actual_rank = actual_top12.index(candidate) + 1 if is_correct else "Not in top 12"
            
            st.write(f"{i}. {candidate} {status} (Actual Rank: {actual_rank})")
    
    with col2:
        st.subheader("Actual Top 12")
        for i, candidate in enumerate(actual_top12, 1):
            # Check if this candidate is in the predicted top 12
            is_predicted = candidate in poll_data['Predicted Top 12']
            status = "✓" if is_predicted else "✗"
            
            # Get the predicted rank if the candidate is in the predicted top 12
            predicted_rank = poll_data['Predicted Top 12'].index(candidate) + 1 if is_predicted else "Not in predicted top 12"
            
            st.write(f"{i}. {candidate} {status} (Predicted Rank: {predicted_rank})")
    
    # Display poll percentages for all candidates
    st.subheader("Poll Percentages for All Candidates")
    st.info(f"Displaying predicted rankings and their poll percentages by **{selected_poll}**. Green entries are in the actual top 12, red entries are not.")
    
    # Create a dataframe with just the candidate names and their poll results
    poll_percentages = opinion_polls[['Standardized Name', selected_poll]].copy()
    # Remove rows with NaN values
    poll_percentages = poll_percentages.dropna(subset=[selected_poll])
    # Sort by poll results in descending order
    poll_percentages = poll_percentages.sort_values(by=selected_poll, ascending=False)
    
    # Create a bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get top 20 candidates for better visualization
    top_candidates = poll_percentages.head(20)
    
    # Create the bar chart
    bars = sns.barplot(x=selected_poll, y='Standardized Name', data=top_candidates, ax=ax)
    
    # Color the bars based on whether the candidate is in the actual top 12
    for i, bar in enumerate(bars.patches):
        candidate = top_candidates.iloc[i]['Standardized Name']
        if candidate in actual_top12:
            bar.set_color('green')
        else:
            bar.set_color('red')
    
    plt.title(f'Top 20 Candidates in {selected_poll}')
    plt.xlabel('Poll Percentage')
    plt.tight_layout()
    
    st.pyplot(fig)

# Summary of Accuracy Page
with summary:
    st.title("Summary of Opinion Polling Accuracy")
    
    # Sort by accuracy
    sorted_comparison = comparison_df.sort_values('Accuracy (%)', ascending=False)
    
    # Display the comparison results
    st.subheader("Opinion Polling Ranked by Accuracy")
    st.dataframe(sorted_comparison[['Opinion Polling', 'Correct Predictions', 'Accuracy (%)']])
    
    # Visualize the accuracy of each opinion polling
    st.subheader("Opinion Polling Accuracy Visualization")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='Opinion Polling', y='Accuracy (%)', data=sorted_comparison, ax=ax)
    plt.xticks(rotation=90)
    plt.title('Opinion Polling Accuracy in Predicting Top 12 Senators')
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Most accurate opinion polling
    st.subheader("Most Accurate Opinion Pollings")
    for i, (_, row) in enumerate(sorted_comparison.head(3).iterrows(), 1):
        st.write(f"{i}. {row['Opinion Polling']}: {row['Correct Predictions']} correct ({row['Accuracy (%)']}%)")
    
    # Least accurate opinion polling
    st.subheader("Least Accurate Opinion Pollings")
    for i, (_, row) in enumerate(sorted_comparison.tail(3).iterrows(), 1):
        st.write(f"{i}. {row['Opinion Polling']}: {row['Correct Predictions']} correct ({row['Accuracy (%)']}%)")
    
    # Overall average accuracy
    avg_accuracy = comparison_df['Accuracy (%)'].mean()
    st.subheader("Overall Average Accuracy")
    st.write(f"Average Accuracy Across All Opinion Polling: {avg_accuracy:.2f}%")
    
    # Most commonly missed candidates
    st.subheader("Candidates in the Actual Top 12 Most Commonly Missed by Opinion Pollings")
    
    missed_counts = {}
    for senator in actual_top12:
        missed_count = sum(1 for _, row in comparison_df.iterrows() if senator not in row['Predicted Top 12'])
        missed_counts[senator] = missed_count
    
    # Sort by most missed
    for senator, count in sorted(missed_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        if count > 0:
            miss_percentage = (count / len(comparison_df)) * 100
            st.write(f"- {senator}: Missed by {count} opinion pollings ({miss_percentage:.1f}%)")
    
    # Most commonly incorrectly included candidates
    st.subheader("Candidates Not in the Actual Top 12 Most Commonly Included by Opinion Pollings")
    
    incorrect_counts = {}
    for _, row in comparison_df.iterrows():
        for candidate in row['Predicted Top 12']:
            if candidate not in actual_top12:
                incorrect_counts[candidate] = incorrect_counts.get(candidate, 0) + 1
    
    # Sort by most included
    for candidate, count in sorted(incorrect_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        if count > 0:
            include_percentage = (count / len(comparison_df)) * 100
            st.write(f"- {candidate}: Incorrectly included by {count} opinion pollings ({include_percentage:.1f}%)")