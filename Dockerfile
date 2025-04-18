FROM python:3.8.5-slim

WORKDIR /todo_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "run.py"]

