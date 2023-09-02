#Simplify

## Introduction
------------
You can interact with your customized education plan with the Simplify App. Depending on your grade level, the application will provide applicable answers to any questions you ask in everyday language. This software uses a language model to generate accurate answers to your questions. simplify complex educational materials and provide users with a more accessible learning experience.

## Usage
-----
To use the simplify App, follow these steps:

1. Ensure that you have installed the required dependencies and added the OpenAI API key to the `.env` file.

# the required dependencies are
langchain==0.0.184
PyPDF2==3.0.1
python-dotenv==1.0.0
streamlit==1.18.1
openai==0.27.6
faiss-cpu==1.7.4
altair==4
tiktoken==0.4.0

2. Run the `main.py` file using the Streamlit CLI. Execute the following command:
   ```
   streamlit run simplify.py
   ```

3. Load  PDF document into the app you want to simplify by following the provided instructions.

4. Ask questions in natural language about the loaded PDFs using the chat interface.