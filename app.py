import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "Glossary_Compile.xlsx")
df = pd.read_excel(file_path, header=2)

# Title for your app
st.title('Glossary Istilah Direktorat Jenderal Perbendaharaan')

# Input for search query
query = st.text_input("Enter a keyword to search:")

# Filtering data based on search query
if query:
    results = df[df['SINGKATAN'].str.contains(query, case=False, na=False)]
    if not results.empty:
        st.dataframe(results)
    else:
        st.write("No results found")
else:
    # Display some instructions or general information
    st.write("Please enter a keyword above to search in the data.")
    