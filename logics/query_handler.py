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

@st.cache_data
def load_documents(file_path):
    # Load and process documents only once, then cache the results

    with open(file_path, 'r') as f:
        data = json.load(f)

    documents = [
        Document(
            page_content=item.get('content', ''),
            metadata={
                "url": item.get("url", ""),
                "depth": item.get("depth", ""),
                "type": item.get("type", "")
            }
        )
        for item in data
    ]

    # Split the documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=330, chunk_overlap=10, length_function=count_tokens)
    return text_splitter.split_documents(documents)

file_path = 'scraped_content_old.json'
# r'C:\Users\ASUS\Documents\ABC Bootcamp 2024 (Govtech)\Streamlit Project\scraped_content_old.json'
splitted_documents = load_documents(file_path)#

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

def safety_message_translator_chinese(message):
    delimiter = "####"

    system_message = f"""
    You will be provided with a response reply in English language from a Large Language Model (LLM) related to workplace safety and health to the user. 
    The response will be enclosed in a pair of {delimiter}. Your task is to translate the response into Chinese, bearing in mind that the message context is in Singapore's safety industry, and technical jargon may be used in the message. The reader is a foreign worker who is not fluent in English. The translation should be succinct, clear and easy to understand.

    If the response reply is "I don't know":, you should not reinvent the wheel and come up with something that is not in the response.  
    """
    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{message}{delimiter}"},
    ]
    translated_response_chinese_str = get_completion_by_messages(messages)
    translated_response_chinese_str = translated_response_chinese_str.replace("'", "\"")
    # translated_response_chinese = json.loads(translated_response_chinese_str)
    return translated_response_chinese_str

def translate_output_chinese(message):

    translation_chinese = safety_message_translator_chinese(message)
    return translation_chinese


def safety_message_translator_bengali(message):
    delimiter = "####"

    system_message = f"""
    You will be provided with a response reply in English language from a Large Language Model (LLM) related to workplace safety and health to the user. 
    The response will be enclosed in a pair of {delimiter}. Your task is to translate the response into Bengali, bearing in mind that the message context is in Singapore's safety industry, and technical jargon may be used in the message. The reader is a foreign worker who is not fluent in English. The translation should be succinct, clear and easy to understand.

    If the response reply is "I don't know":, you should not reinvent the wheel and come up with something that is not in the response.  
    """
    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{message}{delimiter}"},
    ]
    translated_response_bengali_str = get_completion_by_messages(messages)
    translated_response_bengali_str = translated_response_bengali_str.replace("'", "\"")
    return translated_response_bengali_str

def translate_output_bengali(message):

    translation_bengali = safety_message_translator_bengali(message)
    return translation_bengali