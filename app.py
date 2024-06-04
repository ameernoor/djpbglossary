import streamlit as st
import pandas as pd
import os
from PIL import Image

def resize_image(input_path, output_path, height):
    with Image.open(input_path) as img:
        # Calculate the new width to maintain the aspect ratio
        aspect_ratio = img.width / img.height
        new_width = int(height * aspect_ratio)
        new_img = img.resize((new_width, height))
        new_img.save(output_path)

# Specify the desired height
desired_height = 100

# Resize images
resize_image(os.path.join(BASE_DIR, 'images', 'kemenkeu.jpeg'), os.path.join(BASE_DIR, 'images', 'kemenkeu_resized.jpeg'), desired_height)
resize_image(os.path.join(BASE_DIR, 'images', 'djpb.jpeg'), os.path.join(BASE_DIR, 'images', 'djpb_resized.jpeg'), desired_height)
resize_image(os.path.join(BASE_DIR, 'images', 'intress.jpeg'), os.path.join(BASE_DIR, 'images', 'intress_resized.jpeg'), desired_height)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "Glossary_Compile.xlsx")
df = pd.read_excel(file_path, header=2)

# Display logos with better alignment
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.image(os.path.join(BASE_DIR, 'images', 'kemenkeu_resized.jpeg'), use_column_width=True)
with col2:
    st.image(os.path.join(BASE_DIR, 'images', 'djpb_resized.jpeg'), use_column_width=True)
with col3:
    st.image(os.path.join(BASE_DIR, 'images', 'intress_resized.jpeg'), use_column_width=True)

st.title('Glossary Direktorat Jenderal Perbendaharaan')

## Input for search query with a unique key
query = st.text_input("Masukan Kata Kunci:", key="main_search")

# Filtering data based on search query
if query:
    results = df[df['SINGKATAN'].str.contains(query, case=False, na=False)]
    if not results.empty:
        st.dataframe(results, index=False)  # Hide the index
    else:
        st.write("No results found")
else:
    st.write("Masukan kata kunci di atas untuk mencari istilah")

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
        st.dataframe(filtered_data, index=False)  # Hide the index
    else:
        st.write(f"Tidak ada istilah yang diawali huruf {selected_letter}")
