import os

def load_env():
  os.environ["OPENAI_API_TYPE"] = "azure"
  os.environ["OPENAI_API_VERSION"] = "2023-05-15"
  os.environ["AZURE_OPENAI_API_KEY"] = ""
  os.environ["AZURE_OPENAI_ENDPOINT"] = ""