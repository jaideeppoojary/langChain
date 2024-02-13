from dotenv import load_dotenv
from langchain_openai import AzureOpenAI
import streamlit as st

# Loading environment variables from .env
load_dotenv()

def get_open_ai_response(question: str):
  llm = AzureOpenAI(deployment_name="gpt-35-turbo", temperature=0.7)
  response = llm(question)
  return response

st.set_page_config(page_title="Q&A Bot")
st.header("LangChain Powered application")

input = st.text_input("Input: ", key="input")
submit = st.button(label="Ask your question")

if submit:
  res = get_open_ai_response(input) 
  st.subheader("The response is :")
  st.write(res)