from langchain_openai import AzureOpenAI
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory

def start(llm: AzureOpenAI):
  st.title("Lang Chain Demo")
  input_text =  st.text_input("Search what you want...")

  #  seeting LLM
  # llm = AzureOpenAI(deployment_name="text-davinci-003", temperature=0.8)

  # Memory
  person_memory = ConversationBufferMemory(input_key='name', memory_key='chart_history')
  dob_memory = ConversationBufferMemory(input_key='person', memory_key='chart_history')
  events_memory = ConversationBufferMemory(input_key='dob', memory_key='events_history')

  # Template and Chainig
  first_pt = PromptTemplate(input_variables=['name'], template="Tell me about celebraty {name}")
  chain = LLMChain(llm=llm, prompt=first_pt, verbose=True, output_key='person', memory=person_memory)

  sec_pt = PromptTemplate(input_variables=['person'], template="When was {person} born")
  chain2 = LLMChain(llm=llm, prompt=sec_pt, verbose=True, output_key='dob', memory=dob_memory)

  thir_pt = PromptTemplate(input_variables=['dob'], template="Mention 5 major events happend around {dob} in the wolrd")
  chain3 = LLMChain(llm=llm, prompt=thir_pt, verbose=True, output_key='incidents', memory=events_memory)

  # Running chains sequentially  
  # seq = SimpleSequentialChain(chains=[chain, chain2], verbose=True)
  seq = SequentialChain(chains=[chain, chain2, chain3], verbose=True, input_variables=['name'], output_variables=['person', 'dob', 'incidents'])

  # manual input
  print(seq({'name': 'virat koli'}))

  if input_text:
    st.write(input_text)
    # res = llm(input_text)
    # res = chain.run(input_text)
    res = seq({'name': input_text})
    st.write(res)

    with st.expander('Person'):
      st.info(person_memory.buffer)
    with st.expander('Major Events'):
      st.info(events_memory.buffer)

