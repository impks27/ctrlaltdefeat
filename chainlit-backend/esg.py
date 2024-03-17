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
from langchain.indexes import VectorstoreIndexCreator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Method to get answer for a question


class ESGUtil:
        def __init__(self):
                  self.azure_endpoint = r"https://openaisatheesh.openai.azure.com/"
                  self.azure_deployment = "openapiembeddings"
                  self.openai_api_version = "2024-02-15-preview"
                  os.environ["AZURE_OPENAI_API_KEY"] = "a31b5dcb986d4480a067344fdd352814"
                  load_dotenv()

        # Method to get all questions for a pdf
        def getAllQuestionsFromPDF(self, file):

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
            print("List of Questions from "+file)
            print(questionsList)
            return questionsList

        def getAllSplitTexts(self):
            print("Invoked getAllSplitTexts")
            loader = UnstructuredFileLoader("2021-annual-report.pdf")
            documents = loader.load()
            #text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=30, 
                separators=["\n\n", "\n", " ", ""]
            )
            texts = text_splitter.split_documents(documents)

            #loader = UnstructuredFileLoader("2022-annual-report.pdf")
            #documents = loader.load()
            ##text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
            #text_splitter = RecursiveCharacterTextSplitter(
            #    chunk_size=300,
            #    chunk_overlap=30, 
            #    separators=["\n\n", "\n", " ", ""]
            #)
            #texts1 = text_splitter.split_documents(documents)
            #texts += texts1
            return texts
        
        def generateAnswer(self, reportYear, inputQuestion):
             print("Invoked generateAnswer")
             

        # Method to get answer for a given question
        def getAnswer(self, question, texts):
            print("Invoked getAnswer")

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

            chain = RetrievalQA.from_chain_type(
                 llm=AzureOpenAI(azure_endpoint=r"https://openaisatheesh.openai.azure.com/",
                                 openai_api_version="2024-02-15-preview",azure_deployment="openapiendpoint",temperature=0.5),
                                 chain_type='stuff', retriever = doc_search.as_retriever(),
                                 return_source_documents=True, verbose=True) #search_type="similarity", search_kwargs={"k":2}, return_source_documents=True

            #chain = RetrievalQA.from_chain_type(llm=AzureOpenAI(azure_endpoint = self.azure_endpoint, openai_api_version = self.openai_api_version, azure_deployment = self.azure_deployment), chain_type='stuff', retriever = doc_search.as_retriever())

            #query = 'Describe how COVID-19 has impacted the world'
            print("Getting answer for question: "+question)
            #print(chain.run(question))
            print(chain({"query": question}, return_only_outputs=True))
        
        # Method to get answer for a given question - index
        def getAnswerIndex(self, question, file):
            print("Invoked getAnswer. index")
            loader = UnstructuredFileLoader(file)
            os.environ["AZURE_OPENAI_API_KEY"] = "a31b5dcb986d4480a067344fdd352814"
            os.environ['OPENAI_API_KEY'] = 'dummy_key'
            index_creator = VectorstoreIndexCreator(
                vectorstore_cls=Chroma,
                embedding=AzureOpenAIEmbeddings(
                azure_endpoint=r"https://openaisatheesh.openai.azure.com/",
                azure_deployment="openapiembeddings",
                openai_api_version="2024-02-15-preview"
                ),
                text_splitter=RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=30, 
                separators=["\n\n", "\n", " ", ""])
            )   

            index = index_creator.from_loaders([loader])
            index.query(question)

        def create_pdf(self, file_name, questions_answers):
            c = canvas.Canvas(file_name, pagesize=letter)
            textobject = c.beginText(100, 750)  # Position of the text in the PDF
            textobject.setFont("Helvetica-Bold", 14)  # Font and size of the questions
            for question, answer in questions_answers.items():
                textobject.textLine(f"Q: {question}")
                textobject.setFont("Helvetica", 12)  # Font and size of the answers
                textobject.textLine(f"A: {answer}")
                textobject.moveCursor(0, 20)
            c.drawText(textobject)
            c.save();

        def getAnswerforQuestionnaire(self, file, texts):
             questionsList = self.getAllQuestionsFromPDF(file)
             print("Questions:")
             print(questionsList)
             content = {}
             for question in questionsList:
                print("Question: "+question)
                answer = self.getAnswer(question, texts)
                #print("Answer: "+answer)
                content[question] = answer;
             answerfile = "answer.pdf"
             self.create_pdf(answerfile, content)



#obj = ESGUtil()
#obj.getAllQuestionsFromPDF('Survey-Questionnire-Part3.pdf');

#obj.getAnswer('Describe how COVID-19 has impacted the world', 'Survey-Questionnire-Part1.pdf')

#file_name = "questions_answers.pdf"
#questions_answers = {
#                "What is Python?": "Python is a high-level programming language...",
#                "What are the benefits of using Python?": "Some benefits of using Python include...",
#                "How do you define a function in Python?": "In Python, you can define a function using the 'def' keyword...",
#                # Add more questions and answers here
#            }
#obj.create_pdf(file_name, questions_answers)
#print(f"PDF file '{file_name}' created successfully.")
#obj.getAnswerforQuestionnaire("Survey-Questionnire-Part3.pdf");
#texts = obj.getAllSplitTexts()
#obj.getAnswer('Describe how COVID-19 has impacted the world', texts)
#obj.getAnswerforQuestionnaire("Survey-Questionnire-Part3.pdf", texts)