# IMPORT THE NECESSARY MODULES
import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

# PROMPT TEMPLATE
template = """
You are a summarization AI. Please summarize the following text:

{text}

Please wait... Your Summary is loading...
"""

# INITIALIZE THE MODEL AND PROMPT
model = OllamaLLM(model="llama3")
prompt = PromptTemplate.from_template(template)

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
                    result = model(formatted_prompt)
                    
                    # DISPLAY THE SUMMARY
                    st.subheader("Summary:")
                    st.write(result)
                
                except Exception as e:
                    st.error(f"Error occurred while generating summary: {e}")

summarize_text()
