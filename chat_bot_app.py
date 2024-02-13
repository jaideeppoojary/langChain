from dotenv import load_dotenv
from langchain_openai import AzureOpenAI
import streamlit as st

from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_openai.chat_models import AzureChatOpenAI

# Loading environment variables from .env
load_dotenv()

# UI
st.set_page_config(page_title="Conversational Q&A Chat Bot")
st.header("Hey Let's chat ✌️")

# Initial state of the session
if 'chat_bot_message' not in st.session_state:
  st.session_state['chat_bot_message'] = [
    SystemMessage(content="You are a comedian AI assistant")
  ]

chart_model = AzureChatOpenAI(deployment_name="gpt-35-turbo", temperature=0.5)

def get_chart_model_response(question: str):
  st.session_state['chat_bot_message'].append(HumanMessage(content=question))
  answer = chart_model.invoke(st.session_state['chat_bot_message'])
  st.session_state['chat_bot_message'].append(AIMessage(content=answer.content))
  return answer.content

input = st.text_input("Input: ", key="input")
submit = st.button(label="Ask your question")

if submit:
  res = get_chart_model_response(input) 
  st.subheader("The response is :")
  st.write(res)