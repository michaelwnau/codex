import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = None

# Custom template for the LLM model
CUSTOM_TEMPLATE = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(CUSTOM_TEMPLATE)

def validate_environment():
    """Validate that all required environment variables are set."""
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return openai_api_key

def get_pdf_text(pdf_docs):
    """Extract text from PDF documents."""
    if not pdf_docs:
        raise ValueError("No PDF documents provided")
    
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            raise Exception(f"Error reading PDF {pdf.name}: {str(e)}")
    
    if not text.strip():
        raise ValueError("No text could be extracted from the PDFs")
    
    return text

def get_chunks(text):
    """Split text into chunks for processing."""
    if not text:
        raise ValueError("No text provided for chunking")
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_text(text)
    if not chunks:
        raise ValueError("Text could not be split into chunks")
    
    return chunks

def get_vectorstore(text_chunks):
    """Create a vector store from text chunks."""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore
    except Exception as e:
        raise Exception(f"Error creating vector store: {str(e)}")

def get_conversationchain(vectorstore):
    """Create a conversation chain with the LLM."""
    try:
        openai_api_key = validate_environment()
        
        llm = ChatOpenAI(
            temperature=0.1,
            api_key=openai_api_key
        )
        
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            condense_question_prompt=CUSTOM_QUESTION_PROMPT,
            memory=memory,
        )
        
        return conversation_chain
    except Exception as e:
        raise Exception(f"Error creating conversation chain: {str(e)}")

def handle_question(question):
    """Process and display the response to a user question."""
    try:
        response = st.session_state.conversation({"question": question})
        st.session_state.chat_history = response["chat_history"]
        
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(
                    user_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True
                )
            else:
                st.write(
                    bot_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True
                )
    except Exception as e:
        st.error(f"Error processing question: {str(e)}")

def process_documents(docs):
    """Process uploaded documents and initialize conversation chain."""
    try:
        raw_text = get_pdf_text(docs)
        text_chunks = get_chunks(raw_text)
        vectorstore = get_vectorstore(text_chunks)
        st.session_state.conversation = get_conversationchain(vectorstore)
        return True
    except Exception as e:
        st.error(f"Error processing documents: {str(e)}")
        return False

def main():
    """Main application function."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Validate environment
        try:
            validate_environment()
        except ValueError as e:
            st.error(str(e))
            return

        # Set up page configuration
        st.set_page_config(
            page_title="Codex - PDF Query System",
            page_icon=":books:"
        )
        st.write(css, unsafe_allow_html=True)
        
        # Main header
        st.header("Codex - PDF Query System")
        
        # Question input
        question = st.text_input("Ask a question about your documents:")

        # Sidebar for document upload
        with st.sidebar:
            st.subheader("Document Upload")
            docs = st.file_uploader(
                "Upload your PDFs and click 'Process'",
                accept_multiple_files=True,
                type=['pdf']
            )
            
            if st.button("Process Documents"):
                if not docs:
                    st.error("Please upload at least one PDF document.")
                else:
                    with st.spinner("Processing documents..."):
                        if process_documents(docs):
                            st.success("Documents processed successfully!")

        # Handle user questions
        if question:
            if st.session_state.conversation is None:
                st.warning("Please process your documents before asking questions.")
            else:
                handle_question(question)

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
