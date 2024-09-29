Week 2 Project :

Hello everyone, the title is:
Automated Content Summarizer for News Articles

I have created a chatbot which uses OLLAMA, Langchain, streamlit modules. When users paste text into the interface, the chatbot generates a summary of the article, enabling users to save time and grasp the content more easily.


Tools and Methods used:

I have downloaded ollama 3 in my local machine. Since the LLM model is stored locally, API KEYS are not required, although this may result in slightly slower response times.

There are few modules to be installed (dependencies):
langchain, langchain-ollama, ollama, and streamlit.

A template is created, and the output will be in the template provided.

The llama3 model is assigned to a variable named 'model', prompt template is stored in the variable 'prompt'.

To handle whitespace characters (gaps between paragraphs) in the articles, I implemented a function called preprocess_text, which removes these gaps.

The main function incorporates Streamlit, providing users with instructions on where to paste the long article. A large input box is available for this purpose.

A button is included to summarize the text. Upon clicking the button, the function first removes gaps between paragraphs, then processes the cleaned text with the prompt. The model takes a moment to analyze the prompt and generate the output.

Approximately, the summarization process takes about 3 to 4 minutes for longer texts.

And finally, to execute this code, we must use terminal and write the following code.

streamlit Text_Summarizer_2.py

Thanks!!!