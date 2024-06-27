import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# Define the base directory and file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "glossary_for_apps.xlsx")
df = pd.read_excel(file_path, header=0)

# Remove duplicates based on 'SINGKATAN' and 'ISTILAH' columns
df.drop_duplicates(subset=['SINGKATAN', 'ISTILAH'], keep='first', inplace=True)

# Function to generate an HTML table with text wrapping and handle NaN values
def generate_html_table(data):
    # Replace NaN values with an empty string
    data = data.fillna('')
    
    # Start the table with styles
    html = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px;
            word-wrap: break-word;
        }
        .wide-column {
            max-width: 500px;  /* Adjust width for the URAIAN column */
        }
        .tooltip {
            position: relative;
            display: inline-block;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 500px;
            background-color: #f9f9f9;
            color: #000;
            text-align: left;
            border: 1px solid #ccc;
            padding: 8px;
            position: absolute;
            z-index: 1;
            top: 100%;
            left: 50%;
            margin-left: -250px;
            word-wrap: break-word;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
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
            cell_value = row[col]
            if col == 'URAIAN':
                truncated_value = cell_value if len(cell_value) <= 500 else cell_value[:500] + "..."
                html += f"<td class='wide-column'><div class='tooltip'>{truncated_value}<span class='tooltiptext'>{cell_value}</span></div></td>"
            else:
                html += f"<td>{cell_value}</td>"
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