import streamlit as st


# app.py, run with 'streamlit run app.py'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('BNEF Tier PV.xlsx')  # will work for Excel files

st.title("BNEF Tier PV")  # add a title
st.write(df)  # visualize my dataframe in the Streamlit app

# Convert Period to datetime for easier manipulation
#df['Period'] = pd.to_datetime(df['Period'], format='%YQ%q')
#df['Period'] = pd.Period(df['Period'], freq="Q").start_time
df['Period'] = df['Period'].apply(lambda x: pd.Period(x, freq="Q").start_time)


# Calculate annual production
annual_data = df.groupby(['Period', 'Brand'])['Annual module capacity, MW/year'].sum().reset_index()

st.title("Annual module capacity, MW/year")
# Filter by brand
brands = annual_data['Brand'].unique()
selected_brands = st.multiselect("Select Brands", brands)

# Filter data based on selected brands
filtered_data = annual_data[annual_data['Brand'].isin(selected_brands)]

# Create a line plot
fig, ax = plt.subplots(figsize=(10, 6))
for brand in filtered_data['Brand'].unique():
    brand_data = filtered_data[filtered_data['Brand'] == brand]
    ax.plot(brand_data['Period'], brand_data['Annual module capacity, MW/year'], label=brand)

ax.set_xlabel('Period')
ax.set_ylabel('Annual module capacity, MW/year')
ax.set_title('Annual module capacity, MW/year')
ax.legend()

# Display the plot
st.pyplot(fig)

# Plot with gaps
st.title("BNEF Tier PV (Gaps)")  # add a title

# Load the data
data = pd.read_excel('BNEF Tier PV.xlsx')

# Create a complete set of periods for each brand
years = data['Year'].unique()
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
brands = data['Brand'].unique()

# Create a multi-index DataFrame with all possible combinations
index = pd.MultiIndex.from_product([years, quarters, brands], names=['Year', 'Quarter', 'Brand'])
complete_data = pd.DataFrame(index=index).reset_index()

# Merge the original data into the complete set
complete_data = pd.merge(complete_data, data[['Year', 'Quarter', 'Brand', 'Annual module capacity, MW/year']], 
                         on=['Year', 'Quarter', 'Brand'], how='left')

# Rename columns for clarity
complete_data.columns = ['Year', 'Quarter', 'Brand', 'Annual Capacity']

# Convert Quarter to a datetime-like object for plotting
complete_data['Period'] = complete_data.apply(lambda row: f"{row['Year']}Q{int(row['Quarter'].replace('Q', ''))}", axis=1)
complete_data['Period'] = pd.PeriodIndex(complete_data['Period'], freq='Q').to_timestamp()

# Calculate annual capacity (since it's already given, just sum by year)
annual_data = complete_data.groupby(['Year', 'Brand'])['Annual Capacity'].sum().reset_index()

# Fill NaN values with 0 (assuming no capacity means 0)
annual_data['Annual Capacity'] = annual_data['Annual Capacity'].fillna(0)

# Create a Streamlit app
st.title("Annual Module Capacity by Brand")

# Filter by brand
preselected_brands = ['JA Solar', 'Jinko', 'Longi Green', 'Trina Solar']
#selected_brands = st.multiselect("Select Brands", brands)

# Filter data based on selected brands
filtered_data = annual_data[annual_data['Brand'].isin(preselected_brands)]


# Create a line plot
fig, ax = plt.subplots(figsize=(10, 6))
for brand in filtered_data['Brand'].unique():
    brand_data = filtered_data[filtered_data['Brand'] == brand]
    ax.plot(brand_data['Year'], brand_data['Annual Capacity'], label=brand)

ax.set_xlabel('Year')
ax.set_ylabel('Annual Capacity (MW)')
ax.set_title('Annual Module Capacity')
ax.legend()

# Display the plot
st.pyplot(fig)
