import streamlit as st
# cd /c/Users/sebastian.hong/Documents/GitHub/
# run with streamlit run main.py

import pandas as pd
import numpy as np
import plotly.express as px

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