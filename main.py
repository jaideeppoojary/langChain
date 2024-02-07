from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import streamlit as st

load_dotenv()

st.title("Lang Chain Demo")
input_text =  st.text_input("Search what you want...")

llm = AzureChatOpenAI(temperature=0.8, openai_api_version="2023-05-15")

if input_text:
  st.write(input_text)
  response = llm("Tell me a joke")
  st.write(response)
