from heading_class import Headings
from convert_dict import get_dict
import streamlit as st
def run_app(file, save_path):
    headings = Headings(file, save_path)
    headings.make_dir()
    headings.read_pdf()
    chunks = headings.create_chunks()
    
    for chunk in chunks:
        chunk = chunk.strip('\n')
        key_p = "left text " + str(headings.i)
        data_val = get_dict().extract_dict(chunk, key_p)
        headings.clean_dict(data_val)
        headings.initialize_vars()


        for key,value in list(headings.data_dict_vals.items()):
            key = headings.clean_text(key)

            if key.startswith("left text"):
                headings.handle_left_text(value)

            else:
                headings.handle_remaining_text(key,value)
            headings.last_key = key
        headings.i += 1
