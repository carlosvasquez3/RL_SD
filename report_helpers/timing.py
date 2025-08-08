import pandas as pd

def generate_timing_table(csv_filename, max_run=1000):
    """
    Generate timing statistics table from experimental results.
    
    Parameters:
    csv_filename: Path to CSV file with experimental results
    max_run: Maximum run number to filter for final timing statistics
    
    Returns:
    DataFrame with timing statistics grouped by treatment conditions
    """
    df = pd.read_csv(csv_filename, delimiter=",")
    filtered_df = df[df["Run"] == max_run]
    timing_stats = filtered_df.groupby(["Epsilon_Level", "Rho_Level"])["Execution_Time"].agg(["mean", "std"]).reset_index()
    timing_stats.to_csv("execution_time_statistics.csv", index=False)
    return timing_stats