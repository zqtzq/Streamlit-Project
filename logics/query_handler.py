__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import json
from langchain.schema import Document
from helper_functions.llm import *
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
# os.environ["OPENAI_API_KEY"] = API_KEY
from langchain_chroma import Chroma

# from vector_db.vector_db_data import Chroma  # Import the Chroma class


# llm to be used in RAG pipeplines in this notebook
# llm = ChatOpenAI(model='gpt-4o-mini', temperature=0) # can change the seed

# Load the JSON file as a list of dictionaries
file_path = r'C:\Users\ASUS\Documents\ABC Bootcamp 2024 (Govtech)\Streamlit Project\scraped_content_old.json'
with open(file_path, 'r') as f:
    data = json.load(f)  # Load JSON data into a list of dictionaries

# Initialize an empty list to store Document objects
documents = []

# Loop through each dictionary in the JSON list
for item in data:
    # Create a Document with content and associated metadata
    doc = Document(
        page_content=item.get('content', ''),  # Extract the 'content' field
        metadata={
            "url": item.get("url", ""),
            "depth": item.get("depth", ""),
            "type": item.get("type", "")
        }
    )
    documents.append(doc)


from langchain_text_splitters import RecursiveCharacterTextSplitter

# # In this case, we intentionally set the chunk_size to 330 tokens, to have the smallest document (document 2) intact
text_splitter = RecursiveCharacterTextSplitter(chunk_size=330, chunk_overlap=10, length_function=count_tokens)

# Split the documents into smaller chunks
splitted_documents = text_splitter.split_documents(documents)

from langchain_chroma import Chroma
# Create the vector database
vectordb = Chroma.from_documents(
    documents=splitted_documents,
    embedding=embeddings_model,
    collection_name="naive_splitter", # one database can have multiple collections
    persist_directory="./vector_db"
)


# Compared to the rag pipelines that we used above, this cell allows a custom prompt to be used
# This is useful for customizing the prompt to be used in the retrieval QA chain
# The prompt below is the standard template that is used in the retrieval QA chain
# It also includes the "documents" that are used in the prompt
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


def process_user_message(user_input):
    vectordb = load_vector_db()

    # Build prompt
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Your answer should be clear and succinct.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Run chain
    qa_chain = RetrievalQA.from_chain_type(
        ChatOpenAI(model='gpt-4o-mini'),
        retriever=vectordb.as_retriever(),
        return_source_documents=True, # Make inspection of document possible
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    reply = qa_chain.invoke(user_input)

    return reply