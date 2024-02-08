from dotenv import load_dotenv
from langchain_openai import AzureOpenAI
from env_setup import load_env
# import streamlit as st

load_env()
# st.title("Lang Chain Demo")
# input_text =  st.text_input("Search what you want...")

llm = AzureOpenAI(
    deployment_name="gpt-35-turbo",
    model_name="gpt-35-turbo",
)

print(llm("What is the capital of Italy?"))
# if input_text:
#   st.write(input_text)
#   response = llm("Tell me a joke")
#   st.write(response)
