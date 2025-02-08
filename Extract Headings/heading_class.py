from langchain.text_splitter import RecursiveCharacterTextSplitter
import PyPDF2
import os
import ast
import re
from convert_dict import get_dict
import streamlit as st
class Headings:
    def __init__(self, file, save_path):
        self.text = ""
        self.file = file
        self.list_dicts = [None,None]
        self.last_key = None
        self.temp_dict = None
        self.i = 1
        self.path = save_path
        self.data_dict_vals = None
    
    def read_pdf(self):
        reader = PyPDF2.PdfReader(self.file)
        pages = []
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pages.append(page.extract_text())
        
        whole_text = " "
        for text in pages:
            whole_text += text
        self.text = whole_text
        
    
    def make_dir(self):
        os.makedirs(f'{self.path}', exist_ok=True)

    def create_chunks(self):

        r_splitter = RecursiveCharacterTextSplitter(
            separators= ["\n\n", "\n", "."],
            chunk_size = 5500,
            chunk_overlap = 0
        )
        chunks = r_splitter.split_text(self.text)

        return chunks
    
    def clean_dict(self, data_val):
        data_dict_vals = data_val["kwargs"].values()
        dict_vals_list = list(data_dict_vals)
        cleaned_data_vals = list(dict_vals_list)[0].strip('```python\n').strip('```')
        self.data_dict_vals = ast.literal_eval(cleaned_data_vals)
    
    def initialize_vars(self):
        
        if self.list_dicts[0]:
            self.temp_dict = self.list_dicts[0]
        
        self.list_dicts[0] = self.list_dicts[1]
        self.list_dicts[1] = self.data_dict_vals
        if self.list_dicts[0] is None:
            self.last_key = list(self.list_dicts[1].keys())[0]
        else:
            self.last_key = list(self.list_dicts[0].keys())[-1]

    def clean_text(self,text):
        text = re.sub(r'[\/:*.?"<>|]', '', text)
        text = text.replace('\n', '')
        return text
    
    def save_file(self,save_path,value):
        with open(self.path + "/" + save_path + '.txt', 'w', encoding='utf-8') as file:
                file.write(value)
    

    
    def handle_left_text(self,value):
        if self.list_dicts[0] is None:
            self.list_dicts[1] = self.data_dict_vals
            save_name = value[:25].replace('\n', '')
            save_name = save_name.replace('/','')
            self.save_file(save_name,value)
        
        elif self.list_dicts[1] is not None and self.list_dicts[0] is not None:
            self.last_key = list(self.list_dicts[0].keys())[-1]
            if self.last_key.startswith("left text"):
                temp_lastkey = list(self.temp_dict.keys())[-1]
                self.temp_dict[temp_lastkey] += '\n' + value
                value = self.temp_dict[temp_lastkey]
                self.last_key = temp_lastkey
                self.list_dicts[0][self.last_key] = value
                self.last_key = self.last_key.replace('/','')
                self.save_file(self.last_key, value)

            else:

                self.list_dicts[0][self.last_key] += '\n' + value
                value = self.list_dicts[0][self.last_key]
                self.last_key = self.last_key.replace('/','')
                self.save_file(self.last_key, value)

    def handle_remaining_text(self,key,value):
        self.last_key = key
        if isinstance(value, list):
            value = "\n".join(str(item) for item in value)
        else:
            value = str(value)
        key1 = key.replace('/','')
        self.save_file(key1, value)


