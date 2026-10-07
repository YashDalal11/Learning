# Load language model, embeddings, and index for conversational AI
from langchain.chat_models import ChatOpenAI                #model
from langchain.indexes import VectorstoreIndexCreator       #index
from langchain.document_loaders.csv_loader import CSVLoader #tool
from langchain.prompts import PromptTemplate                #prompt
from langchain.memory import ConversationBufferMemory       #memory
from langchain.chains import RetrievalQA                    #chain
import os

os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'

def load_llm():
    # Setting up the LLM model
    llm = ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")
    return llm


def load_index():
    # if you want to avoid the step of saving/loading a file, 
    # you can use the `from_documents()` method of the VectorstoreIndexCreator()
    loader = CSVLoader(file_path='uae_holidays.csv')
    index = VectorstoreIndexCreator().from_loaders([loader])
    return index

template = """
You are a assistant to help answer when are the official holidays, 
    based only on the data provided.
Context: {context}
-----------------------
History: {chat_history}
=======================
Human: {question}
Chatbot:
"""

# Create a prompt using the template
prompt = PromptTemplate(
    input_variables=["chat_history", "context", "question"],
    template=template
)

# Set up conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", 
          return_messages=True, input_key="question")

# Set up the retrieval-based conversational AI
qa = RetrievalQA.from_chain_type(
    llm=load_llm(),
    chain_type='stuff',
    retriever=load_index().vectorstore.as_retriever(),
    verbose=True,
    chain_type_kwargs={
        "prompt": prompt,
        "memory": memory,
    }
)

# Function to print the response for a given query
def print_response_for_query(query):
    return print(qa.run({"query": query}))

query = "Are there any holidays in March?"
print_response_for_query(query)