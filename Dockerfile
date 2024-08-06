FROM python:3.12

WORKDIR /app

COPY . .

# processes the requirements.txt file in-place and creates a new file with the version constraints removed.
RUN sed 's/==.*//' requirements.txt | sed 's/>=.*//' | sed 's/<.*//' | sed '/^$/d' > requirements_no_versions.txt

RUN pip install -r requirements_no_versions.txt

CMD ["python", "-u", "-m", "vector_embedder_service.main"]