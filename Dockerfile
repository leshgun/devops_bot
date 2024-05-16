FROM python:3.11
#FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "main.py"]
