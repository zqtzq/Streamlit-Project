# query_handler.py
import json
from langchain.schema import Document
from helper_functions.llm import *
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import numpy as np

# Initialize the language model and embeddings model
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')

# Load the JSON file as a list of dictionaries
file_path = r'C:\Users\ASUS\Documents\ABC Bootcamp 2024 (Govtech)\Streamlit Project\scraped_content_old.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Initialize an empty list to store Document objects
documents = []
for item in data:
    doc = Document(
        page_content=item.get('content', ''),
        metadata={
            "url": item.get("url", ""),
            "depth": item.get("depth", ""),
            "type": item.get("type", "")
        }
    )
    documents.append(doc)

# Use RecursiveCharacterTextSplitter to split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=330, chunk_overlap=10, length_function=count_tokens)
splitted_documents = text_splitter.split_documents(documents)

# Create the FAISS vector database from the documents
vectordb = FAISS.from_documents(documents=splitted_documents, embedding=embeddings_model)

# Function to handle user queries using RAG with a custom prompt
def process_user_message(user_input):
    # Build prompt template
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Your answer should be clear and succinct.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Create a RetrievalQA chain with the custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    # Generate the response
    reply = qa_chain.invoke(user_input)

    return reply
