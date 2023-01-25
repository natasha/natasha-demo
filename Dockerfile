
FROM python:3.9.13-slim

COPY requirements/app.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
CMD python app.py
