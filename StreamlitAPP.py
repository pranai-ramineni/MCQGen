import streamlit as st
import os
import json
import pandas as pd
from src.mcqgenerator.MCQgenerator import invoke_gen_chain
from src.mcqgenerator.my_logger import logging
from src.mcqgenerator.utils import extract_text_from_file
from io import StringIO





st.title("MCQ Generator")

with st.form("user_input"):
    upload = st.file_uploader("Upload a PDF or Text File")

    mcq_count = st.number_input("No of MCQs", min_value=1, max_value=5)

    subject = st.text_input("Subject", max_chars=20, placeholder="History")

    difficulty = st.text_input("Complexity of the questions", max_chars=20, placeholder="Simple")

    button = st.form_submit_button("Create Quiz")

file_path = os.path.join(os.path.dirname(__file__), 'src/mcqgenerator/response.json')
with open(file_path, 'r') as file:
    RESPONSE_JSON = json.load(file)

if button and upload is not None and mcq_count and difficulty:
    with st.spinner("loading..."):
        try:
            text = extract_text_from_file(upload)

            response = invoke_gen_chain(text,mcq_count,subject,difficulty,RESPONSE_JSON)

            json_data = json.loads(response["quiz"])
            st.json(json_data)
            st.write(response["review"])

            json_string = json.dumps(json_data, indent=2)
            json_bytes = json_string.encode('utf-8')
            st.write("Donwload the Questions in JSON")

            st.download_button(
                label = "Download Questions",
                data = json_bytes,
                file_name = "questions.json",
                mime = "applications/json"
            )

        except Exception as e:
            st.write(e)

