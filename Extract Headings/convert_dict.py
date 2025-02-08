import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
class get_dict:
    def __init__(self):
        self.gropapi = "YOUR GROQ API"
        self.llm = ChatGroq(temperature=0, groq_api_key=self.gropapi, model_name="llama-3.3-70b-versatile")

    def extract_dict(self, text, key_p):
        prompt_extract = PromptTemplate.from_template(
            '''
            ### TEXT FROM PDF:
            {text}
            ### INSTRUCTION:
            The provided text is extracted from a PDF document.  
            1. Extract the main headings and their corresponding text.  
            2. Present the output as a Python dictionary where:  
            - Headings are the keys.  
            - The text under each heading is the value.  
            3. If there is any initial text before the first heading, or text that doesn't fall under any heading, store it with the key `{key_p}`.  
            4. Ensure the output is a valid Python dictionary, formatted correctly, with no additional explanation or preamble.  

            ### VALID DICTIONARY (NO PREAMBLE):
            '''

        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"text": text, "key_p": key_p})
        res = res.to_json()
        return res
