
# STREAMLIT APP TO SUMMARIZE TEXT USING LANGCHAIN AND GROQ API

# IMPORT THE NECESSARY MODULES
import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# PROMPT TEMPLATE
template = """
You are a summarization AI. Please summarize the following text:

{text}

Please wait... Your Summary is loading...
"""

# GET API KEY - PRIORITY: ENV VARS > STREAMLIT SECRETS > ERROR
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    try:
        api_key = st.secrets["groq"]["api_key"]
    except (KeyError, FileNotFoundError):
        st.error("No API key found. Please set GROQ_API_KEY environment variable or configure Streamlit secrets.")
        st.stop()

# GET MODEL NAME
model_name = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')

# INITIALIZE THE MODEL AND PROMPT
model = ChatGroq(temperature=0,
               groq_api_key=api_key,
               model_name=model_name
               )
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# FUNCTION TO REMOVE SPACE BETWEEN PARAGRAPHS
def preprocess_text(text):
    return ' '.join(text.split())

# STREAMLIT MAIN FUNCTION
def summarize_text():
    st.title("News Article Summarizer")

    # INSTRUCTION FOR USER
    st.write("Paste your text into the box below and click 'Summarize'.")

    # TEXT INPUT
    user_input = st.text_area("Enter text to summarize", height=300)

    # BUTTON WHICH GENERATES SUMMARY
    if st.button("Summarize"):
        if user_input.strip() == "":
            st.error("Please enter some text to summarize.")
        else:
            # FUNCTION CALL TO REMOVE SPACE BETWEEN PARAGRAPHS
            processed_text = preprocess_text(user_input)
            
            # PROMPT IS FORMATTED
            formatted_prompt = prompt.format(text=processed_text)

            # FORMATTED PROMPT IS DISPLAYED
            st.write(f"**Formatted Prompt:**\n{formatted_prompt}")

            # LOADING CIRCLE
            with st.spinner('Generating summary...'):
                try:
                    # SUMMARY FROM MODEL
                    result = chain.invoke({"text" :formatted_prompt})
                    answer = result.content

                    # DISPLAY THE SUMMARY
                    st.subheader("Summary:")
                    st.write(answer)
                
                except Exception as e:
                    st.error(f"Error occurred while generating summary: {e}")

summarize_text()