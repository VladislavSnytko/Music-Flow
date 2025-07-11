FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir db services models wbs

COPY db/ /app/db/
COPY services/ /app/services/
COPY models/ /app/models/
COPY wbs/ /app/wbs/
COPY main.py /app/


CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]