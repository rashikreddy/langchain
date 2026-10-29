import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True)
azure_openai_key = os.environ["AZURE_OPENAI_KEY"]


from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_azure_ai.utils.agents import pretty_print

model = AzureAIOpenAIApiChatModel(
    endpoint="https://grashikreddy-8785-resource.services.ai.azure.com/openai/v1/",
    credential=azure_openai_key, #if using Entra ID you can should use DefaultAzureCredential() instead
    model="gpt-5.4-mini"
)

messages = [
    SystemMessage(
      content=""
    ),
    HumanMessage(content="Tell me one fact avbout kennedy family apart that he is a president, i need detail response"),
]

reponse = model.invoke(messages)


for chunk in model.stream(
    "Tell me one fact avbout kennedy family apart that he is a president, i need detail response"
):
    print(chunk, end="", flush=True)