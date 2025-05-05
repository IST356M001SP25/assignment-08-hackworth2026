import pandas as pd
import streamlit as st 


def top_locations(violations_df: pd.DataFrame, threshold=1000) -> pd.DataFrame:
    location_totals = (
        violations_df.groupby('location')['amount']
        .sum()
        .reset_index()
        .sort_values('amount', ascending=False)
    )
    filtered_locations = location_totals[location_totals['amount'] >= threshold]
    return filtered_locations

def top_locations_mappable(violations_df: pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locs = top_locations(violations_df, threshold)
    location_coords = violations_df[['location', 'lat', 'lon']].drop_duplicates('location')
    combined = pd.merge(top_locs, location_coords, on='location', how='inner')
    return combined.drop_duplicates()

def tickets_in_top_locations(violations_df: pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locs = top_locations(violations_df, threshold)
    tickets = violations_df[violations_df['location'].isin(top_locs['location'])]
    return tickets

if __name__ == '__main__':
    print("Starting ETL pipeline...")
    input_file = './cache/final_cuse_parking_violations.csv'
    print(f"Loading data from {input_file}")
    violations_data = pd.read_csv(input_file)

    output_top_locations = top_locations(violations_data)
    output_top_locations.to_csv('./cache/top_locations.csv', index=False)
    print("Saved top locations data.")

    output_mappable = top_locations_mappable(violations_data)
    output_mappable.to_csv('./cache/top_locations_mappable.csv', index=False)
    print("Saved mappable top locations data.")

    output_tickets = tickets_in_top_locations(violations_data)
    output_tickets.to_csv('./cache/tickets_in_top_locations.csv', index=False)
    print("Saved tickets in top locations data.")
