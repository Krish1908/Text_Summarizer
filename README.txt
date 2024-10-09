Hello everyone, the title is:
Automated Content Summarizer for News Articles

I have created a chatbot which uses GROQ CLOUD, Langchain, Streamlit modules. When users paste text into the interface, the chatbot generates a summary of the article, enabling users to save time and grasp the content more easily.

	
Tools and Methods used:

I have used the API KEY from GROQ CLOUD. As we use the API keys, the response time is much faster. The only thing is, we need internet connection to fetch the data via API KEYS.

There are few modules to be installed (dependencies):
langchain, chatgroq, and streamlit.

A template is created, and the output will be in the template provided.

The API KEY is stored in a secret file, so that when the code gets uploaded in the internet, other people won't misuse it.

To handle whitespace characters (gaps between paragraphs) in the articles, I implemented a function called preprocess_text, which removes these gaps.

The main function incorporates Streamlit, providing users with instructions on where to paste the long article. A large input box is available for this purpose.

A button is included to summarize the text. Upon clicking the button, the function first removes gaps between paragraphs, then processes the cleaned text with the prompt. The model takes a moment to analyze the prompt and generate the output.

And finally, to execute this code, we must use terminal and write the following code.

streamlit run Text_Summarizer_2.py


Thanks!!!