# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap

from IPython.display import display
from IPython.display import Markdown

# Configure OpenRouter API
API_KEY = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

## Function to load OpenRouter model and get responses
def get_openrouter_response(question):
    try:
        response = client.chat.completions.create(
            model="anthropic/claude-3-haiku",  # You can change this to any model available on OpenRouter
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant. Provide clear, educational responses."},
                {"role": "user", "content": question}
            ],
            max_tokens=1000,
            temperature=0.7,
            stream=True
        )
        return response
    except Exception as e:
        return f"Error: {str(e)}"

##initialize our streamlit app

st.set_page_config(page_title="AI Chatbot")

st.header("Student Assistance Chatbot")

input=st.text_input("Input: ",key="input")


submit=st.button("Ask the question")

## If ask button is clicked

if submit:
    
    response=get_openrouter_response(input)
    st.subheader("The Response is")
    if hasattr(response, '__iter__') and not isinstance(response, str):
        for chunk in response:
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                st.write(chunk.choices[0].delta.content)
                print("_"*80)
    else:
        st.write(response)
    