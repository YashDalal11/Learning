# from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

import streamlit as st
import os,re,glob,io
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
mistral_model = os.getenv("MODEL_NAME")
api_key = os.getenv("MODEL_API_KEY")
llm = ChatMistralAI(model=mistral_model, temperature=0, api_key=api_key)

frontend =  input("Enter Frontend Technology: ") or "Reactjs"
backend = input("Enter Backend Technology: ") or "Django"
cloud = input("Enter Cloud provider: ") or "AWS"
description = input("Enter description: ") or ""

template = """
    Consider yourself an expert software architect.
    Your job is to write the Python code using the diagrams module (version 0.23.4) with advanced web service (with colors and labels) to generate a cloud architecture diagram for the description provided.
    
    Important Note: 
    - If the description is not related to an architecture diagram, do not generate any code and return "Invalid request" as the output.
    - The description must be architecture-related. If it is not, return "Invalid request."
    
    Description: 
    {description}
    
    If the description is related to an architecture diagram, consider the following:
    - {FE} as frontend.
    - {BE} as backend.
    - {CL} as the cloud provider
    - Firewall
    - loadBalancer
    - Incorporate best practices.
    - Consider all security scenarios.
    
    Outformat of the diagrams code should be svg
    do not use any image URLs—only use everything provided by the diagrams library.
    
    Make sure to generate only code with advanced web service (with colors and labels) that supports diagrams version 0.23.4, and ensure that the code does not produce any errors.
"""

template_2 = """
{Chat_History}
Changes: make changes in above code {edit_text}
Answer:
"""

prompt = PromptTemplate(
    input_variables=["description","FE","BE","CL"], template=template
)

prompt2 = PromptTemplate(
    input_variables=["edit_text"], template=template_2
)
memory = ConversationBufferMemory(memory_key="Chat_History")


# llm = Ollama(model="llama2")
output_parser = StrOutputParser()

# chain = prompt|llm|output_parser
chain_1 =  LLMChain(
    llm=llm,
    prompt=prompt
)

chain_2 =  LLMChain(
    llm=llm,
    prompt=prompt2,
    memory=memory,
)
edit_text =''
while True:
    response=''
    print("\nResponding to your request...")
    if description :
        response = chain_1.predict(
            description=description,
            FE=frontend,
            BE=backend,
            CL=cloud
        )
        
        description=''
    elif edit_text:
        response = chain_2.predict(edit_text=edit_text)
        edit_text=''
    else:
        print("No valid Input")
        break
    
    code_block = re.search(r"```(.*?)```", response, re.DOTALL)
    if code_block:
        data = code_block.group(1).strip()
        code=data.replace("python","")
        code=code.replace("`","")
        cwd=os.getcwd()
        files=glob.glob(cwd+"/*.png")
        for file in files:
            os.remove(file)
        with io.open("codesample.py","w",encoding="utf-8")as f1:
            f1.write(code)
            f1.close()
        os.system("python codesample.py")
        files=glob.glob(cwd+"/*.svg")
        memory.save_context({"Question": description or edit_text}, {"Answer": code})
        print("\nImage Generated\n")
        edit_text = input("Edit your query: ")
    else: 
        print("Please give input related to cloud architecture")
        description = input("Enter description Again: ") or ''
        

