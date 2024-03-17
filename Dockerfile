FROM python:3.9

WORKDIR /data
COPY . /data

# Launch Backend
RUN ls -l
RUN pip install -r chainlit-backend/requirements.txt
CMD [ "chainlit", "run", "chainlit-backend/app.py", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
# Launch Frontend

