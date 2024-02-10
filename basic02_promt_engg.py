from langchain_openai import AzureOpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain


def start(llm: AzureOpenAI):
    # 1.
    my_promt = PromptTemplate(
        template="I want you to act as the finacial advisor for people. In a easy way explain the basics of {concept}",
        input_variables=["concept"],
    )
    chain = LLMChain(llm=llm, prompt=my_promt)
    # print(chain.invoke({"concept": "Stock market"}))

    # 2. FewShortTem
    rel_prompt = PromptTemplate(
        template="Guess the relation of word: {name}", input_variables=["name"]
    )
    ex = [
        {"name": "student", "relation": "study"},
        {"name": "teacher", "relation": "teach"},
    ]
    few_prompt = FewShotPromptTemplate(
        examples=ex,
        example_prompt=rel_prompt,
        input_variables=["name"],
        prefix="Give the relation of every name",
        suffix="Name: {name}",
    )

    chain2 = LLMChain(prompt=few_prompt, llm=llm, verbose=True)
    print(chain2.invoke({"name": "developer"}))
