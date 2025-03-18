import streamlit as st
# cd /c/Users/sebastian.hong/Documents/GitHub/
# run with streamlit run main.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


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

#                                                                           Plot with gaps
st.title("BNEF Tier PV (Gaps)")  # add a title

# Load the data
data = pd.read_excel('BNEF Tier PV.xlsx')

# Create a complete set of quarters for each brand
years = range(2021, 2026)
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
brands = data['Brand'].unique()

# Create all possible combinations of years and quarters
all_periods = []
for year in years:
    for quarter in quarters:
        # Skip quarters after Q1 for 2025
        if year == 2025 and quarter != 'Q1':
            continue
        all_periods.append(f"{year}Q{quarter[1]}")

# Create a multi-index DataFrame with all possible combinations
index = pd.MultiIndex.from_product([brands, all_periods], names=['Brand', 'Period'])
complete_data = pd.DataFrame(index=index).reset_index()

# Merge the original data into the complete set
complete_data = pd.merge(complete_data, data[['Brand', 'Period', 'Annual module capacity, MW/year']], 
                         on=['Brand', 'Period'], how='left')

# Convert Period to a decimal date format for plotting
complete_data['Year_Decimal'] = complete_data['Period'].apply(
    lambda x: int(x[:4]) + (int(x[5]) - 1) / 4
)

# Sort by Brand and Period
complete_data = complete_data.sort_values(['Brand', 'Year_Decimal'])

st.write(complete_data)

# Create a Streamlit app
st.title("Annual Module Capacity by Brand")

# Preselect brands
preselected_brands = ['JA Solar', 'Jinko', 'Longi Green', 'Trina Solar']

# Filter data based on preselected brands
filtered_data = complete_data[complete_data['Brand'].isin(preselected_brands)]

# Create a line plot
fig, ax = plt.subplots(figsize=(10, 6))
for brand in preselected_brands:
    brand_data = filtered_data[filtered_data['Brand'] == brand]
    ax.plot(brand_data['Year_Decimal'], brand_data['Annual module capacity, MW/year'], 
            label=brand, marker='o')

# Set x-axis ticks with 0.25 increments
start_year = 2021
end_year = 2025.25
x_ticks = np.arange(start_year, end_year, 0.25)
ax.set_xticks(x_ticks)
ax.set_xticklabels([f"{int(year)}-Q{int((year % 1) * 4) + 1}" if year % 1 else f"{int(year)}" for year in x_ticks], 
                   rotation=45, ha='right')

ax.set_xlabel('Year-Quarter')
ax.set_ylabel('Annual Capacity (MW)')
ax.set_title('Annual Module Capacity')
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='upper left')

# Display the plot
st.pyplot(fig)

##                                                  Interactive chart with Plotly
# Load the data
data = pd.read_excel('BNEF Tier PV.xlsx')

# Create a complete set of periods for each brand
years = range(2021, 2026)
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
brands = data['Brand'].unique()

# Create all possible combinations of years and quarters
all_periods = []
for year in years:
    for quarter in quarters:
        # Skip quarters after Q1 for 2025
        if year == 2025 and quarter != 'Q1':
            continue
        all_periods.append(f"{year}{quarter}")

# Create a multi-index DataFrame with all possible combinations
index = pd.MultiIndex.from_product([brands, all_periods], names=['Brand', 'Period'])
complete_data = pd.DataFrame(index=index).reset_index()

# Convert Period to Year and Quarter columns for merging
complete_data['Year'] = complete_data['Period'].str[:4].astype(int)
complete_data['Quarter'] = complete_data['Period'].str[4:]

# Merge the original data into the complete set
complete_data = pd.merge(complete_data, data[['Year', 'Quarter', 'Brand', 'Annual module capacity, MW/year']], 
                         on=['Brand', 'Year', 'Quarter'], how='left')

# Convert Period to a decimal date format for plotting
complete_data['Year_Decimal'] = complete_data.apply(
    lambda x: int(x['Year']) + (int(x['Quarter'][1]) - 1) / 4, axis=1
)

# Sort by Brand and Period
complete_data = complete_data.sort_values(['Brand', 'Year_Decimal'])

# Create a Streamlit app
st.title("Annual Module Capacity by Brand - Plotly")

# Preselect brands
preselected_brands = ['JA Solar', 'Jinko', 'Longi Green', 'Trina Solar']

# Filter data based on preselected brands
filtered_data = complete_data[complete_data['Brand'].isin(preselected_brands)]

# Create an interactive plot with Plotly
fig = px.line(filtered_data, 
              x='Year_Decimal', 
              y='Annual module capacity, MW/year',
              color='Brand',
              markers=True,
              title='Annual Module Capacity (2021Q1-2025Q1)',
              labels={'Year_Decimal': 'Year', 
                     'Annual module capacity, MW/year': 'Annual Capacity (MW)'},
              hover_data={'Year_Decimal': False,  # Hide the decimal year in hover
                         'Brand': True,
                         'Annual module capacity, MW/year': ':,.0f'})  # Format with thousand separators

# Customize the x-axis ticks
fig.update_xaxes(
    tickvals=np.arange(2021, 2025.25, 0.25),
    ticktext=[f"{int(year)}-Q{int((year % 1) * 4) + 1}" if year % 1 else f"{int(year)}" for year in np.arange(2021, 2025.25, 0.25)]
)

# Improve the layout
fig.update_layout(
    hovermode='closest',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    xaxis_title='Year-Quarter',
    yaxis_title='Annual Capacity (MW)',
    height=600,
    margin=dict(l=40, r=40, t=40, b=80)
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)