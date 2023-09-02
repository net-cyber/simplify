import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template


#uses the Streamlit framework to create a web-based interface for simplifying complex concepts from text books. It also uses various libraries for PDF processing, natural language processing, and chat-based language models. 


#This function takes a list of PDF documents as input, reads the text content from each PDF, and returns the concatenated text as a single string.
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
#This function splits the input text into smaller chunks using a character-based text splitter from the langchain package. It returns a list of text chunks.
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=700,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

#This function processes the text chunks to create vector representations of the text using OpenAI's embeddings and the FAISS library for vector storage. It returns the vector stores.
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstores = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstores

#This function sets up a conversational chain using an NLP model from langchain. It uses the vector store and other components to create a conversational retrieval chain.
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain
   
#This function takes a user's question as input, uses the conversation chain to generate a response, and updates the chat history. It also writes the user and bot messages to the Streamlit interface.
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            
def main():
    #Configures the Streamlit web application, including setting the page title and icon and applying custom CSS styles.
    load_dotenv()
    st.set_page_config(page_title=" Simplify",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    
    #Initializes the conversation and chat history state variables if they are not already initialized.
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
        
    #Creates a Streamlit header and a text input field for users to ask questions.
    st.header(" Simplify complex concepts :")
    user_question = st.text_input("Ask me a question 😊😊😊 :")
    #Handles user input by processing the user's question and generating a response using a chatbot model and NLP techniques.
    if user_question:
        handle_userinput(user_question)
        
    with st.sidebar:
        st.subheader("Your Text book")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
                
                
                
                
if __name__ == '__main__':
    main()