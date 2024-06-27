import streamlit as st
import pandas as pd
import os

# Define the base directory and file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "glossary_for_apps.xlsx")
df = pd.read_excel(file_path, header=0)

# Remove duplicates based on 'SINGKATAN' and 'ISTILAH' columns
df.drop_duplicates(subset=['SINGKATAN', 'ISTILAH'], keep='first', inplace=True)

# Function to generate an HTML table with text wrapping
def generate_html_table(data):
    # Start the table with styles
    html = """
    <style>
        td, th {
            border: 1px solid #ccc;
            padding: 8px;
            word-wrap: break-word;
        }
        .wide-column {
            max-width: 300px;  /* Increased width for the URAIAN column */
        }
    </style>
    <table>
    """

    # Add header row
    html += "<tr>"
    for col in data.columns:
        html += f"<th>{col}</th>"
    html += "</tr>"

    # Add data rows
    for _, row in data.iterrows():
        html += "<tr>"
        for col in data.columns:
            # Apply a specific style to 'URAIAN' column
            if col == 'URAIAN':
                html += f"<td class='wide-column'>{row[col]}</td>"
            else:
                html += f"<td>{row[col]}</td>"
        html += "</tr>"
    
    html += "</table>"
    return html

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
        # Generate and display the HTML table
        html_table = generate_html_table(results)
        st.markdown(html_table, unsafe_allow_html=True)
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
        # Generate and display the HTML table
        html_table = generate_html_table(filtered_data)
        st.markdown(html_table, unsafe_allow_html=True)
    else:
        st.write(f"Tidak ada istilah yang diawali huruf {selected_letter}")
