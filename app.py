import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "glossary_for_apps.xlsx")
df = pd.read_excel(file_path, header=0)

# Remove duplicates based on 'SINGKATAN' and 'ISTILAH' columns
df.drop_duplicates(subset=['SINGKATAN', 'ISTILAH'], keep='first', inplace=True)

logo1 = os.path.join(BASE_DIR, 'images', 'kemenkeu.png')
logo2 = os.path.join(BASE_DIR, 'images', 'djpb.png')
logo3 = os.path.join(BASE_DIR, 'images', 'intress.png')

# Inject custom CSS to create a spacer div
st.markdown("""
<style>
.spacer {
    height: 30px;  /* Adjust the height as needed */
}
</style>
""", unsafe_allow_html=True)

# Create columns for the logos with specified widths
col1, col2, col3 = st.columns([8, 3, 4])
with col1:
    # Add spacer using custom CSS
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    st.image(logo1, use_column_width=True)

with col2:
    st.image(logo2, use_column_width=True)

with col3:
    # Add larger spacer using custom CSS
    st.markdown('<div class="spacer" style="height: 40px;"></div>', unsafe_allow_html=True)  # Adjust the height as needed
    st.image(logo3, use_column_width=True)

st.title('Glossary Direktorat Jenderal Perbendaharaan')

## Input for search query with a unique key
query = st.text_input("Masukan Kata Kunci:", key="main_search")

# Filtering data based on search query
if query:
    # Check if query is in any of the three columns
    mask = (
        df['SINGKATAN'].str.contains(query, case=False, na=False) |
        df['ISTILAH'].str.contains(query, case=False, na=False) |
        df['BAHASA INGGRIS'].str.contains(query, case=False, na=False)
    )
    results = df[mask]
    if not results.empty:
        results = results.reset_index(drop=True)  # Reset index and do not keep the old one
        st.table(results)  # Use st.table() which supports text wrapping
    else:
        st.write("Kata-Kata Tidak Dapat Ditemukan")

# Buttons for A-Z arranged horizontally
st.write("## Daftar Istilah Berdasarkan Alfabet")
letters = [chr(i) for i in range(65, 91)]  # ASCII values for A-Z
selected_letter = None
cols = st.columns(len(letters))
for i, letter in enumerate(letters):
    if cols[i].button(letter):
        selected_letter = letter

# Displaying terms starting with selected letter
if selected_letter:
    filtered_data = df[df['SINGKATAN'].str.startswith(selected_letter, na=False)]
    if not filtered_data.empty:
        filtered_data = filtered_data.reset_index(drop=True)
        st.dataframe(filtered_data, width = 1000, height=300)  # Adjust height as needed
    else:
        st.write(f"Tidak ada istilah yang diawali huruf {selected_letter}")