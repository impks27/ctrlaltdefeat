import os
# import uuid
from openai import AsyncOpenAI

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from chainlit.auth import create_jwt
from chainlit.server import app
import chainlit as cl
import esg

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    HTMLResponse,
)
from typing import List

# CORS configuration allowing all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# cache to store metadata
metadata_cache = {}

#client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@app.get("/custom-auth")
async def custom_auth():
    # Verify the user's identity with custom logic.
    token = create_jwt(cl.User(identifier="Test User"))
    return JSONResponse({"token": token})

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )
    await cl.Message(content="Connected to Chainlit!").send()

'''
@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
'''

@app.get("/esgreports/keepalive/ping")
async def ping(request: Request):
    print(request.headers)
    return {"status": "success", "message": "Ping successful"}

class Item(BaseModel):
    inputQuestion: str
    reportYear: str

@app.post("/questionnaire/generatefirstdraft/generateAnswer")
async def generateAnswer(item: Item):
    print(item)
    print(dir(item))
    obj = esg.ESGUtil();
    reportYear = item.reportYear
    inputQuestion = item.inputQuestion
    response = obj.generateAnswer(reportYear,inputQuestion)
    return {
  "reportYear": reportYear,
  "questionnireSummary": {
    "response": response,
    "status": "Success",
    "citation": "string",
    "documentReference": "string",
    "accuracy": "string",
    "confidenceScores": "string"
  }
}


@app.post("/esgreports/upload")
async def upload_esg_reports(documentName: List[UploadFile] = File(...),
                             DocumentURL: List[str] = Form(...),
                             YearOfReport: str = Form(...)):
    print(len(documentName))
    try:
        # Generate a unique tracker id for each file
        tracker_id = "adkjfalsoueir62386" # TODO 

        # Create the 'uploaded_files' directory if it doesn't exist
        os.makedirs("uploaded_files", exist_ok=True)

        # Process each uploaded file
        for file in documentName:

            # Save the file in the 'uploaded_files' folder
            file_path = os.path.join('uploaded_files', file.filename)
            with open(file_path, 'wb') as buffer:
                buffer.write(await file.read())

            # Create metadata and add it to the cache
            metadata = {
                "documentName": file.filename,
                "documentURL": DocumentURL[documentName.index(file)],
                "YearOfReport": YearOfReport
            }
            metadata_cache[f"{file.filename}_{YearOfReport}"] = metadata

        return JSONResponse(content={"status": "success", "message": "Files uploaded successfully", "tracker_id": tracker_id})
    
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    

# Example data representing uploaded documents
uploaded_documents = [
    {
        "documentName": "example_document.pdf",
        "metadata": {
            "documentType": "PDF",
            "referenceLink": None,
            "generated By": "Uploader",
            "reportYear": "2022"
        }
    },
    {
        "documentName": "example_url_document.txt",
        "metadata": {
            "documentType": "URL",
            "referenceLink": "https://example.com",
            "generated By": "Scraper",
            "reportYear": "2022"
        }
    }
]

class UploadedDocument(BaseModel):
    documentName: str
    metadata: dict

class RetrieveESGReportsRequest(BaseModel):
    reportYear: str

class RetrieveESGReportsResponse(BaseModel):
    documents: List[UploadedDocument]

@app.post("/esgreports/retrieve", response_model=RetrieveESGReportsResponse)
async def retrieve_esg_reports(request: RetrieveESGReportsRequest):
    try:
        report_year = request.reportYear
        retrieved_documents = [UploadedDocument(**doc) for doc in uploaded_documents if doc["metadata"]["reportYear"] == report_year]
        return RetrieveESGReportsResponse(documents=retrieved_documents)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)