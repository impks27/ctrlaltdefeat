FROM python:3.9

WORKDIR /data
COPY chainlit-backend /data

# Launch Backend
RUN ls -l
RUN pip install -r requirements.txt
EXPOSE 80
CMD [ "chainlit", "run", "chainlit-backend/app.py", "--host", "0.0.0.0", "--port", "80"]
# Launch Frontend

