import streamlit as st

st.title("Demo Streamlit Page 2")
st.header("Welcome to the demo page")
st.write("This is a simple Streamlit application.")

if st.button('Say hello'):
    st.write('Hello, Streamlit!')
else:
    st.write('Goodbye, Streamlit!')