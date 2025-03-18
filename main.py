import streamlit as st


# app.py, run with 'streamlit run app.py'
import pandas as pd

# df = pd.read_csv("./data/titanic.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
df = pd.read_excel('BNEF Tier PV.xlsx')  # will work for Excel files

st.title("BNEF Tier PV")  # add a title
st.write(df)  # visualize my dataframe in the Streamlit app