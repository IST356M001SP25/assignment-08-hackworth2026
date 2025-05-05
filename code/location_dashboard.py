'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="wide")

tickets_df = pd.read_csv('./cache/tickets_in_top_locations.csv')

# Page title and description
st.header('Syracuse Parking Ticket Hotspots')
st.write('Discover where Syracuse racks up over $1,000 in parking violations and explore patterns by time and day.')

# Select location
locations_list = sorted(tickets_df['location'].unique())
chosen_location = st.selectbox('Pick a location to explore:', locations_list)

# Filter dataset for selected location
if chosen_location:
    loc_df = tickets_df.query('location == @chosen_location')

    # Summary metrics
    total_tickets = loc_df.shape[0]
    total_fines = loc_df['amount'].sum()

    st.subheader(f'Summary for {chosen_location}')
    st.metric('Total Tickets', total_tickets)
    st.metric('Total Fines Collected', f"${total_fines:,.2f}")

    # Charts in a grid layout
    st.subheader('Ticket Patterns')

    col_a, col_b = st.columns(2)

    with col_a:
        fig_hour, ax_hour = plt.subplots()
        sns.countplot(data=loc_df, x='hourofday', ax=ax_hour)
        ax_hour.set_title('Tickets by Hour of Day')
        ax_hour.set_xlabel('Hour')
        ax_hour.set_ylabel('Number of Tickets')
        st.pyplot(fig_hour)

    with col_b:
        fig_day, ax_day = plt.subplots()
        sns.countplot(data=loc_df, x='dayofweek', ax=ax_day, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        ax_day.set_title('Tickets by Day of Week')
        ax_day.set_xlabel('Day')
        ax_day.set_ylabel('Number of Tickets')
        st.pyplot(fig_day)

    # Map visualization
    st.subheader('Location Map')
    st.map(loc_df[['lat', 'lon']])