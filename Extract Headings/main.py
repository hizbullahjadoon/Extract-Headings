import streamlit as st
from headings_run import run_app

st.title("Extract and Save with PDF Headings")
st.subheader("Upload a File")
uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False, type="pdf")
process_url_clicked = st.button("Process PDF")

try:

    if process_url_clicked:
        if uploaded_file is not None:
            file_name = uploaded_file.name
            file_name = file_name.split(sep = '.')[0]
            save_path = f'./New_Headings/{file_name}'
            run_app(uploaded_file, save_path)

            st.success("File Processed")    

except Exception as e:
    st.write("An Error ", e, " Occurred")