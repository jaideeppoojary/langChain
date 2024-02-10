from dotenv import load_dotenv
from langchain_openai import AzureOpenAI
import basic01
import basic01_promt_engg
# load_env()
load_dotenv()

llm = AzureOpenAI(deployment_name="text-davinci-003", temperature=0.8)

# 1st ex
# basic01.start(llm)

# 2nd promt engg ex.
basic01_promt_engg.start(llm)
