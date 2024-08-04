FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# RUN pip install python-dotenv

# RUN pip install openai

# RUN pip install chromadb

# RUN pip install tensorflow-hub

CMD ["python", "-m", "vector_embedder_service.main"]