import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "Glossary_Compile.xlsx")
df = pd.read_excel(file_path, header=2)

st.title('Glossary Direktorat Jenderal Perbendaharaan')

# Display logos at the top of the page
logo1 = os.path.join(BASE_DIR, 'images', 'kemenkeu.png')
logo2 = os.path.join(BASE_DIR, 'images', 'djpb.png')
logo3 = os.path.join(BASE_DIR, 'images', 'intress.png')
st.image([logo1, logo2, logo3], width=100)


# Input for search query
query = st.text_input("Masukan Kata Kunci:")

# Filtering data based on search query
if query:
    results = df[df['SINGKATAN'].str.contains(query, case=False, na=False)]
    if not results.empty:
        st.dataframe(results)
    else:
        st.write("No results found")
else:
    # Display some instructions or general information
    st.write("Masukan kata kunci di atas untuk mencari istilah")
    

import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "Glossary_Compile.xlsx")
df = pd.read_excel(file_path, header=2)

st.title('Glossary Direktorat Jenderal Perbendaharaan')

# Input for search query
query = st.text_input("Masukan Kata Kunci:")

# Filtering data based on search query
if query:
    results = df[df['SINGKATAN'].str.contains(query, case=False, na=False)]
    if not results.empty:
        st.dataframe(results)
    else:
        st.write("No results found")
else:
    st.write("Masukan kata kunci di atas untuk mencari istilah")

# Buttons for A-Z
st.write("## Daftar Istilah Berdasarkan Alfabet")
col1, col2 = st.columns(2)
with col1:
    letters = [chr(i) for i in range(65, 91)]  # ASCII values for A-Z
    clicked = st.radio("Pilih Alfabet:", letters)

# Displaying terms starting with selected letter
with col2:
    if clicked:
        filtered_data = df[df['SINGKATAN'].str.startswith(clicked, na=False)]
        if not filtered_data.empty:
            st.dataframe(filtered_data)
        else:
            st.write(f"Tidak ada istilah yang diawali huruf {clicked}")
