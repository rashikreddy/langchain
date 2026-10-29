import os
from dotenv import load_dotenv, find_dotenv

from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_azure_ai.utils.agents import pretty_print
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi import FastAPI
from langserve import add_routes   
import uvicorn


_ = load_dotenv(find_dotenv(), override=True)
azure_openai_key = os.environ["AZURE_OPENAI_KEY"]



model = AzureAIOpenAIApiChatModel(
    endpoint="https://grashikreddy-8785-resource.services.ai.azure.com/openai/v1/",
    credential=azure_openai_key, #if using Entra ID you can should use DefaultAzureCredential() instead
    model="gpt-5.4-mini",
    temperature=0.1
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an language translator. Translate the user's input to the requested language. language: {language}."),
    ("human", "{question}"),
])

chain = prompt | model | StrOutputParser()

app = FastAPI(
    title="Language Translator API",
    description="An API that translates text to the requested language using Azure OpenAI.",
    version="1.0.0"
)
add_routes(app, chain, path="/translate")
    

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
