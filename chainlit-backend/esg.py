import os
import re
from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import AzureOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

# Method to get answer for a question


class ESGUtil:
        def __init__(self):
                  self.azure_endpoint = r"https://openaisatheesh.openai.azure.com/"
                  self.azure_deployment = "openapiembeddings"
                  self.openai_api_version = "2024-02-15-preview"
                  os.environ["AZURE_OPENAI_API_KEY"] = "a31b5dcb986d4480a067344fdd352814"
                  load_dotenv()

        # Method to get all questions for a pdf
        def getAllQuestionFromPDF(self, file):

            print("Invoked getAllQuestionFromPDF")

            loader = UnstructuredFileLoader(file)
            documents = loader.load()
            print("-----------------------------------");
            print(type(documents))
            print("-----------------------------------");
            print(documents[0].page_content)

            question_patterns = [
                r'\b(provide|describe|select|identify|who|what|when|where|why|how)\b.*\?',
                r'.*\?'
            ]

            # Step 3: Extract questions
            extracted_questions = []
            for pattern in question_patterns:
                extracted_questions.extend(re.findall(pattern, documents[0].page_content))

            # Step 4: Refinement (if necessary)
            # Step 5: Output or further processing

            questionsList = []
            for question in extracted_questions:
                questionsList.append(question);
            print("List of Questionf from "+file)
            print(questionsList)

        # Method to get answer for a given question
        def getAnswer(self, question, file):
            print("Invoked getAnswer")
            loader = UnstructuredFileLoader(file)
            documents = loader.load()


            #text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=30, 
                separators=["\n\n", "\n", " ", ""]
            )

            texts = text_splitter.split_documents(documents)

            #embeddings = OpenAIEmbeddings(model="openapiendpoint")
            embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=r"https://openaisatheesh.openai.azure.com/",
                azure_deployment="openapiembeddings",
                openai_api_version="2024-02-15-preview"
                #azure_endpoint = self.azure_endpoint, #r"https://openaisatheesh.openai.azure.com/",
                #azure_deployment = self.azure_deployment, #"openapiembeddings",
                #openai_api_version = self.openai_api_version #"2024-02-15-preview",
            )


            doc_search = Chroma.from_documents(texts,embeddings)
            #chain = RetrievalQA.from_chain_type(llm=AzureOpenAI(azure_endpoint=r"https://openaisatheesh.openai.azure.com/",openai_api_version="2024-02-15-preview",azure_deployment="openapiendpoint",model_kwargs={'engine':'gpt-35-turbo'}),chain_type='stuff', retriever = doc_search.as_retriever()))

            chain = RetrievalQA.from_chain_type(llm=AzureOpenAI(azure_endpoint=r"https://openaisatheesh.openai.azure.com/",openai_api_version="2024-02-15-preview",azure_deployment="openapiendpoint"),chain_type='stuff', retriever = doc_search.as_retriever())

            #chain = RetrievalQA.from_chain_type(llm=AzureOpenAI(azure_endpoint = self.azure_endpoint, openai_api_version = self.openai_api_version, azure_deployment = self.azure_deployment), chain_type='stuff', retriever = doc_search.as_retriever())

            #query = 'Describe how COVID-19 has impacted the world'
            print("Getting answer for question: "+question)
            print(chain.run(question))
 
obj = ESGUtil()
obj.getAllQuestionFromPDF('Survey-Questionnire-Part3.pdf');

obj.getAnswer('Describe how COVID-19 has impacted the world', 'Survey-Questionnire-Part1.pdf')