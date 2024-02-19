# from dotenv import load_dotenv
from openai import AzureOpenAI
import streamlit as st

from langchain.schema import HumanMessage, SystemMessage, AIMessage, FunctionMessage
from langchain_openai.chat_models import AzureChatOpenAI

# Loading environment variables from .env
# load_dotenv()

from env_setup import load_env
load_env()

# function calling 
from api_service import FilterModel, FilterOption, get_asset_detail
import json
def get_asset_basic_detail(title: str = '', expireMpuEndDate = None, isFuture: bool = False):
  filter = [FilterOption(property='Title', operator='cn', value=title or '')]
  if expireMpuEndDate is not None:
    filter.append(FilterOption(property='ExpireMpuEndDate', operator= 'gt' if isFuture is True else 'lt', value=expireMpuEndDate))
  
  print(f"\n\n{title}-{expireMpuEndDate}-{isFuture}\n\n")
  ata = get_asset_detail(filter=FilterModel(page_size=5, filters=filter))
  print(f"\n\n{ata.json()}\n\n")
  print(f"\n\n{ata.json()['records']}\n\n")
  return json.dumps(ata.json()['records'])

# Function description for tool
tools = [
        {
            "type": "function",
            "function": {
                "name": "get_asset_basic_detail",
                "description": "Get the asset basic details by name or expire date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Asset Title or name",
                        },
                        "expireMpuEndDate": {
                            "type": "string",
                            "description": "expire date.",
                        },
                        "isFuture": {
                            "type": "boolean",
                            "description": "Weather to lis the asset which comes after expire date ?",
                        },
                    },
                    "required": ["title"],
                },
            },
        }
    ]
# end fn calling 

# UI
st.set_page_config(page_title="Conversational Q&A Chat Bot")
st.header("Hey there ✌️")

# Initial state of the session
if 'chat_bot_message' not in st.session_state:
  st.session_state['chat_bot_message'] = [
    {"role": "system", "content": "You are a helpful AI assistant. you should understand the user requirement and call the necessary function use its result give a simple response to user. If you are unable to find the function just say you are still learning. "}
  ]

import os
client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2023-12-01-preview"
)

model_name = 'gpt-35-turbo'
def get_chart_model_response():
  # client = AzureOpenAI(deployment_name="gpt-35-turbo-16k", temperature=0.5, verbose=True, tools=tools)
  response = client.chat.completions.create(
        model=model_name,
        messages=st.session_state['chat_bot_message'],
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
  
  response_message = response.choices[0].message
  tool_calls = response_message.tool_calls

  if tool_calls:
    # Step 3: call the function
    # Note: the JSON response may not always be valid; be sure to handle errors
    available_functions = {
        "get_asset_basic_detail": get_asset_basic_detail,
    }  # only one function in this example, but you can have multiple
    st.session_state['chat_bot_message'].append(response_message)  # extend conversation with assistant's reply
    # Step 4: send the info for each function call and function response to the model
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            title=function_args.get("title"),
        )
        st.session_state['chat_bot_message'].append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        print(function_name)
    second_response = client.chat.completions.create(
        model=model_name,
        messages=st.session_state['chat_bot_message'],
    )  # get a new response from the model where it can see the function response
    print('second_response', second_response.choices[0].message.content)
    return second_response.choices[0].message.content
  return response_message.content

input = st.text_input("Input: ", key="input")
submit = st.button(label="Ask your question")

if submit:
  st.session_state['chat_bot_message'].append({"role": "user", "content": input}) 
  res = get_chart_model_response() 
  st.subheader("The response is :")
  st.write(res)