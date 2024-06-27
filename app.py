import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(layout="wide")

# Define the base directory and file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "glossary_for_apps.xlsx")
df = pd.read_excel(file_path, header=0)

# Remove duplicates based on 'SINGKATAN' and 'ISTILAH' columns
df.drop_duplicates(subset=['SINGKATAN', 'ISTILAH'], keep='first', inplace=True)

# Load images
logo1 = os.path.join(BASE_DIR, 'images', 'kemenkeu.png')
logo2 = os.path.join(BASE_DIR, 'images', 'djpb.png')
logo3 = os.path.join(BASE_DIR, 'images', 'intress.png')

# Display logos
col1, col2, col3 = st.columns([8, 3, 4])
with col1:
    st.image(logo1, use_column_width=True)
with col2:
    st.image(logo2, use_column_width=True)
with col3:
    st.image(logo3, use_column_width=True)

st.title('Glossary Direktorat Jenderal Perbendaharaan')

# Input for search query
query = st.text_input("Masukan Kata Kunci:", key="main_search")

# Filtering data based on search query
if query:
    mask = (
        df['SINGKATAN'].str.contains(query, case=False, na=False) |
        df['ISTILAH'].str.contains(query, case=False, na=False) |
        df['BAHASA INGGRIS'].str.contains(query, case=False, na=False)
    )
    results = df[mask]
    if not results.empty:
        gb = GridOptionsBuilder.from_dataframe(results)
        gb.configure_pagination()
        gb.configure_default_column(wrapText=True, autoHeight=True)
        gridOptions = gb.build()

        st_aggrid = AgGrid(results, gridOptions=gridOptions, height=500, width='100%', theme='streamlit')
    else:
        st.write("Kata-Kata Tidak Dapat Ditemukan")

# Buttons for A-Z arranged horizontally
st.write("## Daftar Istilah Berdasarkan Alfabet")
letters = [chr(i) for i in range(65, 91)]
selected_letter = None
cols = st.columns(len(letters))
for i, letter in enumerate(letters):
    if cols[i].button(letter):
        selected_letter = letter

# Displaying terms starting with selected letter
if selected_letter:
    filtered_data = df[df['SINGKATAN'].str.startswith(selected_letter, na=False)]
    if not filtered_data.empty:
        gb = GridOptionsBuilder.from_dataframe(filtered_data)
        gb.configure_pagination()
        gb.configure_default_column(wrapText=True, autoHeight=True)
        gridOptions = gb.build()

        st_aggrid = AgGrid(filtered_data, gridOptions=gridOptions, height=500, width='100%', theme='streamlit')
    else:
        st.write(f"Tidak ada istilah yang diawali huruf {selected_letter}")
