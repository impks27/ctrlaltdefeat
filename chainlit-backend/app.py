import os
from openai import AsyncOpenAI

from fastapi.responses import JSONResponse

from chainlit.auth import create_jwt
from chainlit.server import app
import chainlit as cl

from chainlit.server import app
from fastapi import Request
from fastapi.responses import (
    HTMLResponse,
)
#from chainlit import JsonResponse

@app.get("/hello")
def hello(request: Request):
    print(request.headers)
    return HTMLResponse("Hello World")

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf(request):
    #if 'files[]' not in request.files:
        #return JsonResponse({'error': 'No files part'}, status=400)
    print("read Upload")
    print(request)
    return None
    #files = request.files.getlist('files[]')
    #print(files)

# @app.route('/upload-pdf', methods=['POST'])
# def upload_pdf(request):
#     if 'files[]' not in request.files:
#         return JsonResponse({'error': 'No files part'}, status=400)

#     files = request.files.getlist('files[]')

#     if len(files) == 0:
#         return JsonResponse({'error': 'No files selected'}, status=400)

#     results = []
#     for file in files:
#         if file.filename == '':
#             return JsonResponse({'error': 'One of the selected files has no filename'}, status=400)

#         if not file.filename.endswith('.pdf'):
#             return JsonResponse({'error': 'Invalid file format. Only PDF files are allowed'}, status=400)

#         # Process each PDF file here
#         # You can use PyPDF2 or other libraries to extract text or perform other operations
#         results.append({'filename': file.filename, 'status': 'processed'})

#     return JsonResponse({'success': 'PDF files uploaded and processed successfully', 'results': results})
