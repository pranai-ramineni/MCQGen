import os
import pandas as pd
import json
from .my_logger import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain 
from langchain.chains import SequentialChain
from langchain_community.callbacks.manager import get_openai_callback

llm = ChatOpenAI()

TEMPLATE = """
Text:{text}
You are an MCQ maker. Given the above text, it is your job to create a quiz of {number} of multiple choice questions for {subject} students in {difficulty} difficulty.
Make sure the questions are not repeated and check all the questions to be confirming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to make {number} MCQs in json format

RESPONSE_JSON
{response_json}
"""

quiz_gen_prompt = PromptTemplate(
    input_variables=["text","subject","difficulty","number","response_json"],
    template=TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompt = quiz_gen_prompt, output_key="quiz", verbose=True)

print(quiz_chain)

TEMPLATE2="""
You are an expert. Given a multiple choice quiz for {subject} for students. You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity.
if the quiz is not matching with the cognitive and analytical abilities of students, update the quiz questions which need to be changed and change the tone such that it perfectly fits the students abilities
Quiz_MCQs:
{quiz}

Check as an expert for the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject","quiz"],
    template=TEMPLATE2
)

review_chain = LLMChain(llm=llm, prompt = quiz_evaluation_prompt, output_key="review", verbose=True)

gen_chain = SequentialChain(chains=[quiz_chain,review_chain], input_variables=["text","number","subject","difficulty","response_json"],output_variables=["quiz","review"],verbose=True)

def invoke_gen_chain(text,number,subject,difficulty,response_json):

            with get_openai_callback() as cb:
                response = gen_chain(
                    {
                        "text":text,
                        "number":number,
                        "subject":subject,
                        "difficulty":difficulty,
                        "response_json": json.dumps(response_json)
                    }
                )
            return response

